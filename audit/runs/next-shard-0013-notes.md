# Batch 13 — complete for scope

Reviewer: Codex, 2026-11-07. Fixed scope: 50 planned questions in
`questions/q-003.json`, #697 through #775 (manifest/file order, with ID gaps).

## Result

- Reviewed: 50, including three explicit duplicate retirement comparisons.
- Evidence recorded / source verified / approved: 47 retained questions.
- Edited: 31 retained questions; retired: 3; unresolved in scope: 0.
- Change types overlap: factual 7, clarification 31, distractors 8, difficulty 13.
  Explanation, category, scope and metadata edits: 0.
- Retired #697 to #438, #710 to #1383, and #717 to #169. Original snapshots,
  ledger history and explicit comparisons are preserved.
- Current shard: 134/172 active approved. Whole bank: 513/1,920 active approved;
  1,407 remain. Next request starts batch 14 at #776, covering the final 38
  outstanding questions in q-003. Preview only; batch 14 was not created.

## Findings and changes

- #708: corrected the ambiguous unique-highest chart claim. Both Bruno and
  A Whole New World reached No. 1; the final question asks the specific 2022
  first-since-1993 event. The current player flag from Milo says “Are you sure?”;
  it remains open because this content has not been published.
- #704: removed the claim that Ariel is physically alone during her solo.
- #705: narrowed the household-objects song question to the elaborate dinner
  presentation; several original alternatives also feature enchanted servants.
- #724: corrected the chores premise to Cinderella's early bedroom song.
- #739: replaced unsupported Dole Whip availability with positively documented
  soft-serve machines. No blanket claim of Dole Whip absence is made.
- #750: replaced the unsupported Movies Under the Stars proper-title construction
  with the documented Funnel Vision screen name on Disney Fantasy.
- #758: removed the descriptive Forest People synonym and shared trapped-in-forest
  condition; Yelana's leadership uniquely identifies Northuldra.
- Other edits specify original films, English vocals, historical maiden voyages,
  exact song scenes, plausible parallel alternatives and recall difficulty.
- #746 received a separate final challenge and renewed review after initial closure:
  the final question asks which named island area contains submerged statues. This
  avoids assuming that one statue photo excludes every other underwater object.
  The earlier completed result was archived automatically on renewed closure.

Read all complete topic contexts once, deduplicated by question ID, including full
music, cruise and parks categories and the matching film topics; searched all
shards for relevant character names and related facts. Considered ranked comparisons
and all final applicable findings. Thirteen warnings were individually accepted
with specific distinctions or an authentic song-title-length rationale. They are
saved in `next-shard-0013-finding-decisions.json`.

Evidence notes and expanded reviews are saved separately from the regenerable
packet. Primary Disney, creator, Academy and Pixar text was preferred. Detailed
secondary song/scene analysis and a primary concept-art catalogue were used where
official text did not establish the scene. Access limits and corroboration are
recorded in source notes. No film or video playback is claimed. Current offerings
have a 2027-02-05 recheck date. Sources with unrelated mistakes (Menken's Mermaid
page header year and the Fantasy guide's introduction year) were not used for dates.

The read-only player-flag snapshot contains 12 documents with no pagination token:
`artifacts/question-audit/batch-13-player-flags.json`. No production flag was resolved.

## Validation and release boundary

`python scripts/validate_corpus.py` passes: 1,920 active questions, nine shards,
zero structural errors. Review expansion, atomic imports and final closure pass.
The result is `next-shard-0013-result.json`, marked `complete-for-scope`.

The overall audit gate still reports two previously recorded concerns outside this
batch: #1374 (television/color/scope) and #1492 (Laugh-O-gram founding date).
No commit, push or deployment was requested or performed.

## Learning-fact follow-up

The owner's screenshot showed #1397's existing `explanation` and `source` fields.
Git history attributes that explanation to earlier fix commit `c9fe223`, preceding
the sequential batches. Only seven active questions currently have player-facing
explanations. None of this batch had an explanation, and this audit added none.
Private four-option evidence records are separate from player-facing learning facts.
