# v1.52 flag follow-up (backlog #6)

Reviewer: Claude. Prepared 2026-11-11. Plan: release-1.52-flag-followup-plan.json.

## #976 retired, replaced by #1399

Comparison: #976 asked which app provides onboard schedules and chat; its answer
"Disney Cruise Line Navigator" repeated the stem's cruise subject (answer-in-question
leak). Removing the brand words leaves "Navigator", which #1399 already teaches
(the printed schedule the app replaced was the "Personal Navigator"). Memorizing
#1399's answer would solve a leak-free #976, so #1399 is kept and #976 retired.

## Rewords (all four options re-sourced; reviews in release-1.52-flag-followup-reviews.json)

- #2432 Onward A113: distractors B227/C118/T809 (player flag: "none of the other
  answers make sense") replaced with near-miss codes A131/B113/A311.
- #1355: now asks which Magic Kingdom land holds The Hall of Presidents
  (old stem "all U.S. presidents" gave away the attraction name).
- #2243: distractors are now all "Frozen ..." names, so "Frozen-themed" no longer
  singles out Frozen Kingdom.
- #2642: stem no longer names the "Pixar Pal-A-Round"; remaining "Pixar" token is the
  land name (leak finding accepted).
- #1236: stem says "three-circle mouse-head silhouettes" instead of "Mickey Mouse".
- #427: answers are distances (5K/10K/half marathon/1 mile); recheck 2027-02-09.
- #2589: all options are Element- names.
- #518 / #521: inverted; the stem names the author (Dickens / Stevenson) and the
  answer is the film, so the title no longer echoes the novel.
- #925: options drop "Riverboat"/"Sailing Ship"; "paddle-wheel" excludes Columbia.

Not edited: #138 (ship horn). The v1.43 wording limits it to the Magic-class ships;
TouringPlans (Feb 2025) confirms the Magic and Wonder horns play only When You Wish
Upon a Star, while Dream-class ships play several tunes (the likely source of the
"plays both songs" report).

Result: complete-for-scope, 11 reviewed, 10 approved, 10 edited, 1 retired.
Gate: 0 errors. Leak findings for the scope are fixed or decided.

## Player flags closed (production, owner-authorized via backlog #6)

After 510bd87 was live on Pages, all six open flags were closed with the same atomic
write review.html performs (immutable `resolutions` event + parent `_resolved`),
reviewer "Claude (for Milo)", outcome `fixed`, each referencing the commit that
published its fix: #911 x2 -> 4082fb7 (retired), #2432 -> 510bd87, #2080 / #708 /
#138 -> f46f0a4. Read-back confirmed; 0 of 13 flags open on 2026-11-12.
