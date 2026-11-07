# Batch 12 — complete for scope

Reviewer: Codex. Audit record date: 2026-11-07.

Fixed scope: the 50 IDs in `next-shard-0012-plan.json`, in `questions/q-003.json`.
Read the complete deduplicated topic catalogs and ranked comparisons, then searched
the bank for relevant identities and associations. Research used Disney/Pixar
character profiles, Disney park and archive materials, official awards records,
the Walt Disney Family Museum, and PBS documentary research. Source limitations
and the separate final wording challenges are in the saved evidence notes.

- Reviewed: 50; current evidence recorded/source verified/approved: 37 each.
- Retained edits: 24; preserved duplicate retirements: 13.
- Unresolved within batch: 0; unclassified edits: 0.
- Change types overlap: factual 3, clarification 19, distractors 12, difficulty 11;
  explanation/category/scope/metadata 0 each. Edited does not mean factually wrong.

Main corrections: scream energy rather than ordinary electricity and overlapping
powered systems; D23's first Hollywood studio rather than first-ever studio;
Project X was another true planning name, so it could not remain a distractor.
Other edits narrow context, eliminate giveaways or overlapping options, and
calibrate named-character recall difficulty.

Retirements: 605, 607, 635, 665, 668, 677, 678, 679, 685, 686, 690, 691, 696.
Exact snapshots and histories are preserved by the supported retire command.
`next-shard-0012-comparisons.json` documents the comparisons. In particular,
retaining replacement #1492 does not approve its 1921 founding-date claim:
museum evidence gives spring 1922, recorded as an unresolved related concern.
The replacement's content was left for its own queued audit.

Player flags were fetched read-only (11 documents, no pagination token and no
batch-12 IDs); snapshot: `artifacts/question-audit/batch-12-player-flags.json`.
No production flag was resolved.

Validation: `python scripts/validate_corpus.py` passed; sync and report refreshed;
37 schema-2 reviews built and imported atomically with record-many. Eight fresh
applicable findings were explicitly accepted after comparison. Batch close
succeeded as complete-for-scope. The whole-bank gate still reports two manual
concerns outside this batch, #1374 (existing television/color/scope issue) and
#1492 (new founding-date concern). No release was requested or performed.

Current active shard progress: 87/175 approved, 88 remaining.
Current active whole-bank progress: 466/1,923 approved, 1,457 remaining.
Next request starts batch 13 in q-003.json; no next plan was created.

Saved artifacts: `next-shard-0012-evidence-notes.json`,
`next-shard-0012-reviews.json`, `next-shard-0012-finding-decisions.json`, and
`next-shard-0012-result.json`.
