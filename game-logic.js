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
  const all = [...new Set(seen.concat(newIds).reverse())].reverse();
  return all.length > max ? all.slice(all.length - max) : all;
}

// --- Round mix -----------------------------------------------------------------

// Difficulty shares for a round whose pool has more than one difficulty:
// 2 easy / 5 medium / 3 hard per 10. Easy stays at 20% because the bank has only
// ~400 easy questions and the daily keeps 180 days of pins out of play.
const MIX_SHARES = { easy: 0.2, medium: 0.5, hard: 0.3 };
// No category fills more than 30% of a round (3 of 10), unless too few
// categories are in play for that to be possible.
const CATEGORY_CAP_SHARE = 0.3;

// Whole-question targets per difficulty (largest remainder), e.g. 10 → 2/5/3.
function difficultyTargets(count, shares = MIX_SHARES) {
  const keys = Object.keys(shares), raw = keys.map(k => shares[k] * count);
  const out = Object.fromEntries(keys.map((k, i) => [k, Math.floor(raw[i] + 1e-9)]));
  let left = count - Object.values(out).reduce((a, b) => a + b, 0);
  keys.map((k, i) => [k, raw[i] - out[k]]).sort((a, b) => b[1] - a[1])
    .forEach(([k]) => { if (left > 0) { out[k]++; left--; } });
  return out;
}

// Balancing options derived from the pool itself, so player filters win: a
// single-difficulty or single-category pool is never "balanced" against itself.
function roundMix(pool) {
  return { balanceDifficulty: new Set(pool.map(q => q.difficulty)).size > 1,
    categoryCount: new Set(pool.map(q => q.category)).size };
}

// A round should touch at least this many categories (when that many are in play).
const MIN_ROUND_CATEGORIES = 5;

// Picks `count` questions from priority tiers. An earlier tier always wins over
// a later one (freshness beats mix). Inside a tier it walks the tier's order and
// takes questions that keep the round balanced, relaxing only when the tier
// can't supply a balanced fill:
//   1. difficulty under its target, category under its cap, and enough slots
//      left to still reach the minimum number of categories
//   2. as 1, but a medium may stand in for a missing easy or hard
//   3. category cap only
//   4. anything
// Passes 1-3 also keep questions with id >= newFromId to at most maxNew.
function pickBalanced(tiers, count, { balanceDifficulty = true, categoryCount = 1,
                                      newFromId = Infinity, maxNew = Infinity } = {}) {
  const targets = balanceDifficulty ? difficultyTargets(count) : null;
  const cap = categoryCount > 1
    ? Math.max(Math.round(count * CATEGORY_CAP_SHARE), Math.ceil(count / categoryCount)) : Infinity;
  const minCats = Math.min(MIN_ROUND_CATEGORIES, categoryCount, Math.ceil(count / 2));
  const picked = [], ids = new Set(), byDiff = {}, byCat = {};
  let newCount = 0;
  const diffOk = q => !targets || (byDiff[q.difficulty] || 0) < (targets[q.difficulty] || 0);
  const catOk = q => (byCat[q.category] || 0) < cap;
  const newOk = q => q.id < newFromId || newCount < maxNew;
  // Taking q must leave enough slots to bring in the categories still missing.
  const spreadOk = q => {
    const distinct = Object.keys(byCat).length + (byCat[q.category] ? 0 : 1);
    return minCats - distinct <= count - picked.length - 1;
  };
  const passes = [
    q => diffOk(q) && catOk(q) && newOk(q) && spreadOk(q),
    q => (diffOk(q) || q.difficulty === 'medium') && catOk(q) && newOk(q) && spreadOk(q),
    q => catOk(q) && newOk(q),
    () => true
  ];
  for (const tier of tiers) for (const ok of passes) for (const q of tier) {
    if (picked.length >= count) return picked;
    if (ids.has(q.id) || !ok(q)) continue;
    picked.push(q); ids.add(q.id);
    byDiff[q.difficulty] = (byDiff[q.difficulty] || 0) + 1;
    byCat[q.category] = (byCat[q.category] || 0) + 1;
    if (q.id >= newFromId) newCount++;
  }
  return picked;
}

// Regular games, in priority order:
//   1. questions this player has never answered (random)
//   2. answered before but not recently: fewest answers first (random ties)
//   3. the recent window (seenIds), least recently seen first
// `answered` maps question id → times answered (built from questionStats and
// missedQuestionIds), so a question from 301 answers ago is no longer treated
// as new. The final order is shuffled.
function pickRegularQuestions(pool, seenIds, count, rng = Math.random, answered = new Map()) {
  const recent = new Set(seenIds);
  const times = id => answered.get(id) || 0;
  const age = new Map(seenIds.map((id, i) => [id, i]));
  const never = shuffle(pool.filter(q => !recent.has(q.id) && !times(q.id)), rng);
  const older = shuffle(pool.filter(q => !recent.has(q.id) && times(q.id)), rng)
    .sort((a, b) => times(a.id) - times(b.id));
  const repeats = shuffle(pool.filter(q => recent.has(q.id)), rng)
    .sort((a, b) => age.get(a.id) - age.get(b.id));
  return shuffle(pickBalanced([never, older, repeats], count, roundMix(pool)), rng);
}

