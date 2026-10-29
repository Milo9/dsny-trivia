// Shared pure persistence rules. Both adapters and the emulator tests run this code.
function scoreReset(user) {
  return { ...user, totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0,
    dailyStreak: 0, lastDailyDate: null, lastDailyScore: null, lastDailyPoints: 0,
    lastDailyAnswers: null, prevDailyDate: null, prevDailyScore: null,
    prevDailyPoints: 0, prevDailyAnswers: null, categoryStats: {},
    monthlyKey: null, monthlyPoints: 0, prevMonthlyKey: null, prevMonthlyPoints: 0,
    monthlyTotals: {}, completedDailyDates: [], missedQuestionIds: [], questionStats: {},
    recentQuestionIds: [], gameLog: [], resetRevision: (user.resetRevision || 0) + 1 };
}

function validPlayerBackup(u) {
  const count=n=>Number.isSafeInteger(n) && n>=0;
  if(!u || typeof u.id!=='string' || !u.id || u.id.includes('/') || u.id==='__proto__'
    || typeof u.name!=='string' || !u.name.trim() || u.name.length>20) return false;
  if(!['totalAnswered','totalCorrect','gamesPlayed','totalPoints'].every(k=>count(u[k])) || u.totalCorrect>u.totalAnswered) return false;
  if('resetRevision' in u && !count(u.resetRevision)) return false;
  const map=value=>value && typeof value==='object' && !Array.isArray(value);
  for(const key of ['categoryStats','questionStats']) if(key in u) {
    if(!map(u[key]) || !Object.values(u[key]).every(s=>map(s) && count(s.answered) && count(s.correct) && s.correct<=s.answered)) return false;
  }
  if('monthlyTotals' in u && (!map(u.monthlyTotals) || !Object.entries(u.monthlyTotals).every(([k,v])=>/^\d{4}-\d{2}$/.test(k) && count(v)))) return false;
  for(const key of ['monthlyPoints','prevMonthlyPoints','dailyStreak']) if(key in u && !count(u[key])) return false;
  for(const key of ['recentQuestionIds','missedQuestionIds']) if(key in u && (!Array.isArray(u[key]) || !u[key].every(id=>count(id) && id>0))) return false;
  if('completedDailyDates' in u && (!Array.isArray(u.completedDailyDates) || !u.completedDailyDates.every(d=>typeof d==='string' && /^\d{4}-\d{2}-\d{2}$/.test(d)))) return false;
  return true;
}

function effectivePeriodPoints(user, key) {
  if (user.monthlyTotals && Object.hasOwn(user.monthlyTotals, key)) return user.monthlyTotals[key];
  return user.monthlyKey === key ? user.monthlyPoints || 0
    : user.prevMonthlyKey === key ? user.prevMonthlyPoints || 0 : 0;
}

