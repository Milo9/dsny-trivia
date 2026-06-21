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
| `app.js` | All game logic. Loaded last. Depends on `questions.js` and `storage.js`. |
| `storage.js` | Storage abstraction. `FirebaseAdapter` is active. `LocalStorageAdapter` is kept below it as a fallback. |
| `questions.js` | 500 trivia questions as a `const QUESTIONS` array. |
| `review.html` | Standalone admin page for reviewing flagged questions. Shares the same Firestore `flags` collection. |

## The 5 Screens
Screens are `<div class="screen">` elements that get `.hidden` toggled. Only one is visible at a time. Navigation is handled by `showScreen(id)` in `app.js`.

1. `screen-home` — player selection, add new player
2. `screen-settings` — difficulty, categories, question count
3. `screen-game` — active game
4. `screen-results` — score, category breakdown, missed question review
5. `screen-leaderboard` — all players ranked by correct-answer percentage

## Question Format
```js
{
  id: 1,                        // unique integer, never reuse
  question: "Question text?",
  answers: ["Correct", "Wrong1", "Wrong2", "Wrong3"],
  correct: 0,                   // always index 0; app.js shuffles display order
  difficulty: "easy",           // "easy" | "medium" | "hard"
  category: "movies"            // see categories below
}
```

**Categories:** `movies` | `characters` | `parks` | `walt` | `cruise` | `music` | `pixar`

**No TV shows** — the requirement explicitly excludes Disney Channel, streaming series, etc. This is easy to accidentally violate (Mandalorian, WandaVision, DuckTales reboot, etc.) — hold the line.

**Adding questions:** Append to the `QUESTIONS` array in `questions.js`. Use the next available integer ID. Correct answer must be at index 0.

**Current count:** 500 questions. Distribution:
- movies 128, characters 90, parks 75, pixar 62, walt 52, music 52, cruise 41

**Removing a question:** Delete its object from the array. IDs do not need to be contiguous — gaps are fine.

## Storage Layer — Firebase (active)
User stats and flags are stored in **Firestore**, project `disneytrivia-38ac6`.

Collections:
- `users` — one doc per player, keyed by user ID
- `flags` — one doc per flag report (auto-ID)

Document shape:
```js
// users/{userId}
{ id, name, totalAnswered, totalCorrect, gamesPlayed }

// flags/{autoId}
{ questionId, questionText, correctAnswer, allAnswers, difficulty, category,
  reportedBy, comment, timestamp, _resolved? }
```

Stats stored as raw counters (`totalAnswered`, `totalCorrect`); percentage is always derived, never stored. `updateStats` uses a Firestore transaction to avoid race conditions when two players finish at the same time.

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
- After fixing a question in `questions.js`, mark the flag Resolved in `review.html`
- Flagging does NOT auto-remove the question; that's always a manual edit to `questions.js`

## Deploying Changes
The app is hosted on GitHub Pages from the `main` branch. To push an update:

```
git add -A && git commit -m "your message" && git push
```

GitHub Pages redeploys automatically within ~1 minute.

## Key app.js Globals
| Variable | What it holds |
|---|---|
| `currentUser` | The user object selected on the home screen |
| `gameSettings` | `{ difficulty, categories[], questionCount }` — set on settings screen |
| `gameState` | `{ questions[], currentIndex, answers[], score }` — active game |
| `shuffledOpts` | `[{text, originalIndex}]` — display order for current question's answers |

## Styling Conventions
- CSS variables defined in `:root` at the top of `style.css` — use these, don't hardcode colors
- Key variables: `--bg`, `--bg-card`, `--bg-hover`, `--border`, `--primary`, `--gold`, `--green`, `--red`, `--text`, `--muted`
- Border-radius variables: `--r` (cards), `--r-sm` (buttons/inputs)
- All new screens follow the pattern: `.screen` div → `screen-header` → content → actions at bottom
- Mobile-first. Max width 480px centered. Test at 375px (iPhone SE) as the floor.

## Players
Default users seeded on first load: **Kristen** and **Cara**. Seeding is in `FirebaseAdapter._seed()` — it checks if the doc exists before writing, so it's safe to run on every page load. Do not remove them from the seed.

## What NOT to Do
- Do not introduce a build step, bundler, or npm unless explicitly asked
- Do not add a backend or server — this is intentionally fully static
- Do not store derived values (percentages) — always compute from raw counters
- Do not add TV show questions
- Do not reuse question IDs
