# Audit records

Follow [QUESTION_AUDIT.md](../QUESTION_AUDIT.md) for the authoritative procedure.
Dates in the ledger and reports use UTC.

Default authoring workflow: [EFFICIENT_WORKFLOW.md](EFFICIENT_WORKFLOW.md).
`next` also writes a deduplicated `current-compact.json` reading view. Use `view`
for complete merged topic context, `sources` to search `source-notes.json`, and
`notes-template` / `build-reviews` to expand concise evidence notes before
`record-many`. These helpers never infer factual approval. `report --brief --since`
keeps full reports on disk and shows counts plus changed finding IDs.

Say **"Audit the next shard"** to run the next 50-question content review. Work
proceeds through files in manifest order; unfinished batches resume automatically.
Say **"Audit status"** for progress. These shortcuts are defined in AGENTS.md.

- `baseline.json`: frozen hashes of the 2,037 active questions at workflow adoption.
  This is a migration boundary, not factual approval. Do not extend/regenerate it.
- `ledger.json`: per-question structural coverage, review evidence and history;
  content-bound warning decisions live here too. Use the audit commands to update it.
- `queue.json`: default sequential batch size (50) and plan/packet locations.
- `runs/next-shard-NNNN-plan.json` and its matching `-result.json`: fixed scope and
  completion report for each sequential batch. An incomplete or stale batch is
  resumed before new work is selected. The scratch work packet is regenerated
  under artifacts/question-audit/current.json; keep filled review files separate.
- `adoption-report.json`: initial coverage and open findings. All 2,037 passed the
  structural gate. No complete manual/four-option source review was inferred from
  older audit prose or the nine existing source links. The 592 advisory findings
  are candidates for investigation, not 592 confirmed defects.
- `runs/2026-11-02-first-review-plan.json`: a prepared first review batch of 30
  risk-prioritized questions plus 21 reproducible outside-pattern random samples
  (three per category). No factual review of this batch is claimed.

Plans and final/partial run reports belong in `runs/` and should be versioned with
their changes. Scratch templates and regenerable whole-bank reports belong in
ignored `artifacts/`. Keep ledger history and retired question snapshots.

Quick status: `python scripts/question_audit.py report --out artifacts/question-audit.json`

Sequential progress: `python scripts/question_audit.py status`

Prepare/resume a batch: `python scripts/question_audit.py next`

Release gate: `python scripts/question_audit.py check`

New review templates use schema 2: premise evidence, an evidence basis for every
option, and a final challenge of competing answers. Existing reviews retain their
original evidence standard; the tool never invents a retrospective challenge.
Reports distinguish recorded evidence, source verification without open manual
concerns, and completed approval without any open findings.

Use `record-many` to validate all supplied review files before one ledger update.
Use `retire` to preserve a duplicate's exact snapshot and decision with a checked
replacement, or `--no-replacement` for upkeep-only removals. `reschedule` re-tiers
recheck dates (rule 7) without changing evidence. An interrupted retirement requires `recover-retirement` before other
commands can proceed. `record-retirement` documents an existing preserved removal.
Use `classify` to label factual, clarification, distractor, explanation, difficulty,
category, scope or metadata changes. Complete closes require documented retirements
and classified retained edits. See QUESTION_AUDIT.md for command arguments.

Packets include ranked full four-option comparisons and paths to complete topic
digests. Selectors are discovery hints; inspect missing context with additional
searches. Common shared-answer groups are retained. Related material never expands
the fixed plan. Saved result replacements preserve a sibling result-history folder.
