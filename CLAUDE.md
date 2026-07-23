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
| `questions/q-006.json` | Questions 1302–2017 (250 active). |
| `questions/q-007.json` | Questions 2018–2267 (250 active). |
| `questions/q-008.json` | Questions 2268–2318 (51 active). |
| `movies.json` | Weekly Homework movie pool — flat array of `{id, title, year, studio}`, Disney animated + Pixar canon. Fetched by `app.js` at boot alongside questions. |
| `review.html` | Standalone admin page for reviewing flagged questions. Shares the same Firestore `flags` collection. |
| `scripts/count_topics.py` | Counts questions per Disney/Pixar film (question + correct answer only, not distractors); parent-film counts exclude sequel/short matches, which are reported separately. Run from project root: `python scripts/count_topics.py`. Re-run after large batches of additions to update the Per-film coverage map in this file. |
| `scripts/_common.py` | Shared helpers (corpus loader, text normalization, the `SEQUELS_AND_SHORTS` registry) used by the scripts below. Not run directly. |
| `scripts/recon.py` | Compact `id + question` dump for a keyword/film — token-cheap alternative to reading full Grep hits during pre-draft recon. See Question-Bank Tooling below. |
| `scripts/find_gaps.py` | Novelty gap-finder: distractor-only entities and sequel/short coverage, lowest-covered first. See Question-Bank Tooling below. |
| `scripts/find_near_dupes.py` | Lexical near-duplicate detector, whole-corpus or `--new` against a draft batch. See Question-Bank Tooling below. |
| `scripts/validate_batch.py` | Pre-append sanity check for a drafted batch (IDs, enums, exact dupes, answer-format heuristics). See Question-Bank Tooling below. |

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

**Adding questions:** Append to the last shard (`questions/q-007.json` is current), one object per line, no pretty-printing. Use the next available integer ID (2136+). Correct answer must be at index 0. When a shard reaches ~250 questions, create the next shard (`q-008.json`, etc.) and add it to `questions/manifest.json` — no change to `index.html` needed.

**Dedup workflow (grep-first, mandatory):** Before writing any new question, grep all shards for 2–3 key terms from the topic. Because each question is one line, a Grep hit returns the entire question + all answers — eyeball it immediately to confirm it's a true duplicate or a distinct angle. Do not read whole shard files for dedup. For the initial "has this stem/angle been asked at all" scan on a saturated film, `scripts/recon.py` is a cheaper first pass (compact one-line-per-question digest instead of full Grep hits) — but it hides the correct answer by default (`--show-answer` adds only answers[0], never distractors), so once a candidate stem looks close, confirm with a real Grep hit or `--show-answer` before judging it a true duplicate; recon narrows the search, it doesn't replace the eyeball. Before appending a drafted batch, run `scripts/validate_batch.py` (format/enum/exact-dup checks) and `scripts/find_near_dupes.py --new` (lexical near-duplicate check, new-vs-existing and new-vs-new) — see Question-Bank Tooling below for the full workflow.

**Current count:** 1,722 questions (IDs 1–2318, with gaps from removed duplicates/errors). Distribution (exact, via count_topics.py):
- movies 399, characters 308, parks 257, pixar 246, music 188, walt 180, cruise 144

**Per-film coverage map** (questions that are *about* this film — correct answer or question text, not distractors). **The counts below are a rough signal, not a cap.** A film at 30 can still take a 31st question if the fact is genuinely un-asked — the real gate is always "is this a distinct fact, verified against a grep of the existing stems," never "is the count already high." Treat "Saturated" as "the obvious tier-1 facts are probably taken, go deeper (secondary characters, specific scenes/songs, production trivia, direct-to-video sequels, shorts) rather than skip the film," not as "stop." Under-covered rows are just as likely to reflect the count_topics.py regex undercounting (see note below) as genuinely thin coverage — grep the real stems before assuming either way.

