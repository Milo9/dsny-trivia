# Release v1.44

Includes the pending completed sequential audits 14?18, corpus snapshots and evidence history. Batch 18 completed with 50 reviewed, 42 approved/evidence-recorded, 26 edited, eight retired and zero unresolved in scope. See next-shard-0018-result.json and next-shard-0018-notes.md.

Version/cache references synchronized to 1.44 by deploy.ps1 -DryRun -IncludeUntracked. Full release checks passed: structural corpus validation (1,896 active), question audit release gate, 48 JavaScript tests, 76 Python tests, Chromium and WebKit browser/regression suites including offline reload, and 10 Firestore emulator tests against demo-disney-trivia. Mobile home, game and results screenshots inspected. The initial restricted-sandbox browser run had blocked-network console errors; the complete network-enabled rerun passed.

No Firestore rule changes are included. Automatic approval review rejected an attempted redeployment of the identical rules because of their unauthenticated-access policy; no production rules were changed. App publishing proceeds against the existing policy.

Publication uses an explicit file list after deploy.ps1 completed every preflight gate; unrelated local APP_AUDIT.md deletion, .claude settings and debug.log are excluded. Empty regenerable batch 18 note templates are also excluded.
