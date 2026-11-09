# Batch 31 content audit

Reviewer: Codex. Content/source review performed November 8, 2026 (America/Toronto).
The queue tool's UTC date on generated plan/result/classification records is November 9.
Fixed scope: `questions/q-007.json`, #2068–#2117, 50 planned questions.

## Result

Complete for scope: 50 reviewed, 48 evidence-recorded, 48 approved, 31 retained
questions edited, 2 duplicate questions retired, 0 unresolved questions/findings.
Every retained question has four option rationales, premise evidence, editorial
checks and a separately recorded final evidence challenge on its final wording.

Change types overlap: factual 3; clarification 31; distractors 19; difficulty 6;
explanation/category/scope/metadata 0. An edited question is not necessarily a
factual error.

Confirmed factual corrections:

- #2076: changed “each sneeze” to “repeatedly”; the final alphorn sneeze produces
  a giant snowball, so the original universal claim was too broad.
- #2093: Ranjan is Mowgli's adoptive little brother, not Shanti's brother.
- #2111: Mary participates in the floating tea party without laughing herself
  into the air. Removed that false shared trigger and supplied parallel groups.

Other notable repairs: combined overlapping Bell System/AT&T sponsor answers
(#2085); removed song-title paraphrase clues (#2074/#2075), the Bao answer's
parenthetical giveaway (#2080), and the band-name clue (#2107); made Tod's
false-claim question match its answers (#2109). Narrowed speculative or excessive
claims about boat sinking, multiple evacuations, costume disguises, physical
weakness, top-student rankings, race-footage provenance and an all-purpose travel
spell. The current Wish lounge fact #2090 has a February 5, 2027 recheck; #2091
now explicitly asks about the documented 2025 show.

## Duplicate and source review

Preserved original snapshots and retirement decisions:

- #2079 → #2327: the broader Piper fear question repeats the hermit-crab learning
  episode tested more precisely by the retained wave-survival technique question.
- #2099 → #2200: the retained youth-potion question names Yzma and supplies the
  partnership-identity answer asked by the removed question.

Full comparisons are in the two `next-shard-0031-comparison-*.json` files.
Topic digests and additional whole-bank shared-answer/stem comparisons were
considered. The accepted #169/#2087 shared-year comparison remains distinct
(Oscar ceremony versus labor strike). #42/#2094 remains distinct because the
sequel revenge motive separates Shere Khan from the also-returning antagonist Kaa.
Different Genie rules, band-member instrument assignments, song scenes and
sequel production/character facts were not merged simply for sharing a title.

Explicit source notes and per-option rationales are in
`next-shard-0031-reviewed-notes.json`; expanded snapshots and verification records
are in `next-shard-0031-reviews.json`. Reusable passages were added to
`audit/source-notes.json`. Sources include Disney/Pixar pages, official park and
district history, the Animation Guild, AFI, film-composer soundtrack credits and
identified secondary plot/transcript corroboration where official text omits
detail. No original film, audio or video viewing is claimed. Blocked source
routes were not treated as supporting evidence.

## Player reports and validation

Read-only live flag export: `artifacts/question-audit/batch-31-player-flags.json`.
All 13 records fit one response; six are pending. The in-scope pending report is
#2080's parenthetical giveaway, addressed locally by this batch. It remains open
in production until publication; no player-report resolution or production
write was performed. The other pending reports are outside this fixed scope.

Structural validation: 1,859 active questions, zero errors.
Audit gate: zero errors; 530 active questions remain in the disclosed source
verification backlog. The close command reports `complete-for-scope`.
A transient Windows ledger replacement lock during classification was retried
successfully; all 31 retained edits have current hash-bound classifications.

Progress: q-007 is 96/246 approved; the whole bank is 1,329/1,859 approved.
The next request resumes with batch 32 in q-007, beginning at #2118.
Changes remain local and unpublished.