// --- Dates -------------------------------------------------------------------

// Shared daily boundary: 08:00 UTC year-round (4am Toronto summer, 3am winter).
// A fixed instant avoids changing the challenge's duration on DST transitions.
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

// The generation rounds of 2026-11 (v1.48-v1.50) start at this id. They score well
// below the older bank and, never having been pinned, made up a third of the
// daily's fresh pool, so each daily takes at most one. After another generation
// round, leave this unless the older rounds no longer need pacing.
const NEW_QUESTION_MIN_ID = 2656;
const MAX_NEW_PER_DAILY = 1;

// Adds the active question that replaced each retired duplicate (following
// chains), so a fact pinned under its retired id isn't asked again under the
// surviving one. Keeps the order; a replacement's latest position wins.
function withReplacements(ids, retired) {
  const next = new Map((retired || []).filter(q => q.replacedBy).map(q => [q.id, q.replacedBy]));
  const out = new Set(), append = id => { out.delete(id); out.add(id); };
  for (const id of ids) {
    append(id);
    const visited = new Set([id]);
    for (let r = next.get(id); r && !visited.has(r); r = next.get(r)) { visited.add(r); append(r); }
  }
  return out;
}

// Stable-sorts by id first so shard/load order doesn't affect the result.
// Exclusions are insertion-ordered oldest first, allowing gradual cooldown
// relaxation. Fresh questions always win over excluded ones; within each, the
// round is balanced and capped on new questions (pickBalanced), and the final
// order is shuffled by the date.
function pickDailyQuestions(pool, dateKeyStr, count = 10, excludeIds = new Set()) {
  const seed     = dateToSeed(dateKeyStr);
  const sorted   = [...pool].sort((a, b) => a.id - b.id);
  const shuffled = seededShuffle(sorted, seed);
  const fresh    = shuffled.filter(q => !excludeIds.has(q.id));
  const age = new Map([...excludeIds].map((id, i) => [id, i]));
  const repeats = shuffled.filter(q => excludeIds.has(q.id))
    .sort((a, b) => age.get(a.id) - age.get(b.id));
  return seededShuffle(pickBalanced([fresh, repeats], count,
    { ...roundMix(pool), newFromId: NEW_QUESTION_MIN_ID, maxNew: MAX_NEW_PER_DAILY }), seed ^ 0x5bd1e995);
}

// --- Daily history (meta/dailyHistory: {days: {"YYYY-MM-DD": [ids]}}) --------

// How far back past daily pins are excluded when picking a new day. A rolling
// window, not all-time: 10 pins/day for 180 days keeps ~1,800 IDs out of play,
// safely under the ~2,200-question bank, and far longer than anyone remembers
// a specific daily.
const DAILY_HISTORY_DAYS = 180;

function addDays(key, n) {
  return new Date(Date.parse(key + 'T12:00:00Z') + n * 86400000).toISOString().slice(0, 10);
}

// Merges history maps, keeping dates >= since. Earlier maps win for a date
// present in several (an existing entry is never rewritten), so pass the
// stored history first.
function mergeDailyHistory(since, ...maps) {
  const out = {};
  for (const m of maps) for (const [date, ids] of Object.entries(m || {})) {
    if (date >= since && !Object.hasOwn(out, date) && Array.isArray(ids)) out[date] = ids;
  }
  return Object.fromEntries(Object.entries(out).sort(([a], [b]) => a.localeCompare(b)));
}

// Dates in [since, before) with no entry. An empty array marks a day nobody played.
function missingHistoryDates(days, since, before) {
  const out = [];
  for (let d = since; d < before; d = addDays(d, 1)) if (!Object.hasOwn(days || {}, d)) out.push(d);
  return out;
}

// Missing days that can safely be recorded as unplayed ([]): only those more
// than a week before the newest known pin. A recorded day can never be
// rewritten, so a device whose clock runs ahead must not mark a day empty that
// others are still about to play; newer gaps are simply re-read next time.
const UNPLAYED_SETTLE_DAYS = 7;
function unplayedDays(days, since, before) {
  const latest = Object.keys(days || {}).filter(d => days[d].length && d < before).sort().pop();
  return latest ? missingHistoryDates(days, since, addDays(latest, -UNPLAYED_SETTLE_DAYS)) : [];
}