| Film | Count | Status |
|---|---|---|
| Frozen | 49 | Saturated |
| Toy Story | 47 | Saturated |
| Beauty and the Beast | 30 | Saturated |
| The Little Mermaid | 29 | Saturated |
| The Lion King | 29 | Saturated |
| Finding Nemo / Finding Dory | 28 | Saturated |
| Cinderella | 28 | Saturated |
| Aladdin | 24 | Saturated |
| Moana | 22 | Saturated |
| Inside Out | 22 | Saturated |
| Tangled | 21 | Saturated |
| The Incredibles | 20 | Saturated |
| Ratatouille | 19 | Well-covered |
| The Emperor's New Groove | 19 | Well-covered |
| Pocahontas | 18 | Well-covered |
| Encanto | 17 | Well-covered |
| The Hunchback of Notre Dame | 17 | Well-covered |
| Tarzan | 17 | Well-covered |
| Monsters Inc. / Monsters University | 17 | Well-covered |
| Bambi | 17 | Well-covered |
| The Jungle Book | 16 | Well-covered |
| Mulan | 15 | Well-covered |
| Cars | 15 | Well-covered |
| Zootopia | 15 | Well-covered |
| Wreck-It Ralph | 15 | Well-covered |
| Brother Bear | 14 | Well-covered |
| Turning Red | 13 | Well-covered |
| WALL-E | 12 | Well-covered |
| Big Hero 6 | 12 | Well-covered |
| Soul | 12 | Well-covered |
| Brave | 11 | Well-covered |
| A Bug's Life | 11 | Well-covered |
| Inside Out 2 | 11 | Well-covered |
| Elemental | 11 | Well-covered |
| 101 Dalmatians | 11 | Well-covered |
| The Fox and the Hound | 11 | Well-covered |
| Atlantis: The Lost Empire | 10 | Well-covered |
| Hercules | 7 | Under-covered |
| Onward | 6 | Under-covered |
| Luca | 6 | Under-covered |
| Coco | 5 | Under-covered |
| Up | 4 | Under-covered |

These counts still fold numbered theatrical sequels into their parent row (Frozen includes Frozen II, Toy Story includes 2–4, etc.) since that's one continuously-active franchise, not a stale catalog title. **Direct-to-video sequels and shorts are excluded from the parent row and tracked separately** — run `python scripts/count_topics.py` for their counts or `python scripts/find_gaps.py --sequels` for the same list sorted lowest-coverage-first. A direct-to-video sequel or short at or near zero is wide open even when the row above it says Saturated; see `scripts/_common.py:SEQUELS_AND_SHORTS` for the tracked list (Lion King II, Return of Jafar, King of Thieves, Little Mermaid II, Mulan II, Pocahontas II, Hunchback II, Cinderella II/III, Brother Bear 2, 101 Dalmatians II, Jungle Book 2, Tarzan II, Fox and the Hound 2, Kronk's New Groove, Bambi II, Frozen Fever, Olaf's Frozen Adventure, Geri's Game, Piper, Bao).

This table is updated manually; re-run `scripts/count_topics.py` to regenerate it after large batches of additions. Note: the script's keyword regexes only match question text + correct answer, and require fairly specific phrase co-occurrence (e.g. Coco requires `coco`+`pixar` or `miguel`+`guitar` etc. in the same string) — some films are likely undercounted relative to their true coverage; treat this table as a floor, not an exact census.

**Duplicate audit (2026-07-21):** Players reported near-duplicate questions — same fact tested with reworded question text (not exact text matches). Ran a script-assisted audit: grouped all questions by normalized correct answer (ignoring honorifics/articles) plus a film/category-blocked word-overlap pass, then manually reviewed ~150 candidate clusters to separate true duplicates (same fact, reworded) from coincidental matches (different facts that happen to share an answer, e.g. two unrelated questions both answering "1971"). Removed 116 true duplicates, always keeping the better-worded/more-accurately-categorized copy. This is a one-time cleanup — the existing grep-first dedup workflow above remains the process for preventing new duplicates.

**Content generation strategy (2026-07-21, revised same day):** An initial attempt to add 250 questions from memory recall landed at only 72 clean ones — memory of "obvious" facts per film runs out fast in a bank this size. Revised approach, which then added a further 135 questions cleanly in one sitting: **generate WebSearch-primary, not memory-primary.** Research a film/topic's plot, characters, and production details via search, then harvest the facts not already in the bank from that same reading — the source you're reading from doubles as the verification, so this is nearly free of the hallucination risk memory-only drafting carries. One search reliably yields enough material for 5–10 questions. The richest under-mined veins turned out to be: direct-to-video sequels (The Lion King II, Return of Jafar/King of Thieves, Little Mermaid II, Mulan II, Pocahontas II, Hunchback II, Cinderella III, Brother Bear 2, 101 Dalmatians II, Jungle Book 2, Tarzan II, Fox and the Hound 2, Kronk's New Groove, Bambi II — nearly all had zero prior coverage), theatrical shorts (Frozen Fever, Olaf's Frozen Adventure, Geri's Game, Piper, Bao), classic package-film segments (Three Caballeros, Fun and Fancy Free, Fantasia/Fantasia 2000 segments beyond the two or three already covered), specific songs that only ever appeared as wrong-answer distractors and were never the actual target of a question, and verified post-2023 park/cruise facts. Still corroborate surprising specifics (dates, "first/only" claims, exact figures) — two invented-sounding facts were caught and fixed this way before deploy (see git log). The dedup gate is unchanged and non-negotiable: recon-first grep, then an end-of-batch answer-normalized pass covering new-vs-new AND new-vs-existing, PLUS an ignore-thresholds same-answer0 dump (a real duplicate — WALL-E's Axiom ship name — slipped past the thresholded pass in the first round and was only caught this way).

