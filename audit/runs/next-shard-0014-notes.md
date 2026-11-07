# Sequential content audit: batch 14

Reviewed by Codex on 2026-11-07. Fixed scope: the final 38 queued questions in
`questions/q-003.json`, as saved in `next-shard-0014-plan.json`.

Result: **complete-for-scope**. Reviewed 38; current four-option evidence recorded
and approved for 32 retained questions; edited 18; retired 6; unresolved 0.
Classification counts overlap: factual 1, clarification 18, distractors 5,
difficulty 1; explanation/category/scope/metadata 0.

The authoritative filled notes are `next-shard-0014-reviewed-notes.json`, expanded
into `next-shard-0014-reviews.json` and imported with `record-many`. The earlier
`*-evidence-notes.json` and `*-final-evidence-notes.json` files are unused blank
authoring templates, not completed evidence. Reusable inspected passages were
added to `audit/source-notes.json`; evidence limitations are embedded in reviews.

## Changes

- #799: removed the misleading premise that Enchante replaced Remy aboard Wish.
  The two are on different ships; Remy is a strong distractor because its menu
  also involves Arnaud Lallement. Explicit ship lists were checked.
- #784: removed the overlapping amnesia option and grounded alternatives in the
  distinct official Dory, Destiny, Bailey and Hank descriptions.
- #555: specified visiting suitor clans, because Merida enters for DunBroch
  herself. Distractors now differ by one plausible clan.
- Removed answer echoes in #778, #503, #508, #513, #540 and #548; clarified exact
  versions, performance context, operational date or roles elsewhere. #783's
  basic lead-character recall was calibrated to easy.
- Kept #552 and #554: Fantasy/Royal Court and Dream/Royal Palace are separate
  ship-to-venue facts. Tightened the theme to Disney Princess films to distinguish
  Enchanted Garden's real-world Versailles inspiration.

## Preserved retirements

| Retired | Retained | Tested overlap |
| --- | --- | --- |
| 787 | 1487 | Walt's Red Cross ambulance service |
| 791 | 2466 | Collins's authorship of the original Tarzan songs |
| 793 | 1382 | Just Around the Riverbend / Pocahontas association |
| 794 | 1504 | Coco's Oscar-winning Lopez song |
| 796 | 412 | Treasure's December 2024 maiden voyage, already explicit in #412 |
| 798 | 964 | AquaDunk / Disney Magic association |

Full question/option comparisons, evidence locators and challenges are saved in
the six `next-shard-0014-comparison-*-*.json` files. The supported `retire` command
preserved original snapshots in `questions/retired.json` and retained ledger
history. #791 also overstates Collins's in-film singing: Disney identifies five
songs written, four sung by Collins. #793's canoe-race detail was not established
by consulted textual evidence; the cleaner retained association avoids it.

## Evidence and findings

Read the complete combined category context and matching topic/comparison context,
including all four answers. Compared the final wording against related questions.
Accepted the canonical-title length finding for #792 and distinct-fact comparisons
for #256/#531, #329/#531 and #552/#554. None remains unresolved in this scope.

Most evidence is Disney, Pixar, the original songwriters, the Academy, or the Walt
Disney Family Museum. The exact Chicha family relationship, Atlantis ensemble
roles, Brave suitor context and Simba/Zazu scene also use explicitly disclosed
secondary corroboration. No review claims original-film or video playback.
Changing operational facts have rechecks scheduled for 2027-02-05.

Read current production player flags and saved
`artifacts/question-audit/batch-14-player-flags.json`: 13 records, no pagination,
none on an in-scope question. No flag state was changed. #412's historical flag
was already resolved and its current question has existing supporting evidence.

## Validation and progress

- Structural validation: 1,914 active questions, zero errors.
- Audit gate: zero errors; 1,367 active questions remain without current source
  verification. This is not whole-bank factual approval.
- `git diff --check`: passed.
- Closed the saved plan to `next-shard-0014-result.json` with reviewer Codex.
- Physical shard: `q-003.json` is 166/166 approved.
- Whole bank: 547/1,914 approved.
- Next request: batch 15, first 50 queued questions in `q-004.json`, starting #801.
  No batch 15 plan was created.

No publication, commit or deployment was requested or performed. Existing
unrelated worktree items, including the deleted APP_AUDIT.md, were preserved.
