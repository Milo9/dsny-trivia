"""Whole-corpus structural check — the deploy gate for question shards.

Fails (exit 1) only on things that would break the app or make a question
unanswerable: a shard or manifest that isn't valid JSON, a manifest entry
whose file is missing, duplicate IDs across shards, a missing/blank field,
not exactly 4 non-empty answers, two answers that are the same after
normalization (case/articles/honorifics), an invalid category or
difficulty, or "all/none of the above". Advisory checks (leaks, near-dupes,
category heuristics) stay in their own scripts and are not gates.

deploy.ps1 runs this automatically when anything under questions/ changed.
Run from project root: python scripts/validate_corpus.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import BASE, VALID_CATEGORIES, VALID_DIFFICULTIES, normalize_answer  # noqa: E402


def main():
    errors = []
    qdir = os.path.join(BASE, "questions")
    try:
        with open(os.path.join(qdir, "manifest.json"), encoding="utf-8") as f:
            shards = json.load(f)["shards"]
    except Exception as e:
        print(f"ERROR questions/manifest.json: {e}")
        return 1

    seen_ids = {}
    total = 0
    for rel in shards:
        path = os.path.join(BASE, rel)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            errors.append(f"{rel}: {e}")
            continue
        if not isinstance(data, list):
            errors.append(f"{rel}: top level is not a JSON array")
            continue
        for q in data:
            total += 1
            qid = q.get("id")
            where = f"{rel} id={qid}"
            if not isinstance(qid, int):
                errors.append(f"{where}: id is not an integer")
            elif qid in seen_ids:
                errors.append(f"{where}: duplicate id (also in {seen_ids[qid]})")
            else:
                seen_ids[qid] = rel
            if not isinstance(q.get("question"), str) or not q["question"].strip():
                errors.append(f"{where}: missing question text")
            answers = q.get("answers")
            if not isinstance(answers, list) or len(answers) != 4 or \
                    not all(isinstance(a, str) and a.strip() for a in answers):
                errors.append(f"{where}: needs exactly 4 non-empty string answers")
            else:
                norm = [normalize_answer(a) for a in answers]
                if len(set(norm)) != 4:
                    errors.append(f"{where}: two answers are the same after normalization: {answers}")
                if any(a.strip().lower() in ("all of the above", "none of the above") for a in answers):
                    errors.append(f"{where}: uses all/none of the above")
            if q.get("category") not in VALID_CATEGORIES:
                errors.append(f"{where}: invalid category {q.get('category')!r}")
            if q.get("difficulty") not in VALID_DIFFICULTIES:
                errors.append(f"{where}: invalid difficulty {q.get('difficulty')!r}")

    for e in errors:
        print("ERROR " + e)
    print(f"{total} questions in {len(shards)} shards, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
