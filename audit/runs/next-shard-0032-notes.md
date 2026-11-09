# Sequential content audit — batch 32

Reviewer: Codex. Review date: November 8, 2026 (America/Toronto).
The audit CLI's host-date metadata uses November 9; the source and challenge notes retain the client review date.

Fixed scope: `questions/q-007.json`, IDs 2118–2167, 50 questions.
Result: **complete-for-scope** in `next-shard-0032-result.json`.

- Reviewed: 50; current evidence recorded: 50; approved: 50.
- Edited retained questions: 37; retired: 0; unresolved questions: 0.
- Overlapping classifications: factual 7, clarification 37, distractors 14,
  difficulty 2, category 2, scope 1; explanation and metadata 0.
- Thirteen questions retained unchanged. Editing does not imply a factual error.

## Material findings

- #2127–2128: cave entry qualification is separate from the prohibition on taking
  treasure. The original burial-alive claim was replaced with Abu's ruby-triggered
  lava/collapse scene; the characters survive.
- #2129: the sisters initially believe they lack traditions; the ending establishes
  that Olaf already is their tradition. The final wording asks about their belief.
- #2134: the Pascal snake incident is television-series material, misattributed to
  the theatrical film. Replaced it with Flynn's revival by Rapunzel's tear, with
  primary participant commentary from Glen Keane supporting the final question.
- #2140: Thumper recites his father's advice at his mother's prompting; the father
  is not the on-screen speaker. The final wording asks whose advice it is.
- #2153: the original answer, two replacement heads, confuses the myth with the
  Disney scene. Three heads emerge after the original head is cut off. Restricted
  wording to the first regrowth, with four numerical options. This remains distinct
  from #829, which asks for the monster's identity.
- #2159: replaced motion-capture/MIDI wording with Disney's documented filmed hand
  reference for frame-by-frame animation.
- #2121: replaced an undated inflation-adjusted loss estimate with the documented
  working title. #2155 now asks the approximate nominal 1981 budget, avoiding a
  broad historical-record assertion and misleading alternative record claims.
- Other edits remove clues, unneeded superlatives, context ambiguity and uneven
  answer wording. #2150 moves to music; #2134 moves to movies/medium; #2141 to easy.

## Evidence and distinctness

`next-shard-0032-reviewed-notes.json` contains the concise completed reviews;
`next-shard-0032-reviews.json` contains their schema-2 expansion. All four options,
premises, locators, manual attestations and separate final challenges are recorded.
The import was validated and recorded with `record-many`.

Evaluated 54 specifically located source passages, using Disney/Pixar production
notes, institutional histories, official character profiles and participant
interviews where available. Secondary scene transcriptions and historical accounts
are explicitly identified, with corroboration and limitations. No original film,
audio or video playback is claimed. In particular, the Hydra count uses two detailed
secondary scene accounts; the fawn destination uses independent named historians;
the approximate Fox/Hound budget has secondary corroboration rather than an
accessible original studio cost ledger.

Topic digests, all-four-option comparisons and additional cross-bank searches were
used as duplicate context. No out-of-scope question was edited. The eight final
applicable warnings were accepted with specific reasons and complete compared
question snapshots in `next-shard-0032-comparisons.json`. Shared numbers are
unrelated facts; the two Soul cast questions ask separate assignments; piano hand
reference differs from an Oscar credit. There were no duplicate retirements.

## Player reports and checks

Read-only live export: `artifacts/question-audit/batch-32-player-flags.json`.
Thirteen report documents, with no pagination remaining. Unresolved report IDs
reference questions 911 (twice), 2432, 2080, 708 and 138; none concerns this batch.
No production flag was resolved or modified. The live export was retrieved after
content review; the initial sandbox DNS attempt failed and the read-only retry
succeeded. A transient Windows ledger replacement lock interrupted classification;
retries completed it without dropping records.

`validate_corpus.py`: 1,859 active questions, 0 structural errors.
Audit report regenerated after content fixes; final audit gate: 0 errors.
Plan closure succeeded: 50 approved, 0 unresolved. No runtime change or release
was performed, and no publication was requested.

Final progress: **146/246** approved in q-007; **1,379/1,859** across the active bank;
480 remain. The next request resumes batch 33 in q-007 beginning at **#2168**.
