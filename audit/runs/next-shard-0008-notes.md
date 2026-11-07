# Batch 8: complete for scope

Reviewer: Codex. Ledger date: 2026-11-07 (UTC; the session began November 6 in Toronto).

Fixed scope: the 50 planned IDs in `next-shard-0008-plan.json`, from physical
shard `questions/q-002.json`. The full cruise, parks, walt and Snow White topic
digests, complete ranked comparisons and additional cross-bank searches were
read. Context questions were not added to this content audit. Final edits and
fresh comparison findings were rechecked against that context.

- Reviewed: 50; retained with current schema-2 evidence: 30; approved: 30.
- Retained edits: 21; duplicate retirements: 20; unresolved in scope: 0.
- Overlapping change types: factual 2, clarification 19, distractors 10,
  difficulty 1; explanation/category/scope/metadata 0.
- The factual wording corrections are 368 (tower atrium/concourse rather than
  check-in lobby) and 371 (the 1999 show was not EPCOT's original lagoon show).
  Most edits do not mean the old keyed answer was false.
- Structural validation: 1,953 active questions, zero errors.
- Current approval: q-002 is 110/194; the whole bank is 312/1,953.
- Next request: batch 9, continuing q-002 after question 425. The status preview
  did not create the next plan.

## Evidence

`next-shard-0008-evidence-notes.json` contains concise explicit premise and
four-option assessments, all eight performed manual checks and the separate
Codex challenge of each retained question's final wording. Those notes expand
to `next-shard-0008-reviews.json`; all 30 were validated and imported atomically
with `record-many`. The inspected reusable passages are in
`audit/source-notes.json`; neither expansion nor structural validation proves
source support. No film/video viewing is claimed from an indexed title.

Historical dates, exceptional firsts and the Treasure count were corroborated.
Mutable venue/policy records have a 2027-02-05 recheck. The Snow White evidence
distinguishes tracing reference footage from mechanically copying an entire
finished performance. The overlapping live-reference distractor was replaced.
The club questions explicitly ask the full age band because Edge and Vibe both
include age 14. The dining count is limited to the Wish's three main venues.

`next-shard-0008-comparisons.json` preserves fresh full-option comparisons.
Ten remaining duplicate warnings were accepted individually as different facts,
including distinct restaurants, separate entities named Treasure Island, and
unrelated numeric counts. The old 397 answer-length warning and a new 414 salon
word-overlap warning were each recorded unresolved, corrected, re-reviewed and
then marked fixed after they stopped reproducing.

## Retirements

Twenty original snapshots were preserved using `retire`, with complete
counterparts, source passages, all four original-option assessments and specific
challenges in `next-shard-0008-retirements/`. The retirement script calls only the
supported command and does not directly edit shards. No IDs were reused.

| Retired | Retained counterpart | Repeated fact or concern |
| --- | --- | --- |
| 373 | 2631 | Named PeopleMover association already supplied by the motor question. |
| 377 | 2249 | 2023 Magic Kingdom TRON opening is already stated in the origin-park question. |
| 378 | 1172 | Same Matterhorn coaster identity; original also repeats its name. |
| 379 | 1177 | Same studio name; first-studio premise ignores earlier Kansas City work. |
| 382 | 131 | California move is supplied more precisely by Hollywood location. |
| 385 | 1372 | Same wife's name. |
| 386 | 127 | Daughters question already supplies two and asks their names. |
| 388 | 1490 | Same Roy O. brother identity with additional leadership context retained. |
| 390 | 946 | Nature-film series name already given by the first-feature question. |
| 391 | 1379 | Same Johnson/1964/Medal of Freedom event in reverse. |
| 395 | 960 | Same Nine Old Men identity with actual members retained. |
| 399 | 1495 | Same multiplane depth fact in reverse; parallax distractor overlaps. |
| 400 | 690 | Same Burbank/1940 fact, also stated by 959. |
| 401 | 1191 | Same WDI identity; WED alternative is a genuine historical name. |
| 403 | 677 | Same Laugh-O-Gram/Kansas City association, also stated by 1492. |
| 411 | 136 | Aggregates original ship identities from 136 and 961; primary pointer is 136. |
| 417 | 2274 | Theatre identity supplied in the retained musical/ship question. |
| 419 | 434 | Pirate Night supplied in the question about its fireworks title. |
| 421 | 750 | Same outdoor movie screen identity. |
| 422 | 729 | Same Wish/2022 debut fact in reverse. |

Comparing a counterpart does not approve its unrelated claims. In particular,
ambiguous original premises/options on 379, 399 and 401 are explicitly disclosed
in their records; retirement does not claim single-answer verification of them.

## Player reports and broader gate

Fresh read-only snapshot: `artifacts/question-audit/batch-8-player-flags.json`.
Eleven documents, no further page token. Reports on 386 and 412 fall in scope and
were already marked resolved in production. The historical 386 report concerned
names formerly added to its count answer. The 412 report distinguishes five ships
before Treasure from six including Treasure. Final wording explicitly includes
Treasure and the December 2024 maiden-voyage cutoff. Investor commentary calls it
the sixth ship; the official fleet table lists all six.

The overall audit gate has one error: `manual-b5f7a15848ac7596a72e`, newly tracked
on out-of-scope question 1374 during its comparison with 381. The 1954 anthology
TV question calls the program an early color program; the inspected D23 biography
dates Wonderful World of Color to 1961. Its TV scope also needs review. This is a
context-only concern, not a completed audit or content edit of 1374. It does not
leave an in-scope finding open, but it blocks release until separately addressed.
The remaining 1,641 unverified active questions remain the disclosed legacy backlog.

`next-shard-0008-result.json` records complete-for-scope closure. No production
flag mutation, publication, commit or push occurred. Existing unrelated working
tree changes were preserved.
