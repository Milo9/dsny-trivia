# Efficient audit workflow

This is an authoring and reading aid. QUESTION_AUDIT.md remains authoritative.
Keep the saved batch scope, all four option assessments, complete duplicate
context, named manual attestations and the separate final evidence challenge.
Neither cached source notes nor successful compilation establish factual support.

## Read less repetition

Run `python scripts/question_audit.py next` once to prepare/resume work. Read the
named plan and `artifacts/question-audit/current-compact.json` first. This companion
view keeps each batch/comparison question once in a catalog keyed by ID, retaining
the complete question object and all four answers. Comparisons reference IDs.
It omits blank templates and repeated prior evidence; these remain available in
`current.json` when needed. Complete findings and retirement decisions remain visible.
Read relevant existing reviews, coverage gaps and open findings before resuming.

Group remaining questions by the packet's topic names and each topic's
`remainingQuestionIds`, within the fixed batch. Topics can overlap; review each
question once and read all matching context.
Read each complete matching topic digest once for that packet, then research and
review the questions it supports together. This changes work order, not scope.
The command below combines overlapping digests into one question catalog with
all four answers; it never limits matches to the highest-ranked candidates:

```text
python scripts/question_audit.py view --topic "EXACT PACKET TOPIC" --topic "ANOTHER TOPIC"
python scripts/question_audit.py view --ids 123 456
```

`view` defaults to the current full packet and prints compact JSON. `--packet`
selects another full packet; `--out` saves a view. `--ids` selects from the main
packet and any explicitly selected topics, so use it only for follow-up reading,
after complete topic/comparison review. Read missing-context search results too.
If content changes, recheck affected questions, comparisons and topic context;
do not reuse a stale view as evidence of final wording. Resume skips completed
questions; do not repeatedly dump the whole ledger or full report into context.

## Save source notes once

Keep reusable source evidence in `audit/source-notes.json` (initially empty).
Each source ID denotes a specific passage/scene, not an entire website. Example
shape, using placeholders that must be replaced with actually inspected evidence:

```json
{
  "schema": 1,
  "sources": {
    "film-scene-role": {
      "url": "https://example.org/replace-with-real-source",
      "locator": "Specific section or scene/timestamp",
      "evidence": "Concise source-grounded paraphrase of relevant evidence",
      "checkedBy": "Actual reviewer",
      "checkedAt": "2026-11-06",
      "timeSensitive": false,
      "nextReviewAt": null,
      "limitations": "Any access, version or corroboration limitations",
      "topics": ["Exact topic"]
    }
  }
}
```

Prefer concise paraphrases; save only short necessary quotations. Record version,
region and context where relevant. Multiple passages can have separate IDs even
when they share a URL. Search before repeating research:

```text
python scripts/question_audit.py sources audit/source-notes.json --query "topic"
python scripts/question_audit.py sources audit/source-notes.json --ids film-scene-role
```

The search validates the library and shows matching notes and due status. Empty
query lists all notes, so prefer a specific query. For each new question, evaluate
whether the saved passage establishes its premise and excludes each distractor.
Reopen the original source when notes are incomplete, uncertain, time-sensitive,
or do not capture the exact claim. Corroborate exceptional claims as usual.
Changing evidence needs a future `nextReviewAt`; the builder rejects due notes.
Refresh notes only after actual source rechecking. Preserve older evidence in
existing reviews: expansion embeds a copy, so later library edits cannot change it.

## Write concise notes, expand mechanically

```text
python scripts/question_audit.py notes-template audit/runs/next-shard-NNNN-plan.json --reviewer Codex --out audit/runs/next-shard-NNNN-evidence-notes.json
python scripts/question_audit.py build-reviews audit/runs/next-shard-NNNN-evidence-notes.json --sources audit/source-notes.json --out audit/runs/next-shard-NNNN-reviews.json
python scripts/question_audit.py record-many audit/runs/next-shard-NNNN-reviews.json
```

Use the actual reviewer. Template creation does not attest to any checks. Keep
only questions actually completed in the notes' `reviews` array; leave unfinished
work out of the import and record unresolved concerns/partial closure as usual.
Templates contain active planned IDs; use `notes-template --ids 123 456` to select
remaining planned questions in a topic group, or remove already completed reviews
on resume instead of rereviewing them. The template command refuses to overwrite
saved notes; choose a new path for another group or renewed review.

The generated notes have batch-level `reviewer`, `at`, `sourcesChecked` and
per-question records. After reading and challenging evidence:

- Set `sourcesChecked` to the source IDs actually evaluated for these reviews.
- Preserve the generated question `hash`. If wording/options change, inspect the
  final question and renew the notes using a fresh hash; never just patch a hash
  to make stale evidence importable.
- Fill `checks` with all eight names only after performing them:
  `singleAnswer`, `context`, `wording`, `noGiveaway`, `distinctFact`, `category`,
  `difficulty`, `scope`.
- Fill question `notes`, `context`, explicit `timeSensitive` and `nextReviewAt`.
- Fill `premise.reason` and its `sources` array of source IDs.
- Fill all four `options` in stored answer order, each with `basis`, a specific
  `reason` and `sources` IDs. Bases are `direct`, `contradiction`,
  `exclusive-inference`, or `exhaustive-list`. Source IDs may be shared when the
  passage actually supports multiple assessments; rationales remain per option.
- Fill the separate `challenge` with actual reviewer/date, explicit
  `premiseChecked` and `alternativesExcluded`, and specific competing-answer notes.

The builder supplies schema fields, hashes/snapshots, option text/verdicts, repeated
source objects and checklist booleans from those explicit named attestations.
It rejects stale hashes, missing checks, missing option evidence, unacknowledged
sources, due source notes and invalid reviews. It validates the whole batch before
writing output, never updates the ledger, and never invents reasons or challenge
results. `record-many` still independently validates the final import atomically.

## Keep routine output brief

```text
python scripts/question_audit.py sync
python scripts/question_audit.py report --out artifacts/question-audit.json --brief --since artifacts/question-audit.json
python scripts/question_audit.py check
```

For the first report omit `--since` if that file does not exist. When the same
path is used, the previous report is read before replacement. `--brief` prints
counts and the full report path; `--since` adds IDs of added, changed and resolved
open findings. Read new/changed applicable findings in the saved report, and keep
addressing previously open ones. Delta output is not a replacement for the gate.
All gate errors remain visible. Run structural validation/report after content
fixes and renew evidence on final wording. Classify, retire and close using the
existing commands; report the required final batch counts and shard/bank progress.

The default stays at 50 questions. Smaller batches are available for context
management but can repeat setup; group source work inside the existing scope first.
Measure model token use across comparable batches before claiming token savings.
