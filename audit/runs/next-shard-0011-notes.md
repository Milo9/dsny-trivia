# Batch 11 — complete for scope

Reviewer: Codex. Audit record date: 2026-11-07 (the audit CLI's date).
Fixed scope: the 50 IDs in `next-shard-0011-plan.json`, physical shard
`questions/q-003.json`. No publication was requested or performed.

50 reviewed; 49 active with current schema-2 evidence, final challenge and approval;
26 retained edits; one preserved duplicate retirement (506 → 10); zero unresolved
questions/findings within scope. Change types overlap: factual 2, clarification 26,
distractors 10, difficulty 8, category 1, scope 1; explanation/metadata 0.

The factual changes clarify that Alice's card gardeners conceal their mistake
rather than paint at the Queen's request, and anchor Soarin' Around the World to
its 2016 debut because the current official page offers Across America instead.
Other changes narrow context, improve options, remove answer clues, calibrate
difficulty, or move cave trivia into movies. They are not 26 factual errors.

Evidence is in `next-shard-0011-evidence-notes.json` and the expanded
`next-shard-0011-reviews.json`. Sources include specific Disney Archives entries,
official character/film/park descriptions, Wish production notes and corroborated
scene passages. Secondary transcript/academic/artifact evidence and unavailable
video playback are explicitly disclosed per source; indexed official clip titles
are only corroboration, not a claim to have watched those clips. Named identity
and species exclusions are exclusive inferences, not claims that short synopses
prove the absence of every possible action or power.

The full combined topic context was read once, with overlapping IDs deduplicated,
and followed by whole-bank keyword searching. `next-shard-0011-comparisons.json`
preserves full question/options for applicable finding decisions, the retirement,
and the final focused Tangled/Raya comparisons. Sources and comparisons were
challenged against final wording before importing reviews. Retired question 506
preserves the original snapshot exactly; earlier approved q10 is retained.

Player flags were fetched read-only into
`artifacts/question-audit/batch-11-player-flags.json`; none concern this fixed
scope. No player report was resolved or modified.

Validation: `python scripts/validate_corpus.py` reports 1,936 active questions,
zero structural errors. Sync/report and complete closure succeeded. The release
gate has one pre-existing unresolved manual finding for q1374 (1954 television
color chronology and real-TV scope), discovered during batch 8; it is outside
this plan and remains unresolved. No runtime behavior was changed.

Progress: q-003 is 50/188 approved (26.6%); whole bank 429/1,936 approved (22.2%),
1,507 remain. The next request starts batch 12 in q-003, beginning with q599.
Tree of Life's current-name review is scheduled for 2027-02-04. The Soarin'
question is now historical rather than dependent on current availability.
