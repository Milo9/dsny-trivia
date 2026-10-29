# Disney Trivia app audit

Audited October 29, 2026, against local revision `773291a` (app v1.38).

Implementation follow-up: v1.39 addresses the findings below in the working tree.
See `DEVELOPMENT.md` for the implementation and verification details. The owner
explicitly declined accounts/passwords: identity-based family/admin authorization
was skipped, while validation rules and immutable-record protections were added.
Those rules and the app still require production deployment to affect the live app.
The original findings are retained below as the audit record.

The main game flows work in the existing automated checks. The most valuable next work is score integrity, daily date handling, and accessibility. A framework rewrite is unnecessary for this app's size and purpose.

## Validation and limits

- All 29 tests in `test/game-logic.test.js` passed.
- `python scripts/validate_corpus.py` passed: 2,040 questions, nine shards, zero structural errors.
- `python scripts/visual_check.py` passed its regular-game, leaderboard, resume, exit, failed-save recovery, daily, review, game-log, and update checks. Its isolated copy used LocalStorageAdapter; no Firestore requests occurred.
- Reviewed mobile screenshots of home, settings, gameplay, results, and daily review at 375 × 667.
- Additional Node VM checks exercised the actual application functions with a mocked DOM and local storage adapter. These reproduced the rollover error, duplicate daily awards from stale sessions, and a false save failure after a committed score.
- No live player records were changed. Deployed Firestore rules were not inspected. Real iPhone Safari, VoiceOver, and Firestore transaction behavior were not exercised by the browser smoke test. This was not a factual verification of every trivia question.

## Recommended fixes, in priority order

### 1. Make game saves safe to retry, including across devices — High

**Evidence:** `app.js:181–188`, `app.js:1481–1543`, `storage.js:273–327`.

The `ended` guard prevents repeated submissions only for one in-memory game object. Saves have no persistent game ID or processed-game check. Daily eligibility and the streak bonus are computed from `currentUser`, outside the Firestore transaction; the transaction adds those already-computed deltas without checking whether that player completed the daily elsewhere.

**Reproduction:** Two isolated daily completions with stale copies of the same player each received the first-daily bonus. A separate check made `saveSeenIds()` throw after `updateStats()` succeeded: the app reported a failed save despite the committed score. Retrying the same game counted it again.

**Fix:** Persist a stable game ID in checkpoints and atomically record each processed game with its stats. Within the same transaction, check daily completion for the challenge date and calculate eligibility from the fresh stored player. Separate server-save success from best-effort local bookkeeping, so a local storage failure cannot turn a successful server commit into a retryable score.

