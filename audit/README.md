# Audit records

Follow [QUESTION_AUDIT.md](../QUESTION_AUDIT.md) for the authoritative procedure.
Dates in the ledger and reports use UTC.

- `baseline.json`: frozen hashes of the 2,037 active questions at workflow adoption.
  This is a migration boundary, not factual approval. Do not extend/regenerate it.
- `ledger.json`: per-question structural coverage, review evidence and history;
  content-bound warning decisions live here too. Use the audit commands to update it.
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

Release gate: `python scripts/question_audit.py check`