**Content expansion (2026-07-21):** Added 72 new questions (IDs 1553–1624, gaps intentional) after discovering the bank is far more comprehensively mined than raw per-film counts suggest — grepping candidate films before drafting repeatedly turned up existing coverage of the "obvious" facts, even for films the coverage table shows as under-covered. The effective workflow that worked: grep/dump existing coverage for a whole category or film *before* drafting a single question (not after), harvest only facts you're fully certain of, and WebSearch-verify anything post-2023 (new cruise ships, recent park changes) rather than guessing. A dedup pass (answer-normalized, new-vs-new and new-vs-existing) at the end caught 3 genuine duplicates a per-topic grep had missed. This is why the batch landed at 72 rather than a pre-set target — see the deploy notes/commit for the honest accounting.

**Content expansion (2026-07-23):** User asked for 500 new questions; landed at 183 clean (IDs 2136–2318) after generating 185 and cutting 2 true near-duplicates at the merge gate — 500 was never realistic for a single sitting given how mined the bank already was (see the 72/135 precedents above), and padding toward a number would have meant shipping unverified or duplicate content, which the project's dedup gate exists to prevent. **Parallelized via 10 fork agents**, each given a disjoint topic bucket (under-covered classics: Bambi/Brother Bear/Hercules/Fox and the Hound; under-covered Pixar: Soul/Onward/Luca/Coco/Up; direct-to-video sequels & shorts, including Cinderella II: Dreams Come True which had zero prior coverage; parks split three ways — WDW Magic Kingdom+EPCOT, WDW Hollywood Studios+Animal Kingdom+Disneyland/DCA, international parks; Walt/company history; Disney Cruise Line; music; and a secondary-character deep dive using the distractor-only gap report) so each fork's WebSearch-verify-then-draft work stayed independent and out of the main context. **Coordination lesson:** parallel forks can't see each other's drafts, so new-vs-new duplication across forks — not new-vs-existing — was the real risk; each fork wrote to its own scratch file with non-colliding placeholder IDs (bucket-prefixed, e.g. 91000s, 92000s), and the dedup/validation gate ran exactly once on the concatenated union of all 10 files before any renumbering or shard append, which is what caught the two cross-fork-adjacent true duplicates (a Carousel of Progress identification question redundant with existing #369, and a Grimsby/Vanessa question redundant with existing #822 — both same fact as an existing question, different surface wording). Also fixed two pre-existing miscategorized entries found incidentally by a fork during recon (#2076 Frozen Fever and #2133 The Emperor's New Groove were tagged `pixar`; both are Disney, not Pixar — corrected to `movies`). Added a new shard, `questions/q-008.json`, since q-007 filled to 250. Category "walt" and cruise-ship-restaurant/venue trivia were confirmed as the most heavily mined non-film categories — clean yield there came from corporate-history and stage-show angles rather than core biography/ship-amenity facts, which are close to exhausted.

**Removing a question:** Delete its object from the shard JSON. IDs do not need to be contiguous — gaps are fine.

**Local testing note:** `fetch()` is blocked on `file://`. Run a local server to test (`python -m http.server 8000`). On GitHub Pages it works fine.

## Question-Bank Tooling (scripts/)
All scripts are read-only against the shards — they print reports/candidates for a human to eyeball, they never edit shard JSON (adding/removing a question is still always a manual shard edit, per the rule below). Run from the project root with `python scripts/<name>.py`.

| Script | Purpose |
|---|---|
| `recon.py <regex>` | `id + question` dump for a keyword/film — a token-cheap first pass over full Grep hits during the mandatory pre-draft recon scan. Hides answers by default (`--show-answer` adds only the correct answer, never distractors) — good for "has this stem/angle been asked," not a substitute for a real Grep hit when judging whether a specific fact+answer is already covered. `--all-fields` also searches wrong answers. **Read the full digest for the topic you're drafting about, not just what `find_near_dupes.py` algorithmically flags** — a film is usually 15–40 lines, cheap to read end-to-end with semantic intent. This is the actual catch for "same fact, different answer wording" (e.g. "What weapon is X skilled with? → Bow and arrow" vs. "X's signature skill? → Archery") — no lexical script can judge that two answer strings mean the same thing, only a read can. |
| `find_gaps.py` | Two novelty reports: distractor-only entities (names/terms that have appeared as a wrong answer but never as a correct one — candidate seeds for new questions) and sequel/short coverage counts, lowest first. Run before drafting to find genuinely unmined material instead of relying on memory for what's "obviously" missing. `--distractors` / `--sequels` isolates one report; `--min-count`/`--limit` tune the distractor report (expect some noise — generic words and colors show up; it's advisory, not a verdict). |
| `find_near_dupes.py` | Lexical near-duplicate detector. No args = whole-corpus self-audit (same method as the 2026-07-21 audit below, but scriptable/repeatable) — groups above `--max-group-size` (default 6) are skipped as likely just a common name. `--new drafts.json` checks a drafted batch against the existing corpus and against itself before appending; Pass B is NOT size-capped in this mode, since output is already scoped to groups touching the draft — capping there would hide exactly the "draft answer matches a common existing answer, worded differently" case this pass exists to catch. Two passes: question-text Jaccard similarity (`--threshold`, default 0.5, tokens lightly stemmed so "kitten"/"kittens" or "sings"/"singing" count as the same token) catches reworded restatements; same-normalized-answer grouping catches same-fact-different-wording that a text-similarity threshold can miss (Pass B is also why this tool independently catches most "semantically equivalent, low word overlap" dupes — same fact usually means same correct answer, regardless of phrasing). Catches lexical overlap only — semantically-equivalent questions with **low word overlap AND a differently-worded answer** (e.g. "bow and arrow" vs. "archery") still need a human read; see the recon.py note below for how that residual case gets caught. Always eyeball flagged pairs; a shared answer or wording doesn't automatically mean duplicate (e.g. two different songs both answering "Pocahontas"). |
| `validate_batch.py drafts.json` | Pre-append sanity check: valid JSON, ID collisions (against the corpus and within the batch), next-available-ID, category/difficulty enum membership, exact-duplicate question text, and advisory heuristics for the Answer structure rules below (sentence-like answers, answer text leaking into the question). Exits non-zero on errors. |
| `count_topics.py` | Per-film coverage counts — see Per-film coverage map below. |

