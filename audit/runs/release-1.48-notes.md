# Release v1.48

Prepared November 10, 2026 by Codex at the owner's request to commit and publish.

This release publishes both generation rounds: **140 new questions**, including
40 in round 1 and 100 in round 2. All **1,995 active questions** have current
approval, with no open findings or remaining source-verification backlog. The
185 retired question snapshots are preserved. Generation notes and complete
four-option evidence records are retained under `audit/runs/generation-0001-*`
and `audit/runs/generation-0002-*`.

q-009 is now full at 250 questions; the new q-010 shard holds 20 questions and is
included in the manifest. App version, page asset queries, bootstrap fallback,
review-page asset queries and offline cache are synchronized to v1.48. This lets
open apps detect the release and installed clients refresh cached content,
including the new shard. No scoring, storage, authentication, Firestore rules or
production player data changes are included.

Release verification completed before commit:

- `deploy.ps1 -DryRun -IncludeUntracked` passed, using an ignored workspace-local
  temporary directory and process-launch permissions for isolated tests.
- Corpus validation: 1,995 active questions in 10 shards; zero errors.
- Audit gate: zero errors, zero awaiting source verification, zero open findings.
- JavaScript: 48 unit tests passed. The suite was additionally confirmed on
  Node 24.22.2, matching the repository and CI runtime.
- Python content-tool tests: 76 passed.
- Chromium and WebKit: both full isolated suites passed, 150 assertions combined;
  zero live Firestore requests and zero page/console errors. Offline reload and
  practice passed with the new manifest and shard. Mobile home, game, results and
  flag-resolution screenshots were visually inspected.
- Demo Firestore emulator: 10 tests passed; additionally confirmed on Node
  24.22.2. Expected denied-write messages belong to passing negative tests.
- Git whitespace validation passed.

Raw logs and screenshots remain under ignored `artifacts/release-1.48-*` paths.
The initial local default Node runtime was 25; the explicit Node 24 reruns remove
that runtime mismatch from the JavaScript/emulator evidence.

The deployment script's commit stage uses `git add -A`, so this release uses its
completed dry-run checks followed by explicit-path staging and commit/push. The
pre-existing `APP_AUDIT.md` deletion and untracked `debug.log` are excluded.
Generation reports remain historical records of local completion; this release
records their subsequent publication scope. Publication verification checks the
commit's GitHub App checks, Pages deployment, live version/cache and served
question manifest/shards against this release.
