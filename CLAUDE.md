# Disney Trivia App — Claude Reference

## What This Is
A static single-page trivia app built for Kristen and Cara to practice before a Disney Cruise. No build step, no framework, no package manager.

**Live URL:** https://milo9.github.io/dsny-trivia/
**GitHub repo:** https://github.com/Milo9/dsny-trivia

## File Map
| File | Role |
|---|---|
| `index.html` | Single-page shell. All 5 screens live here as hidden divs. |
| `style.css` | All styling. Dark Disney theme, mobile-first, CSS variables at the top. |
| `app.js` | All game logic. Loaded last. Depends on `storage.js` and the `questions/` shards. |
| `storage.js` | Storage abstraction. `FirebaseAdapter` is active. `LocalStorageAdapter` is kept below it as a fallback. |
| `questions/manifest.json` | Lists the shard filenames. `app.js` fetches this first, then fetches each shard. |
| `questions/q-001.json` | Questions 1–250. |
| `questions/q-002.json` | Questions 251–500. |
| `questions/q-003.json` | Questions 501–800 (210 active; 40 gaps from audit). |
| `questions/q-004.json` | Questions 801–1050 (246 active; 4 gaps from quality pass). |
| `questions/q-005.json` | Questions 1051–1400 (347 active; 3 gaps from quality pass). |
| `review.html` | Standalone admin page for reviewing flagged questions. Shares the same Firestore `flags` collection. |

## The 5 Screens
Screens are `<div class="screen">` elements that get `.hidden` toggled. Only one is visible at a time. Navigation is handled by `showScreen(id)` in `app.js`.

1. `screen-home` — player selection, add new player; shows today's and yesterday's daily challenge comparison cards
2. `screen-settings` — difficulty, categories, question count
3. `screen-game` — active game
4. `screen-results` — score, category breakdown, missed question review
5. `screen-leaderboard` — all players ranked by total points (lifetime)

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

**Adding questions:** Append to the last shard (`questions/q-005.json` is current), one object per line, no pretty-printing. Use the next available integer ID (1401+). Correct answer must be at index 0. When a shard reaches ~250 questions, create the next shard (`q-006.json`, etc.) and add it to `questions/manifest.json` — no change to `index.html` needed.

**Dedup workflow (grep-first, mandatory):** Before writing any new question, grep all shards for 2–3 key terms from the topic. Because each question is one line, a Grep hit returns the entire question + all answers — eyeball it immediately to confirm it's a true duplicate or a distinct angle. Do not read whole shard files for dedup.

**Current count:** 1,343 questions (IDs 1–1400, with ~57 gaps from removed duplicates/errors). Distribution:
- movies 290, characters 205, parks 210, pixar 179, walt 153, music 163, cruise 143

**Removing a question:** Delete its object from the shard JSON. IDs do not need to be contiguous — gaps are fine.

**Local testing note:** `fetch()` is blocked on `file://`. Run a local server to test (`python -m http.server 8000`). On GitHub Pages it works fine.

## Storage Layer — Firebase (active)
User stats and flags are stored in **Firestore**, project `disneytrivia-38ac6`.

Collections:
- `users` — one doc per player, keyed by user ID
- `flags` — one doc per flag report (auto-ID)

Document shape:
```js
// users/{userId}
{ id, name, totalAnswered, totalCorrect, gamesPlayed,
  totalPoints,       // accumulated lifetime points — PRIMARY STATE, not derived (sequence-dependent bonuses make it non-recomputable)
  dailyStreak,       // consecutive days with a daily challenge
  lastDailyDate,     // "YYYY-MM-DD" of last daily played
  lastDailyScore,    // correct count (0–10) in last daily
  lastDailyPoints,   // pts earned in last daily
  prevDailyDate,     // "YYYY-MM-DD" of the daily before last (populated when day rolls)
  prevDailyScore,    // correct count (0–10) for prevDailyDate
  prevDailyPoints,   // pts earned for prevDailyDate
  categoryStats }    // { movies: {answered, correct}, characters: ..., ... } — per-category counters, absent on old docs (treated as {})

// flags/{autoId}
{ questionId, questionText, correctAnswer, allAnswers, difficulty, category,
  reportedBy, comment, timestamp, _resolved? }
```

Stats stored as raw counters (`totalAnswered`, `totalCorrect`, `categoryStats`); percentages are always derived, never stored. `totalPoints` looks like a derived value but is **primary state** — streak and bonus mechanics make it non-recomputable from counters alone. `updateStats` uses a Firestore transaction to avoid race conditions when two players finish at the same time. The `dailyUpdate` payload (score, points, dateKey, streak) and the `catStats` per-category delta are written inside the same transaction so all fields are always consistent.

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

**Manual fallback:**
```
git add -A && git commit -m "your message" && git push
```

## Daily Challenge
A second game mode accessible from the settings screen. Always 10 questions, all categories, no difficulty filter. Uses a deterministic seeded shuffle so **all players see the same questions on a given calendar day**.

- Date key: `"YYYY-MM-DD"` via `dayKey(daysAgo=0)` (or the `todayKey()` wrapper), which subtracts 8h from UTC so the day rolls over at 2am MDT (Mountain Daylight Time) = 4am EDT. This ensures both Eastern and Alberta players always share the same question set. `dayKey(1)` gives yesterday using the same offset — do not compute yesterday via string arithmetic.
- Seed: `dateToSeed(key)` hashes the string; `seededShuffle()` uses an inline mulberry32 step
- Questions are stable-sorted by `id` before shuffling so shard load order doesn't affect results
- Streak (`dailyStreak`, `lastDailyDate`) stored in Firestore on the user doc — cross-device
- Replay is allowed; streak only increments once per calendar day
- Counts toward leaderboard stats just like a regular game
- `gameState.isDaily = true` when a daily challenge is active; `endGame()` checks this flag

New user doc fields (Firestore): `dailyStreak: number`, `lastDailyDate: "YYYY-MM-DD"`. Existing docs without these fields default gracefully (`|| 0` / `|| null`).

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
- Replaying the daily challenge earns base + streak bonus only (no daily bonus for second play)
- Exiting mid-game awards base + streak bonus for answered questions only, no perfect/daily bonus

## Key app.js Globals
| Variable | What it holds |
|---|---|
| `QUESTIONS` | Flat array of all question objects, populated at boot by `loadQuestions()` |
| `currentUser` | The user object selected on the home screen |
| `gameSettings` | `{ difficulty, categories[], questionCount }` — set on settings screen |
| `gameState` | `{ questions[], currentIndex, answers[], score, currentStreak, isDaily, pointsEarned, scoreBreakdown }` — active game |
| `shuffledOpts` | `[{text, originalIndex}]` — display order for current question's answers |

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
1. **Cross-shard duplicate check** — Grep all five shard files for key terms (character name, attraction name, film title) before writing. Because shards are one-question-per-line, each Grep hit shows the full question + answers — no need to open the file. Questions about the same topic often exist already. Easy/obvious topics (Mickey's dog, Donald's nephews, Tinker Bell's dress color, Simba's father) are almost certainly covered — check first.

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
