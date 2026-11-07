# Project instructions

Read QUESTION_AUDIT.md for the current question audit requirements. For runtime,
storage, scoring, offline behavior or releases, also read DEVELOPMENT.md and
SECURITY.md. Preserve the owner's password-free/account-free design.

## "Audit the next shard"

Treat "audit the next shard", "audit the next chunk", and "continue the question
audit" as instructions to **perform** the next queued content audit:

1. Run `python scripts/question_audit.py next`. Read the named saved plan and
   `artifacts/question-audit/current-compact.json` first; the complete packet at
   `artifacts/question-audit/current.json` retains templates and prior evidence.
   Follow `audit/EFFICIENT_WORKFLOW.md`: group research within the batch by topic,
   read each complete topic digest once per unchanged packet, search reusable source
   notes, and build full reviews from concise explicit evidence notes. Use brief
   reports and finding deltas; inspect applicable findings and preserve all checks.
   An audit chunk defaults to 50 questions,
   within one physical shard, proceeding in manifest order. Announce the selected
   file, batch and scope. Resume unfinished work instead of choosing another batch.
2. Follow QUESTION_AUDIT.md: research credible sources, verify the premise and all four options,
   check context/wording/giveaways/category/difficulty/scope and cross-bank dupes,
   fix confirmed problems, challenge whether any distractor could also fit, and record the evidence basis,
   locators and final challenge on the final wording. Creating a packet or
   running mechanical checks does not fulfill a request to audit.
3. Keep the plan's scope fixed. On resume, focus on its remaining questions and
   open findings. The packet includes related questions outside the batch for
   duplicate review, plus ranked comparisons and paths to full topic digests;
   read those as context, without expanding the audit scope. Save filled
   review templates separately from the regenerable packet. Never infer that an
   existing source link or a prior partial review proves all four options.
4. Use `record-many` for validated bulk imports, `retire` for preserved duplicate
   removals, and `classify` to distinguish factual fixes from editorial changes.
   Run sync/report/check as appropriate after fixes. Close the plan to its printed
   result path with the actual reviewer. Use --partial when evidence or review is
   unfinished; record unresolved concerns. Do not silently advance past them. If
   next reports awaiting-close, finish the previous report before selecting a new
   batch. Preserve removed question snapshots and evidence history.
5. Report reviewed/evidence-recorded/approved/edited/retired/unresolved counts and
   the change-type breakdown; edited does not mean factually wrong. Give progress through the
   current physical shard and whole bank, and where the next request resumes.
   Finish one batch per request. Publish app/content changes when requested.

"Audit status" means `python scripts/question_audit.py status` (read-only). A
request to change batch size may use `next --size N`; an existing active batch
keeps its original scope. The configured default is in audit/queue.json.
