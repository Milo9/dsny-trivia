# Sequential audit batch 25

Reviewer: Codex. Date: 2026-11-08. Status: **complete-for-scope**.

Fixed scope: 50 planned questions in `questions/q-006.json`, #1302–#1380
(manifest order, with gaps). Reviewed 50; evidence recorded, source verified and
approved 49 retained questions; edited 35; retired 1; unresolved 0.

Change types overlap: factual 4, clarification 35, distractors 13, difficulty 6.
Explanation, category, scope and metadata changes: 0. Edited is not a count of
factually wrong questions.

The factual corrections concern Fergus's misleading bear-loving description
(#1308), invented musician occupations in the Soul options (#1316), the parents'
waiting location in Finding Dory (#1317), and attributing Dumbo's final
feather-free reassurance to the crows rather than Timothy (#1336). Other edits
clarify context, remove unsupported embellishments or answer-word clues, improve
parallel options, and calibrate difficulty.

Retirement: #1326 -> #1103. Both test the Mad Hatter/March Hare tea-party host
pairing. The original snapshot, ledger history, replacement snapshot and explicit
comparison are preserved. The Dormouse's presence does not make any alternative
pair valid, nor does the unbirthday setting introduce a new requested fact.

Sabor research revealed inconsistent institutional species descriptions: the
[Disney A to Z film entry](https://d23.com/a-to-z/tarzan-film/) says leopard,
while a [2022 promotional article](https://d23.com/5-fantastic-things-to-watch-this-weekend-presented-by-state-farm-061622/)
says jaguar. #1338 now asks the predator's name, established as Sabor, avoiding
the disputed label entirely. This question concerns the parents' deaths in 1999's
Tarzan, not the separate Tarzan II chase in #2197.

Read the complete matching topic context, including the broad characters,
movies, parks and Walt digests, and the film-specific Pixar comparisons. Renewed
three fresh duplicate decisions as distinct facts: Joy/Belle colors, Animal
Kingdom/Pandora openings, and Haunted Mansion/Space Mountain opening years.
Accepted the necessary presidents subject vocabulary in #1355. The prior
Louis-cook/Louis-alligator distinct-fact decision remains current.

Sources and all four final options were evaluated explicitly, followed by a
separate literal-wording challenge. Primary institutional profiles, park pages,
operator history and the Johnson ceremony transcript were preferred. Where
needed, detailed film dialogue transcriptions, secondary plot/cast descriptions,
a contemporary Brian Sibley review, and design-history accounts were used with
their limitations recorded. No film or video playback is claimed. Weenie usage
is supported by accounts quoting/locating John Hench; the original book was not
accessed, and invention priority was removed from the question.

Evidence: `next-shard-0025-final-notes.json`, `next-shard-0025-reviews.json`,
the comparison file, and new reusable `b25-*` entries in `audit/source-notes.json`.
The authoring file preserves the concise explicit assessments; it does not edit
question shards. Four current park facts have scheduled rechecks by February
4–6, 2027. Historical festival wording is bounded to spring 2026.

Live flags were read and saved to the ignored artifact
`artifacts/question-audit/batch-25-player-flags.json`; none concern this batch.
No flag was changed. The first network attempt failed DNS resolution; the
authorized read succeeded on retry. A transient Windows atomic-save file lock
interrupted classification once; the affected operation and remaining
classifications succeeded on retry, with final complete closure confirming no
missing classifications.

Validation: corpus structural validation, sync/report, validated bulk evidence
import, and audit gate passed. Gate: zero errors, with 826 active questions still
awaiting current source verification. `git diff --check` passed.

Progress: q-006 is 51/247 approved; whole bank 1,046/1,872 approved. Next request
starts batch 26 in q-006, beginning at #1381. Only batch 25 was created and
completed; the next batch was previewed without creating its plan.

No publication, deployment or commit. Pre-existing `APP_AUDIT.md` deletion and
untracked `debug.log` were preserved.
