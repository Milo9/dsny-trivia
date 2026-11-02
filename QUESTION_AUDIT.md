# Question audit procedure

This is the current authority for question creation and audits. It supersedes
historical audit instructions in CLAUDE.md. DEVELOPMENT.md remains authoritative
for game persistence and historical question snapshots. An audit checks content;
passing structural validation alone never establishes factual correctness.

## Acceptance checklist

For every new or edited question, and every question selected for a factual audit:

1. Read the full question and all four answers. Establish the exact film version,
   park/location, ship, language/region or historical date needed to make it precise.
2. Demonstrate **exactly one defensible answer** under that wording. Explain why
   answers[0] is correct and why each of the other three is incorrect. A source
   confirming answers[0] alone is insufficient. If two options are arguably true,
   rewrite the question or retire it; do not approve the ambiguity.
3. Record supporting HTTPS sources for each option, a specific evidence locator
   (page section, quotation location, film scene/timestamp), and your rationale.
   Prefer the original film/credits, Disney/Pixar/DCL/park materials, official award
   records, or other primary evidence. Search snippets and a generic film homepage
   are not sufficient evidence for a specific plot or attribution claim. Corroborate
   surprising, disputed, exact-number and first/only/record claims independently.
   When primary evidence is unavailable, document the limitation and corroboration;
   leave the question unresolved if the evidence does not establish all options.
4. Check wording and difficulty: clear mobile-readable phrasing, parallel options,
   plausible wrong answers, no grammatical/length clues, no answer giveaways.
   Concise explanatory answers are allowed for why/what-happens questions when all
   options have a comparable form; do not force every answer into a noun phrase.
5. Check distinctness by reading the full topic digest and searching all shards.
   Ask: could memorizing another question's answer solve this one without learning
   a new fact? If so, keep the better question and retire the other. Review both
   wording-similarity and shared-answer candidates; sharing an answer is not itself
   a duplicate. Fact IDs describe the fact, not a rewording, and must be unique.
6. Check category, editorial difficulty and scope. Pixar films use pixar rather
   than movies; character/music categories may still apply. No real TV-show trivia;
   incidental in-universe TV references require a scope decision. Prefer main-canon
   theatrical coverage; sequels/shorts/made-for-TV remain secondary, soft-capped at
   roughly 8–10 questions/title. Coverage counts are approximate signals, not quotas.
7. Avoid unbounded current-status claims. State the historical date where useful.
   Explicitly mark whether the fact can change and give changing facts a next review
   date (normally within 90 days, sooner around announced openings/launches).
8. Run the structural check and audit report again **after every content fix**.
   Review fresh warnings and renew the review on the final wording. Do not resolve
   a player flag until its fix is present in the published version.

The eight `manual` booleans in the review template attest to single-answer validity,
context, wording, giveaways, distinctness, category, difficulty and scope. They are
editorial attestations, not automated proof. Source verification additionally
requires evidence and verdicts for all four answer options.

## Evidence and change tracking

`audit/ledger.json` records each question's content SHA-256, structural-check date,
manual review, four-option verification, recheck date and previous reviews. Any
question-field change invalidates its previous approval. `sync` preserves that
evidence in history. Sources already present in shards are imported as
`legacyEvidence`, never inferred to establish a complete four-option review.

`audit/baseline.json` freezes the existing bank at adoption. It is a migration
boundary, **not approval of those questions**. Do not regenerate or extend it to
pass a release. Unchanged baseline questions may remain in the explicitly reported
backlog. New/changed questions need current manual review, all-option verification
and decisions on every applicable warning. Rechecks that become due block release.
Once a baseline question is edited, its new content is subject to those requirements.

Removed questions must be moved intact to `questions/retired.json`, optionally with
`replacedBy`; never reuse an ID. This preserves old daily/checkpoint recovery.
Ledger entries and decision history must also be retained. No audit script edits
shards, resolves player flags, or accesses production Firestore.

## Repeatable commands

Run from the repository root (Python standard library only):

```text
python scripts/question_audit.py sync
python scripts/question_audit.py report --out artifacts/question-audit.json
python scripts/question_audit.py plan --seed 2026-11-review --limit 30 --sample-per-category 3 --out audit/runs/2026-11-plan.json
python scripts/question_audit.py template 123 --out artifacts/review-123.json
```