function prepareStatsUpdate(user, args, op) {
  const [answered, correct, points, daily, cats, recent, period, log] = args;
  if (op && (op.resetRevision || 0) !== (user.resetRevision || 0)) {
    const error = new Error('Scores were reset. This old game can no longer be saved.');
    error.code = 'reset-game';
    throw error;
  }
  const u = JSON.parse(JSON.stringify(user));
  const date = op?.dateKey || daily?.dateKey;
  const dates = new Set(u.completedDailyDates || []);
  if (u.lastDailyDate) dates.add(u.lastDailyDate);
  if (u.prevDailyDate) dates.add(u.prevDailyDate);
  const firstDaily = !!daily && !dates.has(date);
  let streak = 0;
  if (daily) {
    let cursor = date;
    do {
      streak++;
      cursor = new Date(Date.parse(cursor + 'T12:00:00Z') - 86400000).toISOString().slice(0, 10);
    } while (dates.has(cursor));
  }
  const breakdown = op ? scoreBreakdown(op.answers, firstDaily, streak, op.complete) : null;
  const earned = breakdown ? breakdown.total : points;
  u.totalAnswered = (u.totalAnswered || 0) + answered;
  u.totalCorrect = (u.totalCorrect || 0) + correct;
  u.gamesPlayed = (u.gamesPlayed || 0) + 1;
  u.totalPoints = (u.totalPoints || 0) + earned;
  if (period) {
    const totals = { ...(u.monthlyTotals || {}) };
    if (u.monthlyKey && !Object.hasOwn(totals, u.monthlyKey)) totals[u.monthlyKey] = u.monthlyPoints || 0;
    if (u.prevMonthlyKey && !Object.hasOwn(totals, u.prevMonthlyKey)) totals[u.prevMonthlyKey] = u.prevMonthlyPoints || 0;
    totals[period] = (totals[period] || 0) + earned;
    u.monthlyTotals = totals;
    const keys = Object.keys(totals).sort().reverse();
    u.monthlyKey = keys[0]; u.monthlyPoints = totals[keys[0]];
    u.prevMonthlyKey = keys[1] || null; u.prevMonthlyPoints = totals[keys[1]] || 0;
  }
  u.categoryStats = { ...(u.categoryStats || {}) };
  for (const [cat, counts] of Object.entries(cats || {})) {
    const old = u.categoryStats[cat] || { answered: 0, correct: 0 };
    u.categoryStats[cat] = { answered: old.answered + counts.answered, correct: old.correct + counts.correct };
  }
  u.recentQuestionIds = capSeenIds(u.recentQuestionIds || [], recent || []);
  if (op) {
    const missed = new Set(u.missedQuestionIds || []);
    u.questionStats = { ...(u.questionStats || {}) };
    for (const a of op.answers) {
      const id = a.question.id;
      if (a.correct) missed.delete(id); else missed.add(id);
      const old = u.questionStats[id] || { answered: 0, correct: 0 };
      u.questionStats[id] = { answered: old.answered + 1, correct: old.correct + Number(a.correct) };
    }
    u.missedQuestionIds = [...missed];
  }
  if (daily) {
    dates.add(date);
    u.completedDailyDates = [...dates].sort();
    const summaries = [
      u.lastDailyDate && { date: u.lastDailyDate, score: u.lastDailyScore, points: u.lastDailyPoints, answers: u.lastDailyAnswers },
      u.prevDailyDate && { date: u.prevDailyDate, score: u.prevDailyScore, points: u.prevDailyPoints, answers: u.prevDailyAnswers },
      { date, score: correct, points: earned, answers: daily.answers }
    ].filter(Boolean).sort((a, b) => b.date.localeCompare(a.date));
    const unique = summaries.filter((v, i) => summaries.findIndex(x => x.date === v.date) === i);
    const latest = unique[0], prev = unique[1];
    u.lastDailyDate = latest.date; u.lastDailyScore = latest.score ?? 0; u.lastDailyPoints = latest.points ?? 0;
    u.lastDailyAnswers = latest.answers || null;
    if (prev) {
      u.prevDailyDate = prev.date; u.prevDailyScore = prev.score ?? 0; u.prevDailyPoints = prev.points ?? 0;
      u.prevDailyAnswers = prev.answers || null;
    }
    let last = latest.date, current = 0;
    while (dates.has(last)) {
      current++;
      last = new Date(Date.parse(last + 'T12:00:00Z') - 86400000).toISOString().slice(0, 10);
    }
    u.dailyStreak = current;
  }
  if (log) u.gameLog = appendGameLog(u.gameLog, { ...log, points: earned, ...(daily ? { firstDaily } : {}) });
  return { user: u, breakdown, firstDaily, points: earned, score: correct,
    answers: op ? serializeAnswers(op.answers) : null };
}

function mutateHomework(current, action, movies, week, at, rng = Math.random) {
  let state = current ? JSON.parse(JSON.stringify(current)) : null;
  if (state && !state.watched) {
    state.watched = (state.watchedIds || []).map(id => ({ id, watchedAt: state.pickedAt || at }));
    delete state.watchedIds;
  }
  if (!state || state.weekKey !== week) {
    // Unconfirmed assignments remain unwatched and eligible for a future week.
    const watched = state?.watched || [];
    const { movie } = pickMovie(movies, [...watched.map(w => w.id), ...(state ? [state.movieId] : [])], rng);
    if (!movie) throw new Error('No movies available.');
    state = { weekKey: week, movieId: movie.id, pickedAt: at, watched };
  }
  if (action.type === 'shuffle') {
    const { movie } = pickMovie(movies, [...state.watched.map(w => w.id), state.movieId], rng);
    if (movie) { state.movieId = movie.id; state.pickedAt = at; }
  } else if (action.type === 'unwatch') {
    state.watched = state.watched.filter(w => w.id !== action.movieId);
  } else if (action.type === 'watch') {
    state.watched = state.watched.filter(w => w.id !== state.movieId)
      .concat({ id: state.movieId, watchedAt: at });
  }
  return state;
}

if (typeof module !== 'undefined' && module.exports) {
  Object.assign(globalThis, require('./game-logic.js'));
  module.exports = { prepareStatsUpdate, scoreReset, effectivePeriodPoints, mutateHomework, validPlayerBackup };
}
