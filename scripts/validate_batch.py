"""
Pre-append sanity check for a batch of drafted questions, before they get
pasted into a shard JSON file.

Checks: valid JSON, required fields present, id type/uniqueness (against
both the existing corpus and within the batch itself), difficulty/category
enum membership, exactly 4 answers, exact-duplicate question text against
the corpus, and two advisory heuristics for the "Answer structure" rules in
CLAUDE.md (answers that read like sentences rather than short noun phrases,
and an answer0 that appears verbatim inside its own question text). These
heuristics are advisory, not proof of a violation -- always eyeball what
gets flagged; this does not verify facts.

Usage:
  python scripts/validate_batch.py path/to/draft.json
"""
import json
import sys

from _common import VALID_CATEGORIES, VALID_DIFFICULTIES, load_corpus


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/validate_batch.py path/to/draft.json")
        return 2
    draft_path = sys.argv[1]

    try:
        with open(draft_path, encoding="utf-8") as f:
            draft = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: {draft_path} is not valid JSON: {e}")
        return 1

    if not isinstance(draft, list):
        print("ERROR: draft file must be a JSON array of question objects.")
        return 1

    corpus = load_corpus()
    existing_ids = {q["id"] for q in corpus}
    existing_questions_norm = {q["question"].strip().lower() for q in corpus}
    next_id = max(existing_ids) + 1 if existing_ids else 1

    errors = []
    warnings = []
    seen_batch_ids = set()

    for i, q in enumerate(draft):
        loc = f"draft[{i}]"
        if isinstance(q, dict) and "id" in q:
            loc += f" (id={q['id']})"

        if not isinstance(q, dict):
            errors.append(f"{loc}: not a JSON object")
            continue

        required = {"id", "question", "answers", "difficulty", "category"}
        missing = required - q.keys()
        if missing:
            errors.append(f"{loc}: missing field(s) {sorted(missing)}")
            continue

        qid = q["id"]
        if not isinstance(qid, int):
            errors.append(f"{loc}: id must be an integer, got {type(qid).__name__}")
        else:
            if qid in existing_ids:
                errors.append(f"{loc}: id {qid} already used in the corpus")
            if qid in seen_batch_ids:
                errors.append(f"{loc}: id {qid} duplicated within this batch")
            seen_batch_ids.add(qid)

        if q["difficulty"] not in VALID_DIFFICULTIES:
            errors.append(f"{loc}: difficulty '{q['difficulty']}' not in {sorted(VALID_DIFFICULTIES)}")

        if q["category"] not in VALID_CATEGORIES:
            errors.append(f"{loc}: category '{q['category']}' not in {sorted(VALID_CATEGORIES)}")

        answers = q["answers"]
        if not isinstance(answers, list) or len(answers) != 4:
            errors.append(f"{loc}: answers must be a list of exactly 4 strings")
            continue

        norm_q = q["question"].strip().lower()
        if norm_q in existing_questions_norm:
            errors.append(f"{loc}: question text is an exact duplicate of an existing question")

        for j, a in enumerate(answers):
            if not isinstance(a, str) or not a.strip():
                errors.append(f"{loc}: answers[{j}] is empty or not a string")
                continue
            word_count = len(a.split())
            if word_count > 5 or any(p in a for p in (". ", ", and", "; ")):
                warnings.append(
                    f"{loc}: answers[{j}]='{a}' looks like a sentence, not a short noun phrase (rule #3)"
                )

        correct = answers[0].strip().lower()
        if len(correct) >= 4 and correct in norm_q:
            warnings.append(
                f"{loc}: answers[0]='{answers[0]}' appears verbatim in the question text (possible leak, rule #2)"
            )

    print(f"Checked {len(draft)} draft questions against {len(corpus)} existing.")
    print(f"Next available id after current corpus: {next_id}\n")

    if warnings:
        print(f"--- {len(warnings)} WARNING(S) (advisory, eyeball these) ---")
        for w in warnings:
            print("  " + w)
        print()

    if errors:
        print(f"--- {len(errors)} ERROR(S) ---")
        for e in errors:
            print("  " + e)
        return 1

    print("No errors found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
