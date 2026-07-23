"""
Near-duplicate question detector.

Flags candidate duplicate/reworded questions using lexical similarity so a
human eyeball pass only has to look at flagged pairs, not the whole corpus.
Two passes, mirroring the method used in the 2026-07-21 dedup audit:

  A. Token-Jaccard similarity on question text, above --threshold. Catches
     questions that are reworded restatements of each other.
  B. Exact match on normalized correct answer (answers[0]), grouped and
     dumped regardless of question-text similarity. This is the
     "same answer, different framing" case a similarity threshold can miss
     (this is how the WALL-E Axiom duplicate slipped past the thresholded
     pass in the original audit). In whole-corpus mode, groups larger than
     --max-group-size are skipped (usually just a common name). In --new
     mode that cap is NOT applied, since output is already scoped to groups
     touching the draft -- capping there would silently hide the exact case
     this pass exists to catch.

Usage:
  python scripts/find_near_dupes.py                    # whole-corpus self-audit
  python scripts/find_near_dupes.py --new draft.json    # new-vs-existing + new-vs-new
  python scripts/find_near_dupes.py --threshold 0.45
"""
import argparse
import json
import sys
from collections import defaultdict

from _common import jaccard, load_corpus, normalize_answer, tokenize


def fmt(q):
    return (
        f'#{q["id"]:>5}  ({q.get("category", "?")}/{q.get("difficulty", "?")})  {q["question"]}\n'
        f'        -> {q["answers"][0]}'
    )


def find_similar_pairs(pool_a, pool_b, threshold, same_pool):
    """Token-Jaccard over question text, using an inverted index to skip
    pairs that share no non-stopword token instead of comparing every pair."""
    tokens_a = [tokenize(q["question"]) for q in pool_a]
    tokens_b = tokens_a if same_pool else [tokenize(q["question"]) for q in pool_b]

    index = defaultdict(list)
    for j, toks in enumerate(tokens_b):
        for t in toks:
            index[t].append(j)

    results = []
    for i, toks_a in enumerate(tokens_a):
        candidates = set()
        for t in toks_a:
            candidates.update(index[t])
        for j in candidates:
            # j <= i already guarantees each unordered pair is visited once
            # in same_pool mode, so no separate seen-pairs tracking is needed.
            if same_pool and j <= i:
                continue
            score = jaccard(toks_a, tokens_b[j])
            if score >= threshold:
                results.append((score, pool_a[i], pool_b[j]))
    results.sort(key=lambda x: -x[0])
    return results


def group_by_answer(pool, max_group_size, require_from=None):
    """Group questions by normalized answers[0]; return groups sized >=2.
    If require_from is given, only return groups with >=1 member from it, and
    max_group_size is NOT applied -- require_from already keeps the output
    scoped to the draft, so the cap would otherwise silently drop exactly the
    "draft answer matches a common existing answer" case this pass exists to
    catch. Without require_from (whole-corpus self-audit), groups above
    max_group_size are dropped since they're usually a common name, not a
    duplicate cluster."""
    groups = defaultdict(list)
    for q in pool:
        norm = normalize_answer(q["answers"][0])
        if len(norm) < 3:
            continue
        groups[norm].append(q)

    require_ids = {id(q) for q in require_from} if require_from is not None else None
    flagged = {}
    for norm, members in groups.items():
        if len(members) < 2:
            continue
        if require_ids is not None:
            if not any(id(m) in require_ids for m in members):
                continue
        elif len(members) > max_group_size:
            continue
        flagged[norm] = members
    return flagged


def print_pairs(pairs):
    if not pairs:
        print("  (none)")
        return
    for score, qa, qb in pairs:
        print(f"\n[{score:.2f}]")
        print(fmt(qa))
        print(fmt(qb))


def print_groups(groups):
    if not groups:
        print("  (none)")
        return
    for norm, members in sorted(groups.items(), key=lambda kv: len(kv[1])):
        print(f"\nanswer='{norm}'  ({len(members)} questions)")
        for m in members:
            print("  " + fmt(m).replace("\n", "\n  "))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", help="path to a draft JSON file (array of question objects)")
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument(
        "--max-group-size", type=int, default=6,
        help="whole-corpus self-audit only: skip answer-groups larger than this "
             "(likely a common name, not a duplicate cluster). Ignored with --new, "
             "where output is already scoped to groups touching the draft.",
    )
    args = ap.parse_args()

    corpus = load_corpus()

    if args.new:
        with open(args.new, encoding="utf-8") as f:
            draft = json.load(f)
        print(f"Loaded {len(draft)} draft questions, comparing against {len(corpus)} existing.\n")

        print("=" * 70)
        print(f"PASS A: new-vs-existing question-text similarity (Jaccard >= {args.threshold:.2f})")
        print("=" * 70)
        print_pairs(find_similar_pairs(draft, corpus, args.threshold, same_pool=False))

        print("\n" + "=" * 70)
        print("PASS A: new-vs-new (within draft) similarity")
        print("=" * 70)
        print_pairs(find_similar_pairs(draft, draft, args.threshold, same_pool=True))

        print("\n" + "=" * 70)
        print("PASS B: same normalized correct-answer groups (must include >=1 draft question)")
        print("=" * 70)
        print_groups(group_by_answer(draft + corpus, args.max_group_size, require_from=draft))
        print(
            "\n(Pass B on --new is not size-capped -- a draft answer matching a "
            "common existing answer will show here even in a large group. Eyeball "
            "for the 'same fact, different wording' case; a shared answer alone "
            "isn't proof of a duplicate.)"
        )

    else:
        print(f"Whole-corpus self-audit over {len(corpus)} questions.\n")

        print("=" * 70)
        print(f"PASS A: question-text similarity (Jaccard >= {args.threshold:.2f})")
        print("=" * 70)
        print_pairs(find_similar_pairs(corpus, corpus, args.threshold, same_pool=True))

        print("\n" + "=" * 70)
        print(f"PASS B: same normalized correct-answer groups (size 2-{args.max_group_size})")
        print("=" * 70)
        print_groups(group_by_answer(corpus, args.max_group_size))


if __name__ == "__main__":
    sys.exit(main())
