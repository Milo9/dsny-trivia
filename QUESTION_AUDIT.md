# Question audit procedure

This is the current authority for question creation and audits. It supersedes
historical audit instructions in CLAUDE.md. DEVELOPMENT.md remains authoritative
for game persistence and historical question snapshots. An audit checks content;
passing structural validation alone never establishes factual correctness.

Use [audit/EFFICIENT_WORKFLOW.md](audit/EFFICIENT_WORKFLOW.md) for compact reading,
topic-grouped research within the fixed scope, reusable source notes, concise
evidence authoring and brief report/delta output. These are the default efficiency
practices; they preserve every acceptance requirement below. Start with the saved
plan and `current-compact.json` companion view; consult `current.json` for prior
evidence/templates when needed. Complete topic context is still required, but read
it once per unchanged packet rather than once for each question. No cache entry or
helper-generated field proves factual support.

## Simple requests: "Audit the next shard"

Say **"Audit the next shard"** (or **"Audit the next chunk"**) to have the assistant
perform the next queued audit. Say **"Audit status"** for progress only. The
repository's AGENTS.md gives future sessions the same instructions.

An audit chunk defaults to **50 questions within one physical question file**.
The queue follows questions/manifest.json order and the order of questions inside
each file, starting at q-001.json. It finishes that file before starting q-002.json,
and so on. A last batch in a file can be smaller than 50. Gaps in IDs do not matter.
The default is configurable in audit/queue.json; a different size applies only to
new batches. The older risk/random plan remains available as a separate workflow.

The assistant uses these commands behind the scenes:

```text
python scripts/question_audit.py status
python scripts/question_audit.py next
```

`status` is read-only. `next` creates a fixed-scope plan under audit/runs/ and a
work packet at artifacts/question-audit/current.json, or resumes the earliest
unfinished sequential plan. The packet contains remaining questions, blank review
templates, existing current reviews, coverage, open findings, full four-option
duplicate comparisons ranked for review, and paths to complete topic digests
under the packet's `topics/` directory. Topic selectors search stems and correct
answers; when no film is recognized, a whole-category digest is provided. Read
the full matching digest and search additional terms if a selector misses context.
Related questions outside the batch do not expand its scope. Save filled templates separately:
the packet is regenerated on resume. These commands select work; the assistant
must still research sources and perform the full checklist below.

Progress is derived from current ledger evidence and warning decisions. Partial
reviews, unresolved warnings, due rechecks and changed content do not count as
finished. Completed questions are skipped on resume. Even when all evidence is
present, the queue waits for the saved complete-for-scope report at its printed
result path before advancing. The completion report records final question hashes;
subsequent edits require a renewed report. A later edit, overdue review or new
warning can reopen an earlier batch. Existing risk-based reviews also count toward
coverage when their evidence and warning decisions are current.

After the factual work, use the paths printed by `next` to finish the batch:

```text
python scripts/question_audit.py close audit/runs/next-shard-0001-plan.json --reviewer REVIEWER --out audit/runs/next-shard-0001-result.json
```

Use the actual reviewer name. Add --partial for unfinished work; the next request
will resume it. The assistant reports the batch's findings and progress through
the current file and the whole bank. A factual audit request does not automatically
publish content changes. `next --preview` shows selection without creating files;
`next --size 25` requests a smaller new batch while preserving any active scope.

## Acceptance checklist

For every new or edited question, and every question selected for a factual audit:

1. Read the full question and all four answers. Check the premise itself before
   choosing an answer. Establish the exact film version, scene, park/location,
   ship, language/region or historical date needed to make it precise. Distinguish
   ownership from possession/location, a character's belief from the film's reveal,
   and a claim about the listed options from a claim about every family member.
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
   Classify each option's evidence as `direct`, `contradiction`,
   `exclusive-inference`, or `exhaustive-list`. Explain the inference: a unique
   numeric identifier can exclude other identifiers, but establishing one ability
   does not exclude a simultaneous ability or visual effect. A missing detail in
   a short synopsis is not proof that it never happens. The same source can
   legitimately support several options when it establishes their distinct roles
   or an exhaustive list; four different URLs are not required.
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

Before recording source verification, perform a final evidence challenge: try to
make each distractor defensible under the literal wording, check that the cited
passage actually excludes it, and recheck the source-backed premise. Record the
reviewer, date and specific challenge notes. Another person is welcome but is not
required; a named reviewer must actually perform this separate check. Leave the
review unfinished or track an unresolved `issue` when the evidence is insufficient.
The validator checks that these records exist; it cannot establish source support.

