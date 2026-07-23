"""
Compact recon digest for the grep-first dedup workflow in CLAUDE.md.

Prints "#id [cat/diff]  question" for every question matching a
keyword/regex, instead of the full 4-answer object a Grep hit returns --
cheaper to read when scanning a well-covered film's existing angles before
drafting new questions.

Usage:
  python scripts/recon.py aladdin
  python scripts/recon.py "jafar|genie|agrabah"
  python scripts/recon.py rapunzel --all-fields
  python scripts/recon.py rapunzel --show-answer
"""
import argparse
import re
import sys

from _common import load_corpus


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern", help="regex/keyword to search for, case-insensitive")
    ap.add_argument(
        "--all-fields", action="store_true",
        help="also search wrong answers, not just question text + correct answer",
    )
    ap.add_argument("--show-answer", action="store_true", help="include the correct answer in output")
    args = ap.parse_args()

    corpus = load_corpus()
    rx = re.compile(args.pattern, re.IGNORECASE)

    hits = []
    for q in corpus:
        haystack = q["question"] + " " + q["answers"][0]
        if args.all_fields:
            haystack += " " + " ".join(q["answers"][1:])
        if rx.search(haystack):
            hits.append(q)

    hits.sort(key=lambda q: q["id"])
    for q in hits:
        line = f'#{q["id"]:>5}  [{q.get("category", "?")}/{q.get("difficulty", "?")}]  {q["question"]}'
        if args.show_answer:
            line += f'  -> {q["answers"][0]}'
        print(line)
    print(f"\n{len(hits)} matches.")


if __name__ == "__main__":
    sys.exit(main())
