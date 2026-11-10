# Release v1.49

Prepared November 10, 2026 by Codex at the owner's request to commit and publish.

This release publishes generation round 3: **100 new questions** across 20
underrepresented classic theatrical live-action films. The bank now has **2,095
active questions**, all currently approved, with no open findings or remaining
source-verification backlog. All 185 retired question snapshots and all 1,995
pre-round active question objects are preserved. The additions and complete
four-option evidence are recorded in `audit/runs/generation-0003-*`.

q-010 now contains 120 questions. The manifest's ten shard paths are unchanged.
App version, page asset queries, bootstrap fallback, review-page asset queries
and offline cache are synchronized to v1.49 so installed clients can refresh the
updated question bank. No scoring, storage, authentication, Firestore rules or
production player data changes are included.

Release verification completed before commit:

- `deploy.ps1 -DryRun -IncludeUntracked` passed using an ignored workspace-local
  temporary directory and process-launch permissions for isolated tests.
- Corpus validation: 2,095 active questions in ten shards; zero errors.
- Audit gate: zero errors, zero awaiting source verification, zero open findings.
- JavaScript: 48 unit tests passed, also confirmed on Node 24.22.2.
- Python content-tool tests: 76 passed.
- Chromium and WebKit: both full isolated suites passed, 150 assertions combined;
  no live Firestore requests or page/console errors. Offline reload and practice
  passed with the updated bank. Mobile home, game and flag-resolution screenshots
  were visually inspected.
- Demo Firestore emulator: ten tests passed, also confirmed on Node 24.22.2.
  Expected denied-write messages belong to passing negative tests.
- Git whitespace validation passed. Frozen audit baseline and retired snapshots
  are unchanged.

The local default Node runtime was 25; explicit Node 24 unit/emulator reruns
confirm the repository's required runtime. Raw logs and screenshots remain under
ignored `artifacts/release-1.49-*` paths.

The deploy script stages everything, so its completed dry-run checks are followed
by explicit-path staging and commit/push. The pre-existing `APP_AUDIT.md` deletion
and untracked `debug.log` are excluded. Generation reports remain historical
records of local completion; this release records their publication scope.

Post-push publication verification checks the commit's App checks and Pages
deployment, plus exact live versioned assets, question manifest, all ten active
shards and retired snapshots against this release.
