// =============================================================================
// Pure game rules — no DOM, no storage, no globals. Loaded as a classic script
// before app.js (so every name here is a browser global app.js can call), and
// require()-able from Node so test/game-logic.test.js can exercise the real
// code the app runs. Anything time- or random-dependent takes a `now` / `rng`
// argument (defaulting to the real clock / Math.random) so tests stay
// deterministic. When changing a rule, change it here and add a test — don't
// reimplement it inline in app.js.
// =============================================================================

function shuffle(arr, rng = Math.random) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const SEEN_MAX = 300;

// Appends newIds to a seen-ids list, keeping only the most recent SEEN_MAX.
function capSeenIds(seen, newIds, max = SEEN_MAX) {
  const all = seen.concat(newIds);
  return all.length > max ? all.slice(all.length - max) : all;
}

// Regular-game question pick: only unseen questions if there are enough to
// fill the game, otherwise the exclusion is dropped entirely (never a partial
// top-up with repeats).
function pickRegularQuestions(pool, seenIds, count, rng = Math.random) {
  const seen  = new Set(seenIds);
  const fresh = pool.filter(q => !seen.has(q.id));
  const src   = fresh.length >= count ? fresh : pool;
  return shuffle(src, rng).slice(0, count);
}

// --- Dates -------------------------------------------------------------------

// Daily resets at 2am Mountain Time (UTC-6 summer / MDT).
// Subtracting 8h shifts the UTC day boundary to 8am UTC = 2am MDT = 4am EDT.
// getUTC* is correct here because the offset is baked into the timestamp.
// daysAgo=0 → today, daysAgo=1 → yesterday (same 8h offset, no string arithmetic).
function dayKey(daysAgo = 0, now = Date.now()) {
  const d = new Date(now - 8 * 3600000 - daysAgo * 86400000);
  return `${d.getUTCFullYear()}-${String(d.getUTCMonth()+1).padStart(2,'0')}-${String(d.getUTCDate()).padStart(2,'0')}`;
}
function todayKey(now = Date.now()) { return dayKey(0, now); }

// "YYYY-MM" for the current month, using the same 8h-shifted boundary as
// dayKey() so the month rolls over at the same instant the day does.
function monthKey(now = Date.now()) { return dayKey(0, now).slice(0, 7); }

// "YYYY-MM" for the calendar month before the current one — used for the
// leaderboard's "Last Month" view. Built from a real Date so it correctly
// rolls the year back in January (JS normalizes a negative month index).
function prevMonthKey(now = Date.now()) {
  const [y, m] = monthKey(now).split('-').map(Number);
  const d = new Date(y, m - 2, 1);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
}

// Returns calendar days between two "YYYY-MM-DD" keys. Returns Infinity if prev is falsy.
function computeDaysDiff(prev, today) {
  if (!prev) return Infinity;
  const [py, pm, pd] = prev.split('-').map(Number);
  const [ty, tm, td] = today.split('-').map(Number);
  return Math.round((new Date(ty, tm - 1, td) - new Date(py, pm - 1, pd)) / 86400000);
}

// The daily streak after finishing today's daily: +1 if the last daily was
// yesterday, otherwise it restarts at 1.
function nextDailyStreak(lastDailyDate, currentStreak, today) {
  return computeDaysDiff(lastDailyDate, today) === 1 ? (currentStreak || 0) + 1 : 1;
}

// Same 8h-shift trick as dayKey(): rolls over at 08:00 UTC = 3am EST / 4am EDT.
// Returns the date key ("YYYY-MM-DD") of the most recent Thursday at/after that boundary,
// i.e. the identifier for the current homework week.
function homeworkWeekKey(now = Date.now()) {
  const shifted = new Date(now - 8 * 3600000);
  const day  = shifted.getUTCDay();       // 0=Sun ... 4=Thu
  const diff = (day - 4 + 7) % 7;         // days since the most recent Thursday
  shifted.setUTCDate(shifted.getUTCDate() - diff);
  return `${shifted.getUTCFullYear()}-${String(shifted.getUTCMonth()+1).padStart(2,'0')}-${String(shifted.getUTCDate()).padStart(2,'0')}`;
}

// --- Daily challenge selection ---------------------------------------------

