# Batch 28 — complete for scope

Reviewer: Codex. Date: 2026-11-08. Fixed scope: the 50 planned questions in
`questions/q-006.json`, #1538 through #1595 with ID gaps. No publication requested
or performed. Existing unrelated worktree changes were preserved.

## Result

- Reviewed: 50; current evidence recorded: 50; source verified: 50; approved: 50.
- Edited retained questions: 28; retired: 0; unresolved within scope: 0.
- Overlapping change types: factual 8, clarification 28, distractors 13,
  difficulty 4, category 1, metadata 1; explanation and scope 0.
- Physical shard: 197/243 approved, 46 remaining.
- Whole active bank: 1,192/1,868 approved, 676 remaining.
- Next request: batch 29, beginning #1596, the final 46 questions of q-006.

The factual labels apply to #1545 (invented award premise), #1546 (false plaque
claim), #1566 (glass repair timing and city-saving overclaim), #1573 (screen
broadcast versus wearable goggles), #1574 (invented memory restoration), #1576
(world summit versus signing ceremony), #1578 (Dez's job), and #1579 (Roz's job).
The other edits clarify context, remove unsupported extra clauses, fix ambiguous
options, improve parallelism, or calibrate difficulty; edited does not mean
factually wrong. In particular, #1595 previously offered Cornelius and Wilbur's
father as separate answers even though both describe Lewis's adult identity.
#1578 also replaced the broad distractor doctor with physician because a
veterinarian is a doctor.

## Evidence and distinctness

`next-shard-0028-reviewed-notes.json` contains explicit premise support, all four
option assessments and a separate final challenge for every final question.
`next-shard-0028-reviews.json` contains the expanded schema-2 records imported
with `record-many`. Forty-seven passage-specific reusable source notes were
added to `audit/source-notes.json`. Primary Disney/Pixar profiles, studio
screenplays and historical institutional records were preferred. Where no
specific primary passage was available, the records identify the secondary
transcripts/plot accounts and corroboration rather than claiming film viewing.
No film, audio or video playback was performed.

Complete category digests (351 character, 444 movie, 296 Pixar, 171 Walt records)
and additional records in the named topic digests were read with all four
answers. Relevant final wording was compared with that context. The Onward
mother/partner comparison is saved in `next-shard-0028-comparisons.json`:
Laurel's name and Colt's name are distinct tested facts, so both were retained.
Existing accepted comparisons involving Anna and Friar Tuck remain valid.
The Soul title-word leak is an accepted false positive: it gives no information
about the two bodies. The flea and chasm stem giveaways were removed and no
longer reproduce. No duplicate removal was warranted.

## Verification and follow-up

Structural validation via `sync`/`report` passed after each content-edit group
and after the final classifications: 1,868 questions, nine shards, zero errors.
Bulk evidence validation/import passed. All 28 retained edits have current
hash-bound classifications. `close` produced the complete-for-scope result at
`next-shard-0028-result.json`; read-only `status` previews batch 29.

The release gate was run and reports one error, outside this batch:
`manual-eb23fdafcc14c37947f9`, question #1602. Its stem places Anna's *The Next
Right Thing* before Olaf's condition worsens, while the inspected farewell and
song sequence puts the song after his disappearance. This was discovered in
full Frozen context, recorded as a concern, and left unchanged to preserve the
fixed batch scope. Next-batch review should inspect the sequence and repair the
timing. Evidence route:
https://www.springfieldspringfield.co.uk/movie_script.php?movie=frozen-ii,
lines 1202–1230 and following song, corroborated by the Frozen 2 plot sequence.
The remaining legacy backlog is disclosed; the release gate is not passing.

A classification-command handling mistake caused overlapping helper runs and a
Windows temporary-file collision. After both processes ended, the ledger
contained a complete valid JSON object followed by 121 stray trailing
characters. The original bytes were preserved at
`artifacts/question-audit/next-shard-0028-ledger-recovery-original.txt`; only the
trailing characters were removed. All 50 current reviews, prior 1,142 approvals,
the two warning decisions, the #1602 concern, and all 28 final classifications
were subsequently checked through successful structural/report/closure/status
commands. Classification work completed sequentially. No audit history was
intentionally discarded.