// Pinned IDs, oldest day first.
function dailyHistoryIds(days) {
  return Object.keys(days || {}).sort().flatMap(d => days[d]);
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

function validQuestion(q) {
  return q && Number.isSafeInteger(q.id) && q.id>0 && typeof q.question==='string' && q.question.trim()
    && ['movies','characters','parks','walt','cruise','music','pixar'].includes(q.category)
    && ['easy','medium','hard'].includes(q.difficulty) && Array.isArray(q.answers) && q.answers.length===4
    && q.answers.every(a=>typeof a==='string' && a.trim()) && new Set(q.answers).size===4;
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
    gameId: checkpoint.gameId || `legacy_${dateToSeed(JSON.stringify(checkpoint))}`,
    resetRevision: checkpoint.resetRevision || 0,
    dateKey: checkpoint.dateKey || (checkpoint.savedAt ? todayKey(Date.parse(checkpoint.savedAt)) : todayKey()),
    isPractice: !!checkpoint.isPractice,
    questions, currentIndex: answers.length, answers,
    score: answers.filter(a => a.correct).length, currentStreak: trailingStreak(answers),
    isDaily: false, pointsEarned: 0, scoreBreakdown: null
  };
}

// --- Game log ------------------------------------------------------------------

// Per-player game history (users/{id}.gameLog), newest first, capped. A
// diagnostic trail for "we got different questions" style reports, not game
// state — nothing in the app reads it back.
const GAME_LOG_MAX = 30;

function appendGameLog(log, entry, max = GAME_LOG_MAX) {
  return [entry].concat(Array.isArray(log) ? log : []).slice(0, max);
}

// status: 'complete' | 'exited' (left mid-game) | 'abandoned' (an unfinished
// checkpoint committed by "Start new"). questionIds is the whole game in play
// order; the first `answered` of them were shown. A daily exit commits no
// stats, so its points are 0. Every value is non-undefined: Firestore rejects
// undefined fields, which would fail the stats transaction this rides in.
// Fully answered games that this device never committed: the app was closed on
// the last answer, or the save failed (no signal, stalled wifi). Rebuilt as
// gameStates so they can be saved automatically with no player action.
//   dailyArchives — {userId: {dateKey: {dateKey, answers, questions, resetRevision}}}
//   checkpoints   — {userId: regular-game checkpoint}
//   questionsById — Map of active + retired questions (for regular checkpoints)
// Partially answered games are excluded: the player may still finish them.
// Oldest first, dailies before regular games on the same day, because the daily
// bonus streak is computed from the dates already saved when a daily commits.
function completedUnsavedGames(dailyArchives, checkpoints, questionsById = new Map()) {
  const games = [];
  for (const [userId, entries] of Object.entries(dailyArchives || {})) {
    for (const entry of Object.values(entries || {})) {
      if (!entry?.dateKey || !Array.isArray(entry.questions) || !entry.questions.length) continue;
      const gs = reconcileDailyProgress(entry.questions, entry, entry.dateKey);
      if (gs.answers.length !== entry.questions.length) continue;
      games.push({ ...gs, gameId: 'daily_' + entry.dateKey, dateKey: entry.dateKey, userId,
        resetRevision: entry.resetRevision || 0, resumed: true, recovered: true });
    }
  }
  for (const [userId, cp] of Object.entries(checkpoints || {})) {
    const byId = new Map(questionsById);
    for (const question of cp?.questions || []) if (question && !byId.has(question.id)) byId.set(question.id, question);
    const gs = reconcileRegularCheckpoint(cp, byId);
    if (!gs || gs.isPractice || !gs.answers.length || gs.answers.length !== gs.questions.length) continue;
    games.push({ ...gs, userId, resumed: true, recovered: true });
  }
  return games.sort((a, b) => a.dateKey.localeCompare(b.dateKey) || Number(b.isDaily) - Number(a.isDaily));
}

function buildGameLogEntry({ mode, status, questionIds, answers, points, dateKey,
                             resumed, firstDaily, recovered, device, platform, version, now = Date.now() }) {
  const entry = {
    at:          new Date(now).toISOString(),
    day:         dateKey ?? null,
    mode:        mode ?? null,
    status:      status ?? null,
    questionIds: (questionIds || []).slice(),
    answered:    (answers || []).length,
    correct:     (answers || []).filter(a => a.correct).length,
    points:      points ?? 0,
    resumed:     !!resumed,
    device:      device ?? null,
    platform:    platform ?? null,
    v:           version ?? null
  };
  if (mode === 'daily') entry.firstDaily = !!firstDaily;
  if (recovered) entry.recovered = true;   // saved later, automatically, from this device
  return entry;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    shuffle, SEEN_MAX, capSeenIds, pickRegularQuestions,
    MIX_SHARES, CATEGORY_CAP_SHARE, MIN_ROUND_CATEGORIES, difficultyTargets, roundMix, pickBalanced,
    dayKey, todayKey, monthKey, prevMonthKey, computeDaysDiff, nextDailyStreak, homeworkWeekKey,
    seededShuffle, dateToSeed, NEW_QUESTION_MIN_ID, MAX_NEW_PER_DAILY, withReplacements, pickDailyQuestions, pickMovie,
    DAILY_HISTORY_DAYS, addDays, mergeDailyHistory, missingHistoryDates, unplayedDays, dailyHistoryIds,
    SCORING, scoreBreakdown, buildCatStats, validQuestion,
    serializeAnswers, trailingStreak, reconcileDailyProgress, reconcileRegularCheckpoint,
    completedUnsavedGames, GAME_LOG_MAX, appendGameLog, buildGameLogEntry
  };
}
