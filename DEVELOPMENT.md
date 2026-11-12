# Development and release notes — v1.50

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

The current editorial audit procedure is [QUESTION_AUDIT.md](QUESTION_AUDIT.md).
Its version-bound ledger distinguishes structural checks, manual review and
four-option source verification. CI and deployment run its read-only release gate.
The frozen adoption baseline is a disclosed backlog, not factual approval.
For conversational sequential audits, "Audit the next shard" means perform the
next 50-question batch via `question_audit.py next`, resuming unfinished work.
AGENTS.md defines the shortcut; `question_audit.py status` is read-only.

Missed-question and weakest-category practice are available from player settings
after there is relevant history. Practice does not award competitive points or
update competitive accuracy. The separate home-screen practice entry also works
offline after an initial online visit and cache installation. `sw.js` caches only
same-origin app assets and questions; database requests remain network-only.
Requests are network-first, but a request that gets no answer within 4 s (stalled
wifi) is served from the cache while the network request finishes in the background;
for 30 s after a stall, later requests wait only 300 ms. `loadQuestions()` publishes
`QUESTIONS` only after every file loads, so the static practice button cannot open
settings mid-boot. The isolated browser suite serves the test copy through
`scripts/stall_server.py` and checks a stalled-wifi reload in both browsers, plus a
stall with the real FirebaseAdapter and a never-answering Firebase CDN/Firestore
(practice must start and stay running past bootstrap's CDN time limits).

The home hero shrinks on short screens (style.css, max-height 760/700/600 px) so the
first two players fit at 375x667 (~60 px spare) and at Safari's ~548 px usable
height. The browser suite asserts the 667 px case and prints 647/548 px positions.
The service worker never caches the admin page or update probes.

There are 2,191 active questions plus 189 preserved retired snapshots in the
working bank after forty-two sequential audit batches and four generation rounds
adding 340 questions. The latest 100 questions cover 16 live-action films, two
Pixar features, Disneyland Paris and Disney Adventure. See
audit/runs/generation-0004-notes.md for coverage and evidence. The prior rounds
are recorded in audit/runs/generation-0001-notes.md through generation-0003-notes.md.
See questions/retired.json for preserved snapshots and replacement IDs.
Optional question metadata:

```json
{
  "factId": "cinderella.transformation-spell",
  "film": "Cinderella",
  "explanation": "The Fairy Godmother's magic helps Cinderella attend the Royal Ball.",
  "source": "https://movies.disney.com/cinderella-1950",
  "verifiedAt": "2026-10-29"
}
```

Fact IDs must be unique across active questions. Sources must be HTTPS. There are 347
active questions with verified explanations and links. All 2,191 active questions
now have current manual review and four-option evidence; explanations and links
embedded in the playable question objects remain incremental metadata.
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

`visual_check.py` aborts with exit code 3 if a run exceeds 20 minutes
(`VISUAL_CHECK_WATCHDOG_S`), printing the last completed check, so a hung browser
step fails deploy/CI instead of freezing it.

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

Development dependency overrides pin patched grpc, telemetry, uuid, re2 and undici
versions. On 2026-11-12 `npm audit` reported 11 moderate advisories, all in the
firebase-tools dependency tree (CLI/emulator tooling, never shipped).

The emulator tests load Firebase through the `firebase-cdn` alias
(`npm:firebase@10.12.0`), the same compat SDK version that bootstrap.js and review.html
load from the CDN, and fail if those versions diverge. Upgrade the CDN URLs and the
alias together. `@firebase/rules-unit-testing` keeps its own newer `firebase` peer.

## Deployment

GitHub Pages builds `main` with Jekyll; `_config.yml` excludes `audit/`, `docs/`,
`scripts/`, `test/`, Markdown and other development files from the published site
(they remain public in the repository). Anything the app or review.html fetches must
stay published; add new runtime files outside those excluded paths.

`deploy.ps1` bumps APP_VERSION only when a code file changed. For a question-only
release, raise APP_VERSION in app.js by hand first so installed clients refresh the
offline bank; the script then syncs `?v=` strings and the service-worker cache.

Release v1.55 tiers scheduled rechecks (QUESTION_AUDIT.md rule 7, backlog #5): the
220 rechecks due 2027-01/02 became 48 historical (no recheck), 11 changeable (due
2027-01/02) and 158 stable (staggered 2027-07..10, ~50/month), and #2560, #2561
and #2277 (single-listing questions) were retired without replacement, leaving
2,191 approved active questions. `status` prints the upcoming recheck calendar.
See audit/runs/2026-11-12-recheck-tiers-notes.md.

Release v1.52 removes answer giveaways from ten questions, replaces #2432's
implausible distractors, and retires #976 (leak; duplicate of #1399's fact), leaving
2,194 approved active questions. See audit/runs/release-1.52-flag-followup-notes.md.

Release v1.50 publishes generation round 4 and brings the active bank to
2,195 approved questions. q-010 contains 220 questions. The app and offline cache
use v1.50. See audit/runs/release-1.50-notes.md for release verification.

Release v1.49 publishes generation round 3: 100 new questions across 20 classic
live-action theatrical films, bringing approval to 2,095 of 2,095 active questions
with no open findings. q-010 now holds 120 questions. All 185 retired historical
snapshots are preserved. This release changes no Firestore rules or player data.

The version and offline cache are synchronized to v1.49 so installed clients can
refresh the updated bank. Release verification results are recorded in
audit/runs/release-1.49-notes.md. Earlier v1.48 published generation rounds 1 and 2
and their 140 additions, bringing the bank to 1,995 before this release.

The next question audit work follows new content, new concerns or scheduled
rechecks; the sequential queue has no remaining unaudited chunk.

No production data migration, app publishing, or rule deployment is performed by
tests. App deployment uses `deploy.ps1`; rules require a separate authenticated
Firebase deployment. See `SECURITY.md` for the password-free access tradeoff and
rule deployment command. The app and rules should be deployed together.

Older historical notes (archived from CLAUDE.md) live in `docs/history/CLAUDE-through-v1.50.md`. This file
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
