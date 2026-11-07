# Batch 9 audit handoff

Reviewer: Codex. Recorded date: 2026-11-07 (UTC audit-tool date).
Fixed scope: the 50 IDs in `next-shard-0009-plan.json`, all from `questions/q-002.json`.

Closed **complete-for-scope** in `next-shard-0009-result.json`:

- 50 reviewed: 35 retained with current schema-2 four-option evidence and final challenges, plus 15 documented duplicate retirements.
- 35 evidence-recorded, source-verified and approved; 15 retained questions edited; zero unresolved questions in scope.
- Overlapping retained-edit classifications: factual 5; clarification 11; distractors 6; difficulty 4. Explanation, category, scope and metadata: zero.
- Five factual fixes: q432 hull/funnel colors; q461 second valid songwriter option; q468 lyricist versus composer; q472 Luca's already-known species; q480 false monocle condition.
- q452's overclaim of an entire soundtrack by Phil Collins was removed through duplicate retirement, not counted as a retained factual edit. Its comparison preserves the distinction between Collins songs and Mancina score.

Read the complete topic catalog, all four answer options and ranked comparisons. Searched the whole bank for missing character/song context. Research used official Disney/Pixar material, the Academy, songwriters' and production vendors' own credits, and a shipbuilder's design history. Limitations for third-party-hosted primary material and corroborating secondary text are recorded in source notes. No film/video playback is claimed. Reusable passages are in `audit/source-notes.json`; explicit notes and expanded evidence are in `next-shard-0009-evidence-notes.json` and `next-shard-0009-reviews.json`.

Retired IDs: 437, 439, 440, 442, 443, 444, 445, 449, 452, 454, 464, 465, 467, 475, 476. The supported retirement command preserved their snapshots and evidence histories. Comparisons are in `next-shard-0009-comparisons.json`; final applicable finding decisions are in `next-shard-0009-finding-decisions.json`.

Player reports were read into `artifacts/question-audit/batch-9-player-flags.json`. The q476 spelling report was already resolved; current Forky spelling agrees with Pixar. No production report was changed.

Validation: corpus structural validation passed for 1,938 active questions; review expansion and bulk import passed; batch closure passed. The whole-bank release gate still fails on the pre-existing out-of-scope manual concern for **q1374**, `manual-b5f7a15848ac7596a72e`, concerning 1954 versus 1961 color-television wording and real-TV-show scope. It was recorded during batch 8 and remains unresolved. No release was requested or performed.

Final active coverage: q-002 is **145/179 approved**, with 34 remaining; the bank is **347/1,938 approved**, with 1,591 remaining. The next request selects batch 10, the final 34 questions in q-002. Only previewed that selection; no new batch was started. Mutable cruise sources have a 2027-02-05 recheck.