**Recommended batch workflow:** `recon.py` (and/or `find_gaps.py` for topic ideas) — read the full digest for the topic, not just a skim, since that's what catches same-fact-different-answer-wording duplicates no script can — to confirm a fact isn't already covered → draft the batch as a scratch JSON file → `validate_batch.py` → `find_near_dupes.py --new` → append the survivors to the current shard, bump IDs/counts in this file.

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

**Cache-busting for code files:** `index.html` loads `style.css`, `storage.js`, and `app.js` with a `?v=` query string matching `APP_VERSION` (currently 1.21). When making code changes, bump `APP_VERSION` in `app.js` **and** update the matching `?v=` strings in `index.html` so browsers discard their cached copies. Question shard files and `movies.json` (fetched via `fetch()`) use `{ cache: 'no-cache' }` and don't need manual versioning.

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
- **Exit mid-daily → resume, don't restart.** Nothing is committed to Firestore stats until all 10 are answered. Exiting locks in the answered-so-far questions to `localStorage` (`disney_daily_progress_{userId}`, via `saveDailyProgress`/`getDailyProgress`/`clearDailyProgress` in `app.js`) — not Firestore, so this is per-device, like the other `disney_*` localStorage keys. Re-opening the Daily Challenge (`buildDailyGameState()`) resumes at the next unanswered question with the locked-in answers' score/streak already applied; those questions are never re-shown or re-editable. If a resume's saved answers no longer line up position-by-position with today's pinned questions (e.g. a backfill re-pinned the day after the exit), only the still-matching prefix is kept and the rest is treated as unanswered — never silently miscounted. Progress is cleared only after a successful Firestore save in `endGame()`; if that save fails (offline), progress is kept and the next "Daily Challenge" tap detects the already-complete answer set and retries `endGame()` directly instead of restarting the game. The settings screen shows a "▶️ Resume Daily Challenge (n/10)" state (reading the same localStorage progress) so a mid-exit isn't silently invisible. `endGame()` sets `gameState.ended` as a re-entrancy guard so a double-click on the final question (or two near-simultaneous resume-complete calls) can't double-commit stats.
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
Points are computed by `scoreBreakdown(answers, earnDailyBonus, dailyStreak, awardPerfect = true)` in `app.js` and stored atomically to Firestore inside the `updateStats` transaction. `awardPerfect` is passed `false` only from the mid-game exit handler — otherwise "all answered so far were correct" on a partial (unfinished) set would incorrectly earn the perfect-game bonus. Earning formula:

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