// Deterministic Fisher-Yates using an inline mulberry32 step. Same seed → same result.
function seededShuffle(arr, seed) {
  const a = [...arr];
  let s = seed | 0;
  for (let i = a.length - 1; i > 0; i--) {
    s = (s + 0x6D2B79F5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    const j = ((t ^ (t >>> 14)) >>> 0) % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function dateToSeed(key) {
  let h = 0;
  for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) & 0x7fffffff;
  return h;
}

// Stable-sorts by id first so shard/load order doesn't affect the result.
// Falls back to the unexcluded order if exclusion leaves fewer than `count`.
function pickDailyQuestions(pool, dateKeyStr, count = 10, excludeIds = new Set()) {
  const sorted   = [...pool].sort((a, b) => a.id - b.id);
  const shuffled = seededShuffle(sorted, dateToSeed(dateKeyStr));
  const fresh    = shuffled.filter(q => !excludeIds.has(q.id));
  const src      = fresh.length >= count ? fresh : shuffled;
  return src.slice(0, count);
}

// Picks a random movie not in excludeIds. If that leaves nothing, falls back to the
// full pool (reset: true) so the pool never runs dry.
function pickMovie(pool, excludeIds, rng = Math.random) {
  const excl = new Set(excludeIds);
  let candidates = pool.filter(m => !excl.has(m.id));
  let reset = false;
  if (candidates.length === 0) { candidates = pool; reset = true; }
  return { movie: candidates[Math.floor(rng() * candidates.length)], reset };
}

// --- Scoring -----------------------------------------------------------------

const SCORING = {
  easy: 100, medium: 150, hard: 200,  // pts per correct answer
  streak: 25,                          // per correct while in-game run ≥ 3
  perfect: 500,                        // all correct in one game
  dailyFlat: 200,                      // daily challenge completion
  dailyPerDay: 10,                     // × min(streak, dailyStreakCap)
  dailyStreakCap: 30
};

// Returns {base, streakBonus, perfectBonus, dailyBonus, total}.
// earnDailyBonus — true only on first daily play of the calendar day.
// dailyStreak    — the new streak value after this game.
// awardPerfect   — false for a mid-game exit, where "all answered so far correct"
//                  isn't a completed perfect game and shouldn't earn the bonus.
function scoreBreakdown(answers, earnDailyBonus, dailyStreak, awardPerfect = true) {
  let base = 0, streakBonus = 0, run = 0;
  for (const a of answers) {
    if (a.correct) {
      base += SCORING[a.question.difficulty] || SCORING.easy;
      run++;
      if (run >= 3) streakBonus += SCORING.streak;
    } else {
      run = 0;
    }
  }
  const perfectBonus = (awardPerfect && answers.length > 0 && answers.every(a => a.correct)) ? SCORING.perfect : 0;
  let dailyBonus = 0;
  if (earnDailyBonus) {
    dailyBonus = SCORING.dailyFlat + Math.min(dailyStreak, SCORING.dailyStreakCap) * SCORING.dailyPerDay;
  }
  return { base, streakBonus, perfectBonus, dailyBonus, total: base + streakBonus + perfectBonus + dailyBonus };
}

function buildCatStats(answers) {
  const stats = {};
  for (const a of answers) {
    const c = a.question.category;
    if (!stats[c]) stats[c] = { answered: 0, correct: 0 };
    stats[c].answered++;
    if (a.correct) stats[c].correct++;
  }
  return stats;
}

// --- Checkpoint / resume -------------------------------------------------------

// Serializable form of gameState.answers for a localStorage checkpoint.
function serializeAnswers(answers) {
  return answers.map(a => ({ questionId: a.question.id, correct: a.correct, selectedText: a.selectedText }));
}

// Trailing run of correct answers — the in-game streak to restore on resume.
function trailingStreak(answers) {
  let n = 0;
  for (let i = answers.length - 1; i >= 0 && answers[i].correct; i--) n++;
  return n;
}

// Rebuilds a daily gameState from today's pinned questions plus saved progress.
// Progress only counts if it's for `today` and lines up position-by-position
// with the pinned order — if pins shifted underneath a saved answer (e.g. a
// backfill after the exit), only the still-matching prefix is kept, never
// silently miscounted.
function reconcileDailyProgress(questions, progress, today) {
  const answers = [];
  if (progress && progress.dateKey === today && Array.isArray(progress.answers)) {
    for (const a of progress.answers) {
      const q = questions[answers.length];
      if (!q || q.id !== a.questionId) break;
      answers.push({ question: q, selectedText: a.selectedText, correct: a.correct });
    }
  }
  return {
    questions, currentIndex: answers.length, answers,
    score: answers.filter(a => a.correct).length, currentStreak: trailingStreak(answers),
    isDaily: true, pointsEarned: 0, scoreBreakdown: null
  };
}

// Rebuilds a regular gameState from a checkpoint ({questionIds, answers}).
// Questions deleted from the shards since the checkpoint are dropped — an
// answered one along with its answer, an unanswered one just shrinks the game.
// Answered questions are placed first, in answer order, so currentIndex ===
// answers.length always holds. Returns null if nothing usable is left.
function reconcileRegularCheckpoint(checkpoint, questionsById) {
  if (!checkpoint || !Array.isArray(checkpoint.questionIds) || !Array.isArray(checkpoint.answers)) return null;
  const answers = [];
  const answeredIds = new Set();
  for (const a of checkpoint.answers) {
    const q = questionsById.get(a.questionId);
    if (!q || answeredIds.has(q.id)) continue;
    answeredIds.add(q.id);
    answers.push({ question: q, selectedText: a.selectedText, correct: a.correct });
  }
  const remaining = checkpoint.questionIds
    .filter(id => !answeredIds.has(id))
    .map(id => questionsById.get(id))
    .filter(Boolean);
  const questions = answers.map(a => a.question).concat(remaining);
  if (questions.length === 0) return null;
  return {
    questions, currentIndex: answers.length, answers,
    score: answers.filter(a => a.correct).length, currentStreak: trailingStreak(answers),
    isDaily: false, pointsEarned: 0, scoreBreakdown: null
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    shuffle, SEEN_MAX, capSeenIds, pickRegularQuestions,
    dayKey, todayKey, monthKey, prevMonthKey, computeDaysDiff, nextDailyStreak, homeworkWeekKey,
    seededShuffle, dateToSeed, pickDailyQuestions, pickMovie,
    SCORING, scoreBreakdown, buildCatStats,
    serializeAnswers, trailingStreak, reconcileDailyProgress, reconcileRegularCheckpoint
  };
}
