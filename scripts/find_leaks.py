"""
Whole-corpus scan for CLAUDE.md rule #2 (answer leaked into the question
text) using the shared two-tier detector in _common.py's find_answer_leaks().

This exists because the check that caught 3 leaks in the 2026-07-29 quality
audit was a one-off scratch script, never checked in -- so nothing caught
the next 2 leaks (#1230, #2177) until players flagged them. This script is
the checked-in replacement, runnable any time as its own audit pass instead
of only living inside a draft-batch check.

Tier 1 (verbatim answer substring in the question) is high-precision --
report and fix on sight. Tier 2 (stemmed/prefix token overlap unique to the
correct answer) is advisory -- always eyeball, since some hits are
legitimate (a title-answer that must contain a franchise word the question
also mentions, e.g. "Frozen Fever" answering a question that says "Frozen").

Both tiers are lexical/stem-based only -- a pure-synonym leak (question says
"canine," answer is "Dog") shares no stem and will not be caught here.

Tier 2 in the `music` category deserves extra scrutiny: song titles are
short and a question describing a song almost has to paraphrase it, so a
tier-2 hit there is close to a guaranteed real leak (found 5 in the
2026-09-08 audit: "wishes to be part of the human world" -> "Part of Your
World", "wishes and dreams" -> "A Dream Is a Wish...", "impatience to
become king" -> "I Just Can't Wait to Be King", "around the next bend in
the river" -> "Just Around the Riverbend", "while getting lost" -> "Lost
in the Woods"). Prioritize eyeballing that category's hits first.

Usage:
  python scripts/find_leaks.py            # both tiers
  python scripts/find_leaks.py --tier1    # verbatim only
  python scripts/find_leaks.py --tier2    # advisory token-overlap only
"""
import sys

from _common import find_answer_leaks, load_corpus


def main():
    only_tier = None
    if "--tier1" in sys.argv:
        only_tier = 1
    elif "--tier2" in sys.argv:
        only_tier = 2

    corpus = load_corpus()
    tier1_hits = []
    tier2_hits = []

    for q in corpus:
        for leak in find_answer_leaks(q):
            if only_tier and leak["tier"] != only_tier:
                continue
            (tier1_hits if leak["tier"] == 1 else tier2_hits).append((q, leak))

    print(f"Scanned {len(corpus)} questions.\n")

    if not only_tier or only_tier == 1:
        print(f"--- TIER 1: verbatim answer in question ({len(tier1_hits)}) ---")
        for q, leak in tier1_hits:
            print(f"  id={q['id']}: \"{q['question']}\"")
            print(f"    answers[0]='{q['answers'][0]}'  <- verbatim in question text")
        print()

    if not only_tier or only_tier == 2:
        print(f"--- TIER 2: shared word, unique to correct answer, advisory ({len(tier2_hits)}) ---")
        for q, leak in tier2_hits:
            print(f"  id={q['id']}: \"{q['question']}\"")
            print(f"    answers[0]='{q['answers'][0]}'  shared token='{leak['token']}'  distractors={q['answers'][1:]}")
        print()

    total = len(tier1_hits) + (len(tier2_hits) if not only_tier or only_tier == 2 else 0)
    if total == 0:
        print("No leaks found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
