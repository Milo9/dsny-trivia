# Disney Trivia App — Claude Reference

## What This Is
A static single-page trivia app built for Kristen and Cara to practice before a Disney Cruise. No build step, no framework, no package manager.

**Live URL:** https://milo9.github.io/dsny-trivia/
**GitHub repo:** https://github.com/Milo9/dsny-trivia

## File Map
| File | Role |
|---|---|
| `index.html` | Single-page shell. All 6 screens live here as hidden divs. |
| `style.css` | All styling. Dark Disney theme, mobile-first, CSS variables at the top. |
| `app.js` | All game logic. Loaded last. Depends on `storage.js` and the `questions/` shards. |
| `storage.js` | Storage abstraction. `FirebaseAdapter` is active. `LocalStorageAdapter` is kept below it as a fallback. |
| `questions/manifest.json` | Lists the shard filenames. `app.js` fetches this first, then fetches each shard. |
| `questions/q-001.json` | Questions 1–250 (249 active). |
| `questions/q-002.json` | Questions 251–500 (245 active). |
| `questions/q-003.json` | Questions 501–799 (222 active; gaps from audit and dedup passes). |
| `questions/q-004.json` | Questions 801–1050 (246 active). |
| `questions/q-005.json` | Questions 1051–1300 (247 active). |
| `questions/q-006.json` | Questions 1302–1550 (239 active). |
| `movies.json` | Weekly Homework movie pool — flat array of `{id, title, year, studio}`, Disney animated + Pixar canon. Fetched by `app.js` at boot alongside questions. |
| `review.html` | Standalone admin page for reviewing flagged questions. Shares the same Firestore `flags` collection. |
| `scripts/count_topics.py` | Counts questions per Disney/Pixar film (question + correct answer only, not distractors). Run from project root: `python scripts/count_topics.py`. Re-run after large batches of additions to update the Per-film coverage map in this file. |

## The 6 Screens
Screens are `<div class="screen">` elements that get `.hidden` toggled. Only one is visible at a time. Navigation is handled by `showScreen(id)` in `app.js`.

