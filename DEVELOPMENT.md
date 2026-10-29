# Development and release notes — v1.39

This remains a static app. There is no build step. npm dependencies are for
verification only; production uses the Firebase compat CDN scripts.

## Runtime

`bootstrap.js` loads `game-logic.js`, `data-logic.js`, `storage.js`, then `app.js`.
Firebase loads independently with bounded waits, so a CDN failure cannot prevent
practice. The default adapter remains FirebaseAdapter. Never switch the real app
to LocalStorageAdapter to test it: `scripts/visual_check.py` makes an isolated copy,
changes only that copy, and blocks Firestore requests.

`data-logic.js` contains the pure stats, reset, and homework transformations shared
by both adapters. Keep rule changes there and in `game-logic.js`, with regression
tests. Both the local adapter and actual Firebase transactions are exercised.

## Saved games

- Regular games receive a random persistent `gameId`. Checkpoints preserve the
  ID, start-day date, question snapshots, answers, and player `resetRevision`.
- Daily games use `daily_YYYY-MM-DD`; the date belongs to the challenge, even if
  completed after a reset. Pending daily games are archived by date and can be
  resumed from settings on a later day. An old single-slot checkpoint migrates
  automatically.
- A transaction reads the player and `users/{id}/games/{revision_gameId}` receipt
  before applying stats. A retry returns the saved receipt. Concurrent devices
  completing the same daily share one receipt and one score award. Daily bonus
  eligibility is computed from fresh stored data inside the transaction.
- Local cleanup happens after server success and cannot reclassify the server
  write as failed. The UI displays Saving, Saved, Already saved, or Retry.
- Reset and restore increment `resetRevision`. Older unfinished games cannot
  bring reset points back. Each admin reset/restore backs up the outgoing player.
- Points belong to the game's captured start month (daily: challenge month).
  `monthlyTotals` preserves older buckets, so a delayed save cannot roll newer
  totals backward. Legacy current/previous monthly slots are migrated on write.

## Daily questions and dates

The shared reset is **08:00 UTC year-round**, displayed in the player's local
time with a countdown. It is 4 a.m. Toronto in summer and 3 a.m. in winter; it is
not defined as 2 a.m. Mountain year-round. Weekly homework uses the same boundary
on Thursday. Returning from the background refreshes player/day/homework state.

`dailies/{date}` stores immutable `questionIds` and complete question snapshots.
Existing ID-only records can be upgraded exactly once, keeping their order and
IDs. Removed duplicate questions are retained in `questions/retired.json` for
legacy daily migration and old checkpoints, and never enter a new game's pool.
Never randomly replace a missing historical question. Show an unavailable state
if its original record cannot be recovered.

Unseen questions are selected first. Regular games top up from oldest seen IDs;
daily selection relaxes oldest exclusions first. Shared recent history is merged
inside transactions, deduplicated, and capped at 300 IDs.

## Practice and content

Missed-question and weakest-category practice are available from player settings
after there is relevant history. Practice does not award competitive points or
update competitive accuracy. The separate home-screen practice entry also works
offline after an initial online visit and cache installation. `sw.js` caches only
same-origin app assets and questions; database requests remain network-only.
The service worker never caches the admin page or update probes.

There are 2,037 active questions plus three retired duplicates (754 → 27,
1454 → 47, 766 → 31). Retired IDs must not be reused. Optional question metadata:

```json
{
  "factId": "cinderella.transformation-spell",
  "film": "Cinderella",
  "explanation": "The Fairy Godmother's magic helps Cinderella attend the Royal Ball.",
  "source": "https://movies.disney.com/cinderella-1950",
  "verifiedAt": "2026-10-29"
}
```

Fact IDs must be unique across active questions. Sources must be HTTPS. Nine
initial questions include verified explanations and links; adding metadata is
incremental, not a claim that all 2,037 facts were independently reverified.
The admin page exports difficulty recommendations once a question has at least
20 attempts: 80%+ correct suggests easy, 45%+ medium, otherwise hard. These are
review suggestions, not automatic changes. Existing labels remain editorial
until sufficient player data exists.

## Verification

Use Node 24, Python 3.13+, Java 21+, and Playwright 1.60.0. On Windows, the emulator
runner also detects an optional portable JRE under ignored `.tools/jre/`.

```
npm ci
pip install playwright==1.60.0
python -m playwright install chromium webkit
npm test
python -m unittest discover -s test -p "test_*.py"
python scripts/validate_corpus.py
npm run test:emulator
python scripts/visual_check.py --out artifacts/chromium
python scripts/visual_check.py --browser webkit --out artifacts/webkit
```

The emulator command explicitly uses `demo-disney-trivia`; it must never target
production. Browser checks cover keyboard controls, persistence, lost save
responses, rollover, delayed responses, explicit movie watches, practice, and
actual offline reload in addition to the original game flows. Inspect screenshots
in `artifacts/`. CI runs both browsers, unit tests, corpus checks, and emulator
tests. `deploy.ps1` runs the same checks before commit/push and syncs version
strings in the page, bootstrap, admin page, and offline cache.

The offline reload check uses full browser offline emulation in Chromium. WebKit
1.60 uses an unavailable-origin control (the isolated HTTP server is stopped),
and asserts the reload is served by the service worker. This avoids Playwright's
[known WebKit offline-emulation defect](https://github.com/microsoft/playwright/issues/42775),
fixed upstream in 1.64. This is not a substitute for a real iPhone airplane-mode test.

Development dependency overrides pin patched grpc, telemetry, uuid, and re2
versions. `npm audit` reported zero vulnerabilities after installing them.

## Deployment

No production data migration, app publishing, or rule deployment is performed by
tests. App deployment uses `deploy.ps1`; rules require a separate authenticated
Firebase deployment. See `SECURITY.md` for the password-free access tradeoff and
rule deployment command. The app and rules should be deployed together.

Older historical sections in `CLAUDE.md` describe previous versions. This file
and the current code take precedence for the behaviors changed in v1.39.

## Completed verification — October 29, 2026

`deploy.ps1 -DryRun -IncludeUntracked` completed successfully for v1.39:

- 45 JavaScript tests for game rules, adapters, and actual admin handlers.
- Five Python regression tests for content tooling.
- Nine tests against the real Firestore emulator and versioned rules.
- Full Chromium and WebKit smoke/regression suites; no live database traffic.
- Structural validation of all 2,037 active questions.
- Mobile screenshots reviewed for home, settings, game, results, and review.

No files were staged or committed, and nothing was published. No live player data
was changed. Password-based or account-based access was not added, per owner request.
