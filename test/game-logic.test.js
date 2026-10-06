// Unit tests for game-logic.js. Run from the project root:
//   node --test test/game-logic.test.js
// No package.json / npm — node:test and node:assert are built in.
const test = require('node:test');
const assert = require('node:assert/strict');
const L = require('../game-logic.js');

// Deterministic rng for shuffle-based helpers.
function seqRng(seed = 1) {
  let s = seed;
  return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
}
const utc = (...a) => Date.UTC(...a);
const q = (id, difficulty = 'easy', category = 'movies') => ({ id, difficulty, category, question: `Q${id}`, answers: ['a', 'b', 'c', 'd'] });

// --- Dates -------------------------------------------------------------------

test('dayKey rolls over at 08:00 UTC, not midnight', () => {
  assert.equal(L.dayKey(0, utc(2026, 9, 5, 7, 59)), '2026-10-04');
  assert.equal(L.dayKey(0, utc(2026, 9, 5, 8, 0)), '2026-10-05');
  assert.equal(L.dayKey(1, utc(2026, 9, 5, 8, 0)), '2026-10-04');
  assert.equal(L.todayKey(utc(2026, 9, 5, 12)), '2026-10-05');
});

test('dayKey crosses month and year boundaries', () => {
  assert.equal(L.dayKey(0, utc(2027, 0, 1, 7, 0)), '2026-12-31');
  assert.equal(L.dayKey(1, utc(2026, 2, 1, 9, 0)), '2026-02-28');
});

test('monthKey uses the same 8h-shifted boundary', () => {
  assert.equal(L.monthKey(utc(2026, 10, 1, 7, 59)), '2026-10');
  assert.equal(L.monthKey(utc(2026, 10, 1, 8, 0)), '2026-11');
});

test('prevMonthKey rolls the year back in January', () => {
  assert.equal(L.prevMonthKey(utc(2027, 0, 15, 12)), '2026-12');
  assert.equal(L.prevMonthKey(utc(2026, 9, 15, 12)), '2026-09');
});

test('computeDaysDiff handles month ends, leap years, DST, and missing prev', () => {
  assert.equal(L.computeDaysDiff('2026-01-31', '2026-02-01'), 1);
  assert.equal(L.computeDaysDiff('2028-02-28', '2028-03-01'), 2);
  assert.equal(L.computeDaysDiff('2026-03-07', '2026-03-08'), 1); // US DST start
  assert.equal(L.computeDaysDiff('2026-10-31', '2026-11-01'), 1); // US DST end
  assert.equal(L.computeDaysDiff(null, '2026-10-05'), Infinity);
});

test('nextDailyStreak continues only from yesterday', () => {
  assert.equal(L.nextDailyStreak('2026-10-04', 6, '2026-10-05'), 7);
  assert.equal(L.nextDailyStreak('2026-10-03', 6, '2026-10-05'), 1);
  assert.equal(L.nextDailyStreak(undefined, 0, '2026-10-05'), 1);
});

test('homeworkWeekKey returns the most recent Thursday, rolling at 08:00 UTC', () => {
  // 2026-10-08 is a Thursday.
  assert.equal(L.homeworkWeekKey(utc(2026, 9, 8, 7, 59)), '2026-10-01');
  assert.equal(L.homeworkWeekKey(utc(2026, 9, 8, 8, 0)), '2026-10-08');
  assert.equal(L.homeworkWeekKey(utc(2026, 9, 14, 12)), '2026-10-08');
});

// --- Selection ---------------------------------------------------------------

test('seededShuffle is deterministic and a permutation', () => {
  const arr = Array.from({ length: 50 }, (_, i) => i);
  const a = L.seededShuffle(arr, 12345);
  assert.deepEqual(a, L.seededShuffle(arr, 12345));
  assert.notDeepEqual(a, L.seededShuffle(arr, 54321));
  assert.deepEqual([...a].sort((x, y) => x - y), arr);
});

test('pickDailyQuestions ignores pool order and honors exclusions', () => {
  const pool = Array.from({ length: 40 }, (_, i) => q(i + 1));
  const a = L.pickDailyQuestions(pool, '2026-10-05', 10);
  const b = L.pickDailyQuestions([...pool].reverse(), '2026-10-05', 10);
  assert.deepEqual(a.map(x => x.id), b.map(x => x.id));
  const excl = new Set(a.map(x => x.id));
  const c = L.pickDailyQuestions(pool, '2026-10-05', 10, excl);
  assert.equal(c.length, 10);
  assert.ok(c.every(x => !excl.has(x.id)));
});