1. `screen-home` — player selection, add new player; shows today's and yesterday's daily challenge comparison cards, plus the Weekly Homework card (this week's assigned movie)
2. `screen-settings` — difficulty, categories, question count; daily button becomes "Review Today's Questions" after the player has played
3. `screen-game` — active game
4. `screen-results` — score, category breakdown, missed question review; shows "Review All Questions" button for daily games
5. `screen-daily-review` — all 10 daily questions with each player's answer and the correct answer; reachable from results (after playing today), settings daily button (once played today), or the "View Questions →" link on yesterday's home card; title updates dynamically (Today's Review / Yesterday's Review)
6. `screen-leaderboard` — all players ranked by total points (lifetime)

## Question Format
```js
{
  id: 1,                        // unique integer, never reuse
  question: "Question text?",
  answers: ["Correct", "Wrong1", "Wrong2", "Wrong3"],  // correct answer is always index 0; app.js shuffles display order
  difficulty: "easy",           // "easy" | "medium" | "hard"
  category: "movies"            // see categories below
}
```

**Categories:** `movies` | `characters` | `parks` | `walt` | `cruise` | `music` | `pixar`

**No TV shows** — the requirement explicitly excludes Disney Channel, streaming series, etc. This is easy to accidentally violate (Mandalorian, WandaVision, DuckTales reboot, etc.) — hold the line.

**Shard format:** Each shard is a JSON array with **one question object per line** (compact, not pretty-printed). `app.js` loads shards via `r.json()` so indentation is irrelevant to the app. The compact format means each line contains the full question + all answers, making Grep results immediately useful for duplicate checking without reading whole files.

Example line:
```
{"id": 1, "question": "What color is Cinderella's iconic ball gown?", "answers": ["Blue", "Pink", "Yellow", "White"], "difficulty": "easy", "category": "movies"},
```

**Adding questions:** Append to the last shard (`questions/q-006.json` is current), one object per line, no pretty-printing. Use the next available integer ID (1551+). Correct answer must be at index 0. When a shard reaches ~250 questions, create the next shard (`q-007.json`, etc.) and add it to `questions/manifest.json` — no change to `index.html` needed.

**Dedup workflow (grep-first, mandatory):** Before writing any new question, grep all shards for 2–3 key terms from the topic. Because each question is one line, a Grep hit returns the entire question + all answers — eyeball it immediately to confirm it's a true duplicate or a distinct angle. Do not read whole shard files for dedup.

**Current count:** 1,332 questions (IDs 1–1550, with ~218 gaps from removed duplicates/errors — 116 near-duplicates removed in a 2026-07-21 dedup audit, see below). Distribution (exact, via count_topics.py):
- movies 311, parks 203, pixar 191, characters 188, music 167, walt 150, cruise 122

**Per-film coverage map** (questions that are *about* this film — correct answer or question text, not distractors). Saturated films (≥20) need a genuinely fresh angle before adding more. Well-covered (10–19) are fine for clearly distinct questions. Under-covered (<10) are welcome territory.

| Film | Count | Status |
|---|---|---|
| Toy Story | 34 | Saturated |
| Frozen | 30 | Saturated |
| The Lion King | 29 | Saturated |
| The Little Mermaid | 28 | Saturated |
| Finding Nemo / Finding Dory | 23 | Saturated |
| Beauty and the Beast | 21 | Saturated |
| Moana | 19 | Well-covered |
| Aladdin | 19 | Well-covered |
| Inside Out | 19 | Well-covered |
| Pocahontas | 17 | Well-covered |
| Encanto | 17 | Well-covered |
| Tangled | 17 | Well-covered |
| Mulan | 15 | Well-covered |
| The Hunchback of Notre Dame | 15 | Well-covered |
| Tarzan | 15 | Well-covered |
| The Incredibles | 14 | Well-covered |
| The Emperor's New Groove | 13 | Well-covered |
| Ratatouille | 12 | Well-covered |
| Monsters Inc. / Monsters University | 11 | Well-covered |
| Brave | 11 | Well-covered |
| Cars | 11 | Well-covered |
| Wreck-It Ralph | 11 | Well-covered |
| Turning Red | 11 | Well-covered |
| Big Hero 6 | 10 | Well-covered |
| Atlantis: The Lost Empire | 10 | Well-covered |
| WALL-E | 9 | Under-covered |
| Zootopia | 9 | Under-covered |
| Inside Out 2 | 8 | Under-covered |
| Elemental | 8 | Under-covered |
| A Bug's Life | 7 | Under-covered |
| Hercules | 7 | Under-covered |
| Soul | 7 | Under-covered |
| Onward | 5 | Under-covered |
| Luca | 5 | Under-covered |
| Coco | 4 | Under-covered |
| Up | 4 | Under-covered |

This table is updated manually; re-run `scripts/count_topics.py` (see below) to regenerate it after large batches of additions. Note: the script's keyword regexes only match question text + correct answer, and require fairly specific phrase co-occurrence (e.g. Coco requires `coco`+`pixar` or `miguel`+`guitar` etc. in the same string) — some films are likely undercounted relative to their true coverage; treat this table as a floor, not an exact census.

**Duplicate audit (2026-07-21):** Players reported near-duplicate questions — same fact tested with reworded question text (not exact text matches). Ran a script-assisted audit: grouped all questions by normalized correct answer (ignoring honorifics/articles) plus a film/category-blocked word-overlap pass, then manually reviewed ~150 candidate clusters to separate true duplicates (same fact, reworded) from coincidental matches (different facts that happen to share an answer, e.g. two unrelated questions both answering "1971"). Removed 116 true duplicates, always keeping the better-worded/more-accurately-categorized copy. This is a one-time cleanup — the existing grep-first dedup workflow above remains the process for preventing new duplicates.

**Removing a question:** Delete its object from the shard JSON. IDs do not need to be contiguous — gaps are fine.

**Local testing note:** `fetch()` is blocked on `file://`. Run a local server to test (`python -m http.server 8000`). On GitHub Pages it works fine.

## Storage Layer — Firebase (active)
User stats and flags are stored in **Firestore**, project `disneytrivia-38ac6`.

Collections:
- `users` — one doc per player, keyed by user ID
- `flags` — one doc per flag report (auto-ID)
- `dailies` — one doc per calendar day, keyed by `"YYYY-MM-DD"` date key; stores `{ questionIds: [id, ...] }` written by the first player who plays that day
- `weeklyHomework` — single doc `state`; stores the current Weekly Homework movie pick (see below)

Document shape:
```js
// users/{userId}
{ id, name, totalAnswered, totalCorrect, gamesPlayed,
  totalPoints,        // accumulated lifetime points — PRIMARY STATE, not derived (sequence-dependent bonuses make it non-recomputable)
  dailyStreak,        // consecutive days with a daily challenge
  lastDailyDate,      // "YYYY-MM-DD" of last daily played
  lastDailyScore,     // correct count (0–10) in last daily
  lastDailyPoints,    // pts earned in last daily
  lastDailyAnswers,   // [{questionId, correct, selectedText}] — per-question picks from last daily; used by screen-daily-review
  prevDailyDate,      // "YYYY-MM-DD" of the daily before last (populated when day rolls)
  prevDailyScore,     // correct count (0–10) for prevDailyDate
  prevDailyPoints,    // pts earned for prevDailyDate
  prevDailyAnswers,   // [{questionId, correct, selectedText}] — per-question picks shifted from lastDailyAnswers when day rolls
  categoryStats }     // { movies: {answered, correct}, characters: ..., ... } — per-category counters, absent on old docs (treated as {})

// flags/{autoId}
{ questionId, questionText, correctAnswer, allAnswers, difficulty, category,
  reportedBy, comment, timestamp, _resolved? }

// weeklyHomework/state
{ weekKey,   // "YYYY-MM-DD" of the Thursday this pick belongs to, from homeworkWeekKey()
  movieId,   // id into movies.json for the current pick
  pickedAt,  // ISO timestamp of the last pick/shuffle
  watched }  // [{id, watchedAt}, ...] movies already assigned in a past week, with the date
             // watched — excluded from future picks and rendered as watch history.
             // Older docs may have a bare `watchedIds:[id,...]` instead; app.js's
             // normalizeHomeworkState() upgrades that shape in memory on read.
             // NOT seed-derived like the daily challenge — watched-exclusion and the
             // shuffle veto make the pick stateful and non-reproducible. Do not "simplify"
             // this back to a deterministic weekly shuffle.
```

Stats stored as raw counters (`totalAnswered`, `totalCorrect`, `categoryStats`); percentages are always derived, never stored. `totalPoints` looks like a derived value but is **primary state** — streak and bonus mechanics make it non-recomputable from counters alone. `updateStats` uses a Firestore transaction to avoid race conditions when two players finish at the same time. The `dailyUpdate` payload (score, points, dateKey, streak, answers) and the `catStats` per-category delta are written inside the same transaction so all fields are always consistent.

**Firebase console:** https://console.firebase.google.com/project/disneytrivia-38ac6

**Switching back to localStorage:** Change the last line of `storage.js` from `new FirebaseAdapter()` to `new LocalStorageAdapter()`. The rest of the app is unaffected.

**Firestore security rules** (currently set to open — URL is the only guard for this private family app):
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

## Flag / Review System
- Players tap **👎 Flag** after answering to report a bad question
- Stored in Firestore `flags` collection via `storage.flagReport()`
- `review.html` is the admin triage page — open it at https://milo9.github.io/dsny-trivia/review.html
- After fixing a question in the appropriate shard JSON, mark the flag Resolved in `review.html`
- Flagging does NOT auto-remove the question; that's always a manual edit to the shard JSON

## Deploying Changes
The app is hosted on GitHub Pages from the `main` branch. Use the deploy script:

```powershell
.\deploy.ps1 -Message "your commit message"
```

`deploy.ps1` stages all changes, commits, and pushes in one step. Omitting `-Message` defaults to `"update app"`. GitHub Pages redeploys automatically within ~1 minute.

**Cache-busting for code files:** `index.html` loads `style.css`, `storage.js`, and `app.js` with a `?v=` query string matching `APP_VERSION` (currently 1.18). When making code changes, bump `APP_VERSION` in `app.js` **and** update the matching `?v=` strings in `index.html` so browsers discard their cached copies. Question shard files and `movies.json` (fetched via `fetch()`) use `{ cache: 'no-cache' }` and don't need manual versioning.

**Manual fallback:**
```
git add -A && git commit -m "your message" && git push
```

## Daily Challenge
A second game mode accessible from the settings screen. Always 10 questions, all categories, no difficulty filter. Uses a deterministic seeded shuffle so **all players see the same questions on a given calendar day**.

- Date key: `"YYYY-MM-DD"` via `dayKey(daysAgo=0)` (or the `todayKey()` wrapper), which subtracts 8h from UTC so the day rolls over at 2am MDT (Mountain Daylight Time) = 4am EDT. This ensures both Eastern and Alberta players always share the same question set. `dayKey(1)` gives yesterday using the same offset — do not compute yesterday via string arithmetic.
- **Pinned question IDs**: When the first player starts the daily challenge, the 10 question IDs are written to `dailies/{dateKey}` in Firestore. Every subsequent player (and the review screen) reads from this doc, so everyone plays the same questions regardless of question deploys that happen later in the day. `getDailyPins(dateKey)` / `saveDailyPins(dateKey, ids)` in `storage.js`.
  - If a pinned ID no longer exists in the shards by the time someone reads it (e.g. it was removed as a duplicate after being pinned), the game-start handler backfills the missing slot(s) from the live pool and re-saves the pins so the day stays at its original count; the review screen instead just omits the missing question (it can't reconstruct what a removed question's text/choices were, so a day whose pins referenced a since-deleted question may show fewer than 10 entries in review — this is expected, not a bug).
- Seed: `dateToSeed(key)` hashes the string; `seededShuffle()` uses an inline mulberry32 step
- Questions are stable-sorted by `id` before shuffling so shard load order doesn't affect results
- Streak (`dailyStreak`, `lastDailyDate`) stored in Firestore on the user doc — cross-device
- **Replay is blocked** — each player can play the daily exactly once per calendar day. The settings button becomes "📋 Review Today's Questions" after playing; the results-screen Rematch button is hidden for daily games.
- Per-question answers stored in Firestore as `lastDailyAnswers` on first play; shifted to `prevDailyAnswers` when the next day's challenge is played. Used by `screen-daily-review` for both today and yesterday views.
- Counts toward leaderboard stats just like a regular game
- `gameState.isDaily = true` when a daily challenge is active; `endGame()` checks this flag

New user doc fields (Firestore): `dailyStreak: number`, `lastDailyDate: "YYYY-MM-DD"`, `lastDailyAnswers: [{questionId, correct, selectedText}]`. Existing docs without these fields default gracefully.

## Weekly Homework
A tongue-in-cheek "assignment" feature: a Disney/Pixar movie is picked for family movie night, refreshed every Thursday. Movie pool lives in `movies.json`; pick state lives in Firestore `weeklyHomework/state` (see Document shape above). Card shows on `screen-home`.

- **Not seed-derived.** Unlike the daily challenge, the pick is not deterministic from a seed — watched-exclusion and the shuffle veto make it genuinely stateful. `rollHomeworkIfStale()` reads the stored state; if it's absent or belongs to a past week, it rolls to a new one.
- **Week boundary:** `homeworkWeekKey()` reuses the daily challenge's 8h-UTC-shift trick to roll over at 08:00 UTC = 3am EST / 4am EDT **Thursday**, returning that Thursday's date key. Like the daily challenge, this is a client-triggered check on app load — there is no server-side cron. The new week's movie is picked (and written to Firestore) by whichever player's device happens to load the app first after the boundary passes.
- **Rollover vs. shuffle — two separate code paths, not a shared helper:**
  - `rollHomeworkIfStale()` (boot-time, automatic): the outgoing movie is assumed watched ("homework complete") and pushed onto `watchedIds`, then a new movie is drawn from the unwatched pool.
  - `shuffleHomework()` (manual veto button): draws a new movie excluding `watchedIds` **and** the current pick, but does **not** touch `watchedIds` — a vetoed movie goes back into the pool for a future week.
- **Pool exhaustion:** if every movie is watched, `pickFromMoviePool()` resets and draws from the full pool again (`watchedIds` cleared in the caller).
- **Kristen-only shuffle:** the 🔀 Shuffle button (`#btn-shuffle-homework`) is shown only when `currentUser.id === 'kristen'` — i.e. she has actually selected her own card *this session*. It deliberately does not key off `localStorage.disney_last_user`, since that persists across sessions on a shared device and would show the button to anyone opening the app after Kristen last used it, before they'd selected a player at all this session (this caused an accidental shuffle). Still a loose, client-side-only gate consistent with the rest of the app's security model — it's a light veto-power joke for a 2-person household, not access control.
- **Full movie list:** a `🎬 View Full Movie List` toggle (`#btn-toggle-watched`) expands `#homework-watched-list`, showing the *entire* pool as two groups (current week's pick is excluded from both — it's already shown above):
  - **✅ Watched** — sorted newest-watched first (`watchedAt` descending), each row has an ✕. Clicking it calls `removeFromWatched(movieId)`, pulling that entry out of `watched` and saving — the movie goes back in the pool for future picks/shuffles.
  - **🍿 Not Yet Assigned** — everything else, alphabetical, read-only.
  - **Open to any player, no Kristen gate** on the ✕ (unlike shuffle).
- Graceful degradation: if `movies.json` or the Firestore read fails, the card just stays hidden (`init()` catches the error separately from question loading so a homework failure never blocks the trivia app itself).

## Sound Effects
Web Audio API (synthesized, no audio files). Wrapped in the `sounds` IIFE in `app.js`:

- `sounds.correct()` — two-note ascending chime (C5 → E5)
- `sounds.wrong()` — single low triangle-wave thud (A3)
- `sounds.fanfare()` — C major arpeggio (C5→E5→G5→C6), plays at results screen
- `sounds.toggle()` — flip muted state; persists in `localStorage` key `disney_sound_muted`
- Mute button (🔊/🔇) is in the game screen top bar next to Exit

## Scoring System
Points are computed by `scoreBreakdown(answers, earnDailyBonus, dailyStreak)` in `app.js` and stored atomically to Firestore inside the `updateStats` transaction. Earning formula:

| Component | Value |
|---|---|
| Correct answer — easy | 100 pts |
| Correct answer — medium | 150 pts |
| Correct answer — hard | 200 pts |
| In-game streak bonus (run ≥ 3) | +25 per correct while streak holds |
| Perfect game (all correct) | +500 pts |
| Daily challenge completion (first play of day) | +200 pts flat |
| Daily streak scaling (first play of day) | +10 × min(dailyStreak, 30) |

- `SCORING` constant object in `app.js` holds all values — edit there to rebalance
- `scoreBreakdown()` returns `{ base, streakBonus, perfectBonus, dailyBonus, total }`
- Leaderboard sorts by `totalPoints` descending; percentage is the secondary tiebreaker
- Results screen shows full breakdown when more than one component contributed
- Exiting mid-game awards base + streak bonus for answered questions only, no perfect/daily bonus

## Key app.js Globals
| Variable | What it holds |
|---|---|
| `QUESTIONS` | Flat array of all question objects, populated at boot by `loadQuestions()` |
| `MOVIES` | Flat array of all movie objects, populated at boot by `loadMovies()` |
| `currentUser` | The user object selected on the home screen |
| `gameSettings` | `{ difficulty, categories[], questionCount }` — set on settings screen |
| `gameState` | `{ questions[], currentIndex, answers[], score, currentStreak, isDaily, pointsEarned, scoreBreakdown }` — active game |
| `shuffledOpts` | `[{text, originalIndex}]` — display order for current question's answers |
| `homeworkState` | `{ weekKey, movieId, pickedAt, watched: [{id, watchedAt}] }` — this week's Weekly Homework pick, mirrors Firestore `weeklyHomework/state` |

## Styling Conventions
- CSS variables defined in `:root` at the top of `style.css` — use these, don't hardcode colors
- Key variables: `--bg`, `--bg-card`, `--bg-hover`, `--border`, `--primary`, `--gold`, `--green`, `--red`, `--text`, `--muted`
- Border-radius variables: `--r` (cards), `--r-sm` (buttons/inputs)
- All new screens follow the pattern: `.screen` div → `screen-header` → content → actions at bottom
- Mobile-first. Max width 480px centered. Test at 375px (iPhone SE) as the floor.

## Players
Default users seeded on first load: **Kristen** and **Cara**. Seeding is in `FirebaseAdapter._seed()` — it checks if the doc exists before writing, so it's safe to run on every page load. Do not remove them from the seed.

## Question Quality Rules (Lessons from Audits)

These rules were derived from real mistakes found during shard audits. Follow them every time questions are generated.

**Before adding any new question:**
1. **Cross-shard duplicate check** — Grep all shard files for key terms (character name, attraction name, film title) before writing. Because shards are one-question-per-line, each Grep hit shows the full question + answers — no need to open the file. Questions about the same topic often exist already. Easy/obvious topics (Mickey's dog, Donald's nephews, Tinker Bell's dress color, Simba's father) are almost certainly covered — check first. Also check the Per-film coverage map above: if a film is Saturated (≥20), skip it unless the angle is clearly distinct from what's there.

**Answer structure:**
2. **Never embed the answer in the question text.** If the question says "What type of animal is Geppetto's cat?" and the answer is "Figaro is a kitten," the word "cat" telegraphs the answer. Ask "What is the name of Geppetto's kitten?" instead.
3. **Never include explanatory prose in answer strings.** Answers must be short noun phrases, not sentences. Bad: `"Figaro is a kitten"`. Good: `"Figaro"`.
4. **Never use "All of the above" as a wrong answer** if all the listed options could plausibly be correct. Verify that wrong answers are actually wrong before using them.
5. **Wrong answers must be wrong.** If a question lists three "wrong" options and all three happen to be correct real-world answers, the question is broken. Replace them with genuinely incorrect options.

**Factual accuracy:**
6. **Avoid time-sensitive superlatives.** Phrases like "newest," "latest," or "most recent" become false when new things launch. Name the specific year instead: "the ship that launched in 2022" rather than "the newest ship."
7. **Verify ride/attraction names and statuses.** Brandings change — Rock 'n' Roller Coaster dropped "Starring Aerosmith" at WDW in 2024; Splash Mountain became Tiana's Bayou Adventure in 2024. Check before writing.
8. **Verify ship-specific facts.** DCL restaurant and venue names vary by ship (After Hours on Magic/Wonder, The District on Dream, Europa on Fantasy, Enchanté on Wish). Never write a question about "the adult area on Disney ships" — pin it to a specific ship.

**Category:**
9. **Pixar films use `pixar`, not `movies`.** Brave, Coco, Up, Inside Out, Finding Dory, Onward, Luca, Elemental, Toy Story, Monsters Inc., A Bug's Life, Cars, Ratatouille, WALL-E — all are `pixar`. If in doubt, check whether Pixar Animation Studios is the credited studio.

## What NOT to Do
- Do not introduce a build step, bundler, or npm unless explicitly asked
- Do not add a backend or server — this is intentionally fully static
- Do not store derived values (percentages) — always compute from raw counters
- Do not add TV show questions
- Do not reuse question IDs
