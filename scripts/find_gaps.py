"""
Novelty gap-finder: surfaces content the bank is most likely still missing,
per the "richest under-mined veins" note in CLAUDE.md's content generation
strategy section.

Two signals:
  1. Distractor-only entities -- names/terms that appear as a WRONG answer
     somewhere but have never been the correct answer (answers[0]) to any
     question. Each is a candidate seed for a new question.
  2. Sequel/short coverage -- a maintained list of direct-to-video sequels
     and theatrical shorts (scripts/_common.py:SEQUELS_AND_SHORTS), with a
     live hit-count against the corpus, lowest-coverage first.

Usage:
  python scripts/find_gaps.py                 # both reports
  python scripts/find_gaps.py --distractors    # distractor-only report only
  python scripts/find_gaps.py --sequels        # sequels/shorts report only
  python scripts/find_gaps.py --min-count 3    # distractor must recur >=N times to be listed
"""
import argparse
import re
import sys
from collections import Counter

from _common import SEQUELS_AND_SHORTS, load_corpus, normalize_answer

GENERIC_STOPLIST = {
    "true", "false", "yes", "no", "none", "all of the above", "none of the above",
}


def report_distractors(corpus, min_count, limit):
    answer0_norm = {normalize_answer(q["answers"][0]) for q in corpus}
    counts = Counter()
    examples = {}
    for q in corpus:
        for wrong in q["answers"][1:]:
            norm = normalize_answer(wrong)
            if len(norm) < 3 or norm in GENERIC_STOPLIST or norm.isdigit():
                continue
            counts[norm] += 1
            examples.setdefault(norm, []).append(q["id"])

    candidates = [
        (norm, n) for norm, n in counts.items()
        if norm not in answer0_norm and n >= min_count
    ]
    candidates.sort(key=lambda x: -x[1])

    print("=" * 70)
    print(f"DISTRACTOR-ONLY ENTITIES (never the correct answer, seen >= {min_count}x)")
    print("=" * 70)
    for norm, n in candidates[:limit]:
        ids = examples[norm][:4]
        print(f"  {n:>3}x  {norm:<40} seen in #{', #'.join(str(i) for i in ids)}")
    shown = min(len(candidates), limit)
    print(f"\n{len(candidates)} candidates total (showing top {shown}).")


def report_sequels(corpus):
    print("=" * 70)
    print("SEQUEL / SHORT COVERAGE (lowest first = biggest opportunity)")
    print("=" * 70)
    counts = []
    for entry in SEQUELS_AND_SHORTS:
        n = sum(
            1 for q in corpus
            if re.search(entry["pattern"], q["question"] + " " + q["answers"][0], re.IGNORECASE)
        )
        counts.append((entry["title"], n))
    counts.sort(key=lambda x: x[1])
    for title, n in counts:
        flag = "  <-- ZERO COVERAGE" if n == 0 else ""
        print(f"  {n:>3}  {title}{flag}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--distractors", action="store_true")
    ap.add_argument("--sequels", action="store_true")
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--limit", type=int, default=60)
    args = ap.parse_args()
    corpus = load_corpus()

    do_both = not args.distractors and not args.sequels
    if args.distractors or do_both:
        report_distractors(corpus, args.min_count, args.limit)
        print()
    if args.sequels or do_both:
        report_sequels(corpus)


if __name__ == "__main__":
    sys.exit(main())