test('pickDailyQuestions drops exclusion entirely when it would leave too few', () => {
  const pool = Array.from({ length: 12 }, (_, i) => q(i + 1));
  const excl = new Set([1, 2, 3, 4, 5]);
  const picked = L.pickDailyQuestions(pool, '2026-10-05', 10, excl);
  assert.equal(picked.length, 10);
  assert.deepEqual(picked.map(x => x.id), L.pickDailyQuestions(pool, '2026-10-05', 10).map(x => x.id));
});

test('pickRegularQuestions prefers unseen, else uses the whole pool', () => {
  const pool = Array.from({ length: 20 }, (_, i) => q(i + 1));
  const seen = Array.from({ length: 8 }, (_, i) => i + 1);
  const fresh = L.pickRegularQuestions(pool, seen, 10, seqRng(3));
  assert.equal(fresh.length, 10);
  assert.ok(fresh.every(x => x.id > 8));
  const seen15 = Array.from({ length: 15 }, (_, i) => i + 1);
  const mixed = L.pickRegularQuestions(pool, seen15, 10, seqRng(3));
  assert.equal(mixed.length, 10);
  assert.equal(new Set(mixed.map(x => x.id)).size, 10);
});

test('capSeenIds keeps only the most recent entries', () => {
  assert.deepEqual(L.capSeenIds([1, 2, 3], [4, 5], 4), [2, 3, 4, 5]);
  assert.deepEqual(L.capSeenIds([], [1], 4), [1]);
  assert.equal(L.capSeenIds(Array(299).fill(0), [1, 2, 3]).length, L.SEEN_MAX);
});

test('pickMovie excludes watched and resets when the pool is exhausted', () => {
  const pool = [{ id: 1 }, { id: 2 }, { id: 3 }];
  const r = L.pickMovie(pool, [1, 2], seqRng(1));
  assert.deepEqual(r, { movie: { id: 3 }, reset: false });
  assert.equal(L.pickMovie(pool, [1, 2, 3], seqRng(1)).reset, true);
});

// --- Scoring -----------------------------------------------------------------

const ans = (difficulty, correct) => ({ question: q(0, difficulty), correct });

test('scoreBreakdown: base points by difficulty', () => {
  const bd = L.scoreBreakdown([ans('easy', true), ans('medium', true), ans('hard', false)], false, 0);
  assert.equal(bd.base, 250);
  assert.equal(bd.streakBonus, 0);
  assert.equal(bd.perfectBonus, 0);
  assert.equal(bd.total, 250);
});

test('scoreBreakdown: streak bonus starts at the 3rd consecutive correct and resets on a miss', () => {
  const run = [true, true, true, true, false, true, true, true].map(c => ans('easy', c));
  assert.equal(L.scoreBreakdown(run, false, 0).streakBonus, 75); // 3rd, 4th, then 3rd of the new run
});

test('scoreBreakdown: perfect bonus only for a complete all-correct game', () => {
  const all = [ans('easy', true), ans('easy', true)];
  assert.equal(L.scoreBreakdown(all, false, 0).perfectBonus, 500);
  assert.equal(L.scoreBreakdown(all, false, 0, false).perfectBonus, 0);
  assert.equal(L.scoreBreakdown([], false, 0).perfectBonus, 0);
});

test('scoreBreakdown: daily bonus scales with streak, capped at 30 days', () => {
  assert.equal(L.scoreBreakdown([], true, 5).dailyBonus, 250);
  assert.equal(L.scoreBreakdown([], true, 30).dailyBonus, 500);
  assert.equal(L.scoreBreakdown([], true, 99).dailyBonus, 500);
  assert.equal(L.scoreBreakdown([], false, 99).dailyBonus, 0);
});

test('buildCatStats counts per category', () => {
  const a = [
    { question: q(1, 'easy', 'movies'), correct: true },
    { question: q(2, 'easy', 'movies'), correct: false },
    { question: q(3, 'easy', 'parks'), correct: true },
  ];
  assert.deepEqual(L.buildCatStats(a), { movies: { answered: 2, correct: 1 }, parks: { answered: 1, correct: 1 } });
});

// --- Checkpoint / resume -------------------------------------------------------