Firestore transactions rerun on conflicting edits, but the callback must actually check the relevant fresh state: [Firebase transaction documentation](https://firebase.google.com/docs/firestore/manage-data/transactions).

### 2. Preserve the daily challenge's date when it finishes after reset — High

**Evidence:** `app.js:1129`, `app.js:1488–1511`.

The game preserves `gameState.dateKey` when starting and checkpointing, but `endGame()` stamps completion with `todayKey()`. A challenge started on October 29 and finished after the next reset is saved as October 30. This can block October 30's challenge and associate October 29's answers with October 30's review.

**Reproduction:** A game with `dateKey: '2026-10-29'` finished with a simulated current day of October 30. Its stored `lastDailyDate` became `2026-10-30`.

**Fix:** Use the challenge's captured date consistently for daily completion, streaks, answers, and logs. Explicitly define how points count when a game crosses a month boundary. Add tests for daily and monthly rollover during play and during save recovery.

### 3. Make player selection and category controls keyboard accessible — High

**Evidence:** `app.js:639–660`, `style.css:658`, `index.html:119–154`.

Player cards are clickable `div` elements without keyboard focus or activation. Category checkboxes use `display: none`, removing them from keyboard navigation and the accessibility tree. A keyboard user cannot select a player through the normal flow. Difficulty, question-count, and leaderboard pills also expose no programmatic selected state.

**Fix:** Use native buttons for player cards; visually hide category inputs while keeping them focusable; show a focus ring on their labels; use radio groups or appropriate selected-state attributes for exclusive choices. Add explicit labels to the player-name and report inputs. Verify with keyboard navigation and VoiceOver.

### 4. Verify and restrict database/admin access — High if the documented rules remain deployed

**Evidence:** `CLAUDE.md:279–290`, `review.html:243–257`, `storage.js:193–210`.

The project documents Firestore rules allowing all reads and writes. The app has no authentication flow, and the review page directly resets scores and deletes flags. If those documented rules remain active, anyone who obtains the public app configuration can alter the database. The configuration itself is not the secret to protect; access rules are.

**Fix:** Inspect deployed rules, then add authenticated family access, explicit admin authorization, and collection/field validation. Keep rules in version control and test them with the emulator. Hiding the review URL or a button does not establish authorization. Firebase explicitly warns that allow-all rules permit anyone to overwrite the database: [Firebase security rules documentation](https://firebase.google.com/docs/firestore/security/get-started).

### 5. Make “Reset ALL scores” reset monthly scores too — Medium

**Evidence:** `review.html:227–232`, `storage.js:443–446`.

`SCORE_ZERO` clears lifetime and daily counters but omits `monthlyKey`, `monthlyPoints`, `prevMonthlyKey`, and `prevMonthlyPoints`. Reset players can retain points on the home screen and monthly leaderboards.

**Fix:** Reset both monthly slots. Also define what happens to existing game checkpoints after a reset; a reset revision would let clients invalidate checkpoints created before the reset. Preserve or clear diagnostic logs deliberately.

### 6. Keep published daily questions immutable — Medium

**Evidence:** `app.js:1089–1104`, `storage.js:349–351`.

Creating a new daily uses a safe claim transaction, but repairing missing question IDs uses a random replacement and an unconditional overwrite. If a pinned question is removed during the day, two clients can generate different replacements; an older client can still use the removed question. A failed repair write is swallowed while that client proceeds with its private replacement set.

**Fix:** Store the day's question snapshots or a versioned question reference when publishing the daily. Keep the published set stable for the whole day. If repair is required, make it transactional and play only the canonical returned result.

### 7. Save Weekly Homework changes reliably — Medium

**Evidence:** `app.js:878–917`, `storage.js:402–404`.

Homework rollover, veto, and unwatch operations update local state, write the entire shared document, and silently ignore save errors. Failed changes look successful until reload. Two devices with stale copies can overwrite each other's picks or watch history. State is refreshed only at boot.

**Fix:** Apply shared changes through transactions or targeted updates; report failed saves and retain the previous visible state. Refresh on app foregrounding and when the homework week changes. Consider explicit “Mark watched” rather than assuming the outgoing assignment was watched.

### 8. Let the trivia home screen load before optional homework — Medium

**Evidence:** `app.js:1841–1863`.

Despite the comment that homework must not block trivia, boot waits for the movie file and homework database read before rendering players. The configured waits can add roughly 26 seconds on a degraded connection: up to ten seconds for movies, followed by two eight-second homework read attempts. A stalled homework write has no application-level deadline.

**Fix:** Render the core game as soon as questions and players are ready, and load homework independently. Give optional features their own loading/retry UI. Wrap Firebase initialization and guard startup local-storage access so a blocked CDN or storage exception leads to a usable error screen instead of stopping script execution.

### 9. Prevent stale asynchronous responses from updating the wrong screen — Medium

**Evidence:** `app.js:793–843`, `app.js:1076–1135`, `app.js:1448–1475`.

Several handlers render after awaited work without checking whether the user changed screens or questions. Rapid leaderboard mode changes can render old-period points under the latest mode. A slow flag submission followed by Next can display “Reported” and disable flagging on the next question. A daily load can finish after the player has navigated away.

**Fix:** Capture player, game, question, and requested period identifiers at the start of each operation. Ignore a response if its target is no longer current. Use request sequence numbers for leaderboard renders and a clear busy state for starting games.

### 10. Prefer unseen questions before reintroducing repeats — Medium improvement

**Evidence:** `game-logic.js:31–35`, `game-logic.js:112–117`, `app.js:30–31`, `storage.js:295`.

When fewer fresh questions remain than the requested game length, selection discards the entire seen-question exclusion. For example, nine unseen questions in a ten-question game do not guarantee those nine will be used. Daily selection has a similar all-or-nothing fallback. Cross-device recent history is also overwritten with the current device's list.

**Fix:** Fill with unseen questions first, then top up with the oldest eligible repeats. Merge recent history inside the player transaction. For daily cooldowns, relax exclusions progressively when the pool gets small.

### 11. Remove repeated facts and calibrate difficulty — Medium content improvement

The structural validator passes, but it does not establish factual novelty or consistent difficulty. Confirmed repeated-fact examples include question IDs 27 and 754, both asking for the villain of The Princess and the Frog, and IDs 47 and 1454, both asking for The Black Cauldron's main villain. The latter pair is labeled hard and medium respectively.

**Fix:** Consolidate repeated facts, review difficulty using actual answer rates, and track a canonical topic/fact identifier. Add optional source and verification-date metadata, particularly for changing park and cruise facts. Treat existing lexical advisory scripts as review aids: the leak scan flags “Hopper” inside “grasshopper,” and the category scan mistakes ordinary “frozen foods” for the film Frozen. Do not auto-apply those results.

### 12. Extend release checks to the failure modes above — Medium maintenance improvement

**Evidence:** `deploy.ps1:109–123`, `scripts/visual_check.py:1–17`.

The existing unit and browser tests provide useful coverage, but the release script runs the pure-rule tests and conditional corpus validation; it does not run the browser smoke suite. The smoke suite substitutes the local adapter and therefore does not verify Firebase authorization, transactions, or conflicts.

**Fix:** Add focused regression checks for the reproduced defects, Firebase emulator tests for duplicate submissions and concurrent daily completions, and browser checks for keyboard access and delayed responses. Run the existing smoke suite in CI with Chromium and WebKit coverage. Retain the project's isolation from production data.

## Further product improvements

- Add a short explanation or interesting fact after an answer, with an optional source link.
- Add a “Practice my missed questions” mode and a weakest-category shortcut.
- Remember difficulty, categories, and question count across visits.
- Display the daily reset time or a countdown, and refresh day-dependent UI when returning from the background. The current fixed 08:00 UTC boundary is not 2 a.m. Mountain year-round; choose and document the intended rule.
- Show “Saving…”, “Saved”, or “Retry save” explicitly on results. Retain a dated pending daily completion even after the next daily begins.
- Provide an admin backup/export and a recoverable reset workflow.
- Consider offline practice as a separate feature only after durable game IDs and retry-safe synchronization exist. The manifest currently supplies install presentation, not offline support.

## Suggested implementation order

First address retry-safe scoring and daily date handling. Verify database access rules in the same first pass. Next fix keyboard access, score reset, immutable dailies, and homework persistence. Then improve startup, async rendering, question repetition, and content quality. Expand regression coverage as each fix lands.