`plan` selects up to 30 not-currently-verified questions ranked by risk signals,
plus a reproducible random sample outside those patterns in each category. Risk
signals cover attribution, records, numbers/dates, changing facts, inverted logic,
ship/venue details, plot/attributes, TV scope and cross-answer collisions. Each
distractor is compared with other questions' correct answers when their stems
share at least three content tokens. Neither the risk list nor the random sample
guarantees error-free content. Change the seed for each audit; increase the budget
to work down the backlog. Categories with no eligible outside-pattern questions
contribute fewer samples. Plans retain the selected IDs, seed, reasons and starting
hashes; commit plans and final reports under `audit/runs/`.

Fill in the template after reviewing the evidence. Never mark a checklist item true
merely because a script passed. Use `verification: null` to record a manual-only
review honestly; this does not satisfy the new/changed-question release gate.

```text
python scripts/question_audit.py record artifacts/review-123.json
python scripts/question_audit.py report --out artifacts/question-audit.json
```

The report includes open findings, per-question coverage, risk reasons, due dates
and remaining verification. A concern discovered by reading or sampling can also
be tracked, even when no detector flags it:

```text
python scripts/question_audit.py issue 123 --reviewer Milo --reason "Two plot interpretations may support different options; inspect the original scene."
```

Manual concerns remain open across wording changes until explicitly decided.
Marking one fixed requires a fix reference and current four-option verification.
An unresolved manual concern blocks release even on an unchanged legacy question.
Warnings and manual concerns are findings; reviewers must decide:

- `accepted`: false positive or necessary context, with a specific reason.
- `unresolved`: genuine or uncertain concern; explain what remains to investigate.
- `fixed`: first record unresolved, fix/recheck the content, then record the fix
  reference. The original content-bound finding must no longer reproduce. A newly
  worded question may produce a fresh finding that still needs a decision.

```text
python scripts/question_audit.py decide FINDING_ID accepted --reviewer Milo --reason "Different facts: this asks the opening year, the other asks the film release year."
python scripts/question_audit.py decide FINDING_ID unresolved --reviewer Milo --reason "Two options may be true; check the original credits."
python scripts/question_audit.py decide FINDING_ID fixed --reviewer Milo --reason "Corrected attribution and rechecked all four options." --reference "commit or review-file reference"
python scripts/question_audit.py check
```

Decisions are bound to the involved questions' hashes. Editing either side of a
duplicate warning requires a fresh decision. The integrated report includes leak,
category, scope, asymmetric-answer-style, lexical duplicate and uncapped
shared-answer findings. Historical standalone scripts remain useful for recon.

## Completion and cadence

Every run has an explicit saved plan. Use modest batches so verification is
finishable. Check new player flags before selecting a batch; import/export reports
from review.html as needed. Once a month, run triage plus a new outside-pattern
sample. Before every release, run the gate and address scheduled rechecks. Use
player difficulty recommendations only as editorial hints: repeated attempts from
the same small group are not independent evidence of population difficulty.

The Monthly question audit queue GitHub workflow runs on the first of each month
at 13:00 UTC (and on manual dispatch). It uploads a coverage/due-date report and a
fresh seeded review plan, then checks the gate. This prepares work and exposes due
reviews; it does not perform factual verification or update the ledger automatically.

```text
python scripts/question_audit.py close audit/runs/2026-11-plan.json --reviewer Milo --out audit/runs/2026-11-result.json
```

`close` succeeds only when every active question in the planned scope has current
structural, manual and source verification, no undecided/unresolved findings, and
removed questions have preserved snapshots. It records scope, reviewed/verified
counts, changed/retired IDs, resolved findings, open concerns, overall remaining
coverage and scheduled rechecks. It says **complete-for-scope**, never implies the
entire bank was verified. To record an unfinished run, add `--partial`; the output
explicitly lists the work left. An empty plan cannot be called complete.

CI and deploy.ps1 run the read-only audit gate. The gate tolerates the disclosed
untouched legacy backlog, but not missing/stale structural records, incomplete
evidence for new/edited content, their undecided warnings, overdue verified facts,
or deleted historical snapshots. No command can automatically establish that a
source supports a claim; the reviewer remains responsible for reading it.

## Player report follow-up

review.html records the reviewer, time, reason, decision and optional evidence link.
A fixed decision requires an HTTPS link to the published fix. Reopening creates a
new event without erasing the old decision. Resolution events cannot be edited or
deleted under the versioned Firestore rules, and reports are retained. Full backups
include event histories. Older resolved flags display that their reason was not
recorded; do not invent retrospective evidence.

Deploy review.html and firestore.rules together. Until deployed, the new rules and
UI have no effect on production. Names are self-reported in this password-free
family app; a reviewer field does not establish authenticated identity.
