# Question generation round 5: 200 easy questions (backlog #18)

Reviewer: Claude, 2026-11-25. IDs 2996-3195, all easy, new shard `questions/q-011.json`.

| Category | Added |
| --- | ---: |
| movies | 75 |
| characters | 44 |
| pixar | 35 |
| music | 19 |
| parks | 16 |
| walt | 6 |
| cruise | 5 |

Bank after: 2,391 active, 596 easy / 1,071 medium / 724 hard.

## How the facts were chosen

Every stem and correct answer in the bank, active and retired, was read first, grouped by
film or category. About 250 of some 350 ideas were drafted; the rest, and 50 of the
drafts, were cut as duplicates, leaks, ambiguous, or not famous enough. Not used:
cast, crew, dates and exact counts. A stem may mention something another question also
mentions (for example the mice in the Rescuers), but no pair asks the same fact.
Film-title giveaways were dropped (The Nightmare Before Christmas and Christmas;
Maleficent's kiss; The Princess and the Frog and the frog).

The walt and cruise shares are small on purpose: their famous facts are already asked,
several as retired duplicates, and padding with obscure ones would defeat the label.

## Evidence

- Pages were fetched with curl on 2026-11-25: D23, Wikipedia, dialogue transcripts and
  official Disney pages. The passage for each correct answer was read in that text.
  `generation-0005-rows.json` keeps the pattern that matched, and the build stops on a miss.
- Distractors are excluded by inference from the stated fact (`exclusive-inference`) or by
  the role they hold elsewhere in the film. No film viewing is claimed. Film-to-film
  context in distractor reasons (e.g. a locket belonging to the sequel's Melody) is general knowledge.
- Transcript URLs are in the ledger only; those questions carry an explanation without a
  player-facing `source`.
- Fifteen park, cruise and walt facts are standing features with stable rechecks, the rest are historical or
  anchored to a date.
- 61 automated duplicate findings, all read and accepted: same answer with a different
  subject, or similar wording with a different answer.

## Daily cap and simulation

`NEW_QUESTION_MAX_ID` (2995) bounds the v1.59 cap. With the live `meta/dailyHistory`
(read-only, 181 days), simulated dailies from 2026-11-27 took:

| Days | New batch per day | Max | Paced 2656-2995 per day | Repeats |
| ---: | ---: | ---: | ---: | ---: |
| 30 | 1.33 | 2 | 0.93 (max 1) | 0 |
| 90 | 1.16 | 2 | 0.98 (max 1) | 0 |
| 180 | 0.86 | 2 | 0.96 (max 1) | 0 |

The mix stayed 2/5/3 every day, so no extra pacing was needed.

## Second pass

Before release: marigold bridge (Coco) moved to `pixar`; Dug's greeting checked against a
second source and restored to "I have just met you"; Jiminy's line cited to his song;
Helen Parr restemmed as Violet and Dash's mother; Savi's given a recheck; Tigger's options
made parallel. "What does Alice fall down" was replaced (guessable from the White Rabbit
question), and the weakest park item (clamshell vehicles) was replaced.
Five items cut earlier were restored to reach 200: army men, Bob at home (Incredibles 2),
penguin waiters, Ariel's hair and celebration buttons, plus the two replacements above.