test('reconcileDailyProgress resumes a matching prefix and restores score/streak', () => {
  const qs = [q(10), q(11), q(12), q(13)];
  const progress = { dateKey: '2026-10-05', answers: [
    { questionId: 10, correct: false, selectedText: 'x' },
    { questionId: 11, correct: true, selectedText: 'a' },
    { questionId: 12, correct: true, selectedText: 'a' },
  ] };
  const gs = L.reconcileDailyProgress(qs, progress, '2026-10-05');
  assert.equal(gs.currentIndex, 3);
  assert.equal(gs.score, 2);
  assert.equal(gs.currentStreak, 2);
  assert.equal(gs.isDaily, true);
  assert.equal(gs.answers[0].question, qs[0]);
});

test('reconcileDailyProgress keeps only the prefix that still lines up with the pins', () => {
  const qs = [q(10), q(99), q(12)];
  const progress = { dateKey: '2026-10-05', answers: [
    { questionId: 10, correct: true, selectedText: 'a' },
    { questionId: 11, correct: true, selectedText: 'a' },
    { questionId: 12, correct: true, selectedText: 'a' },
  ] };
  assert.equal(L.reconcileDailyProgress(qs, progress, '2026-10-05').currentIndex, 1);
});

test('reconcileDailyProgress ignores progress from another day', () => {
  const progress = { dateKey: '2026-10-04', answers: [{ questionId: 10, correct: true, selectedText: 'a' }] };
  const gs = L.reconcileDailyProgress([q(10)], progress, '2026-10-05');
  assert.equal(gs.currentIndex, 0);
  assert.equal(gs.score, 0);
});

test('reconcileDailyProgress with a complete set lands at the end (caller retries endGame)', () => {
  const qs = [q(1), q(2)];
  const progress = { dateKey: 'd', answers: qs.map(x => ({ questionId: x.id, correct: true, selectedText: 'a' })) };
  const gs = L.reconcileDailyProgress(qs, progress, 'd');
  assert.equal(gs.currentIndex, gs.questions.length);
  assert.equal(gs.ended, undefined);
});

test('serializeAnswers round-trips through reconcileRegularCheckpoint', () => {
  const qs = [q(1, 'hard'), q(2), q(3), q(4)];
  const byId = new Map(qs.map(x => [x.id, x]));
  const answers = [
    { question: qs[0], selectedText: 'a', correct: true },
    { question: qs[1], selectedText: 'b', correct: false },
  ];
  const cp = { questionIds: qs.map(x => x.id), answers: L.serializeAnswers(answers) };
  const gs = L.reconcileRegularCheckpoint(JSON.parse(JSON.stringify(cp)), byId);
  assert.deepEqual(gs.questions.map(x => x.id), [1, 2, 3, 4]);
  assert.equal(gs.currentIndex, 2);
  assert.equal(gs.score, 1);
  assert.equal(gs.currentStreak, 0);
  assert.equal(gs.isDaily, false);
  assert.equal(gs.answers[0].question, qs[0]);
});

test('reconcileRegularCheckpoint drops questions deleted from the shards', () => {
  const byId = new Map([[1, q(1)], [3, q(3)], [4, q(4)]]); // 2 was deleted
  const cp = { questionIds: [1, 2, 3, 4], answers: [
    { questionId: 1, correct: true, selectedText: 'a' },
    { questionId: 2, correct: true, selectedText: 'a' },
  ] };
  const gs = L.reconcileRegularCheckpoint(cp, byId);
  assert.deepEqual(gs.questions.map(x => x.id), [1, 3, 4]);
  assert.equal(gs.currentIndex, 1);
  assert.equal(gs.score, 1);
});

test('reconcileRegularCheckpoint returns null for unusable checkpoints', () => {
  assert.equal(L.reconcileRegularCheckpoint(null, new Map()), null);
  assert.equal(L.reconcileRegularCheckpoint({ questionIds: [1] }, new Map()), null);
  assert.equal(L.reconcileRegularCheckpoint({ questionIds: [1], answers: [] }, new Map()), null);
});

test('reconcileRegularCheckpoint: a fully answered checkpoint lands at the end', () => {
  const byId = new Map([[1, q(1)], [2, q(2)]]);
  const cp = { questionIds: [1, 2], answers: [
    { questionId: 1, correct: true, selectedText: 'a' },
    { questionId: 2, correct: true, selectedText: 'a' },
  ] };
  const gs = L.reconcileRegularCheckpoint(cp, byId);
  assert.equal(gs.currentIndex, gs.questions.length);
  assert.equal(gs.currentStreak, 2);
});
