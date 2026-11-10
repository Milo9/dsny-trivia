# Release v1.47

Prepared November 10, 2026 by Codex at the owner's request to commit and publish.

This release publishes question-audit batches 37 through 42: 280 planned questions reviewed, 279 retained questions approved, 174 retained questions edited, one duplicate retired with its historical snapshot and evidence preserved, and zero unresolved questions. All six plans have complete-for-scope results. The active bank now has current approval for all 1,855 questions, and q-009 is complete at 130/130. The retired bank has 185 snapshots. Individual batch notes distinguish factual corrections from editorial changes and document source access limitations.

App version, page asset queries, bootstrap fallback, review-page queries and offline cache are synchronized to v1.47 so installed clients can detect the update. No scoring, storage, authentication, Firestore rules or production player data changes are included.

## Release verification

`deploy.ps1 -DryRun -IncludeUntracked` passed after setting TEMP and TMP to a workspace-local ignored directory and allowing the isolated browsers/emulator to launch outside the sandbox:

- Structural corpus validation: 1,855 active questions, nine shards, zero errors.
- Audit gate: zero errors, zero awaiting source verification, zero open findings.
- JavaScript unit tests: 48 passed; also independently passed on Node 24.22.2.
- Python content-tool tests: 76 passed.
- Chromium and WebKit: both full isolated suites passed, 150 assertions combined; no live Firestore traffic or page/console errors. Chromium used full offline emulation and WebKit the documented unavailable-origin control. Mobile home, game, results and flag-resolution screenshots were inspected.
- Demo Firestore emulator: 10 tests passed. The suite was additionally run successfully with Node 24.22.2, matching CI's required runtime.
- Git whitespace validation passed.

The initial sandbox test attempt failed on temporary-directory permissions, and a sandbox browser attempt stalled; neither was a product test failure. The workspace-local temporary directory and approved external process launch resolved those environment restrictions. Expected denied-write messages in emulator negative tests are passing assertions, not production traffic.

Raw local verification logs and screenshots are under ignored `artifacts/`. Publication verification will check GitHub App checks, Pages deployment and the live version/cache plus both changed active shards and the retired snapshots against the committed release.

The first GitHub App checks run for commit 66c8069 passed unit tests, demo emulator tests, corpus validation, the audit gate and Python tests, then failed before browser tests because ubuntu-latest had moved to Ubuntu 26.04. Its log explicitly reports that Playwright 1.60.0 cannot install Chromium on that platform. The App checks runner is now pinned to ubuntu-24.04, which the pinned Playwright dependency supports. This CI-only follow-up preserves v1.47's app and question content; the replacement workflow run verifies the runner correction.

The unrelated APP_AUDIT.md deletion and debug.log are excluded from the release commit. The completed audits' original notes remain historical records of their local completion; this release records their subsequent publication scope.