Examples from batch 1: Cinderella's gown needs a scene because its silver creation
and blue moonlit appearance differ; Coco's mausoleum location must not be confused
with original guitar ownership; Encanto's no-gift claim must not exclude in-laws;
Pinocchio's nose growth alone does not rule out a simultaneous color change.

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
Ledger entries and decision history must also be retained. The explicit `retire`
command is the only audit command that edits shards. It checks an active
replacement, copies the exact original snapshot, preserves the ledger review,
and records a hash-bound duplicate rationale, evidence reference and replacement
snapshot. Its write-ahead journal permits rollback after an interrupted multi-file
update. Audit commands refuse further work while recovery is pending. No audit
command resolves player flags or accesses production Firestore.

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
Newly recorded reviews require schema 2: source-backed `verification.premise`,
an evidence `basis` for every option, and `verification.challenge`. Legacy schema-1
reviews remain in history/current records with their original limitations, and
reports disclose them separately as `legacyEvidenceReviews`; they are never
silently promoted to the new standard. Renewing one requires an actual re-review.

```text
python scripts/question_audit.py record artifacts/review-123.json
python scripts/question_audit.py record-many artifacts/review-123.json artifacts/review-124.json
python scripts/question_audit.py report --out artifacts/question-audit.json
```

`record-many` also accepts files containing JSON arrays. It validates every ID,
content hash, snapshot, option and challenge before a single ledger write. A bad,
duplicate or stale review rejects the whole import, preserving all prior evidence.

Use the supported commands instead of temporary shard-editing scripts:

```text
python scripts/question_audit.py retire 123 --replaced-by 456 --reviewer REVIEWER --reason "Same character-object fact in reverse; retain the more precise question." --reference audit/runs/comparison-123-456.json
python scripts/question_audit.py recover-retirement
python scripts/question_audit.py record-retirement 123 --replaced-by 456 --reviewer REVIEWER --reason "Document the already-preserved duplicate decision." --reference audit/runs/comparison-123-456.json
python scripts/question_audit.py classify 789 --type clarification --type difficulty --reviewer REVIEWER --reason "Specified the film version and calibrated recall difficulty." --reference audit/runs/review-789.json
```

`retire` reruns structural validation and refreshes `artifacts/question-audit.json`.
`recover-retirement` is only for a pending journal and restores the original files;
then rerun sync/report/check. `record-retirement` documents an existing intact
snapshot without changing it. Both retirement commands require the actual
duplicate comparison; moving a question is not evidence that it was audited.

Classify each edited retained question before closing the plan. Supported types
are `factual`, `clarification`, `distractors`, `explanation`, `difficulty`, `category`,
`scope`, and `metadata`. Multiple types may apply, so their counts are not additive.
Classification records are bound to the final content hash and preserve history.
Do not label every edit as a factual error. The frozen baseline is unchanged.

The report includes open findings, per-question coverage, risk reasons, due dates
and remaining verification. A concern discovered by reading or sampling can also
be tracked, even when no detector flags it:

```text
python scripts/question_audit.py issue 123 --reviewer Milo --reason "Two plot interpretations may support different options; inspect the original scene."
```

Manual concerns remain open across wording changes until explicitly decided.
Marking one fixed requires a fix reference and current four-option verification.
An unresolved manual concern blocks release even on an unchanged legacy question.
New decisions closing a manual concern (`accepted` or `fixed`) require an evidence
reference and a renewed schema-2 review with a completed challenge. A review that
predates the concern cannot simply be reused to dismiss it. Historical decisions
retain their original evidence and are not retrospectively upgraded.
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
Reciprocal answer/stem mentions and similar fact wording receive higher duplicate
review priority than unrelated questions sharing a color, year or number. All
shared-answer candidates remain visible, including common and short answers.
Ranking is advisory: an inverse match can also contain a separate production,
song or historical fact. Read both complete questions and decide the actual overlap.

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
removed questions have preserved snapshots and documented retirement decisions,
and retained edits have classifications. It records scope, reviewed/verified
counts, change-type counts, changed/retired IDs, resolved findings, open concerns, overall remaining
coverage and scheduled rechecks. It says **complete-for-scope**, never implies the
entire bank was verified. To record an unfinished run, add `--partial`; the output
explicitly lists the work left. An empty plan cannot be called complete.

Reports distinguish current `evidenceRecorded` from `sourceVerified` (which
excludes open manual evidence concerns) and `approved` (which also requires
structural/manual completion and no open findings of any kind). Queue progress
uses completed approval. A partial report lists unresolved question IDs as well as
finding IDs, undocumented retirements and unclassified edits. Replacing a saved
result archives its previous contents in a sibling `*-result-history/` directory.

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
