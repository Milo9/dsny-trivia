# Release v1.45

Publishes completed sequential audit batches 19 through 24 from commit 3c80189.
The active corpus contains 1,873 questions and 167 preserved retired snapshots.
Current audit approval is 997/1,873, with 876 still in the disclosed source-review
backlog. Batch 24 is complete for its 45-question scope: 43 approved/evidence
records, 15 retained edits, two retirements and no unresolved questions.

APP_VERSION, page asset queries, bootstrap fallback, review-page asset queries and
the service-worker cache are synchronized to 1.45. This refreshes offline caches
for the audited content. DEVELOPMENT.md reflects the new corpus counts.

Preflight completed through deploy.ps1 -DryRun -IncludeUntracked: 48 JavaScript
tests, 76 Python tests, Chromium and WebKit full browser/regression checks
(including offline reload), and 10 Firestore emulator tests against
demo-disney-trivia. Separate corpus validation and the audit release gate passed
with zero errors. Mobile home, settings, game, results and flag-resolution
screenshots were inspected. Browser checks used isolated copies and no live
Firestore writes. No Firestore rules changed in this release.

Publication uses an explicit file list so the unrelated APP_AUDIT.md deletion,
.claude settings and debug.log are excluded. The full deployment script was used
for preflight only because its publication step stages every local change.
