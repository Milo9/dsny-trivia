const APP_VERSION = '1.10';

// =============================================================================
// State
// =============================================================================
let QUESTIONS     = [];
let MOVIES        = [];
let currentUser   = null;
let gameSettings  = { difficulty: 'all', categories: ['movies','characters','parks','walt','cruise','music','pixar'], questionCount: 10 };
let gameState     = { questions: [], currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: false, pointsEarned: 0, scoreBreakdown: null };
let shuffledOpts  = [];   // [{text, originalIndex}] for current question display
let homeworkState = null; // { weekKey, movieId, pickedAt, watchedIds[] } — this week's Weekly Homework pick

// =============================================================================
// Utilities
// =============================================================================
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const SEEN_MAX = 300;

function getSeenIds(userId) {
  try { return JSON.parse(localStorage.getItem('disney_seen_' + userId)) || []; }
  catch { return []; }
}

function addSeenIds(userId, ids) {
  let seen = getSeenIds(userId).concat(ids);
  if (seen.length > SEEN_MAX) seen = seen.slice(seen.length - SEEN_MAX);
  localStorage.setItem('disney_seen_' + userId, JSON.stringify(seen));
}

function pct(correct, total) {
  return total ? Math.round((correct / total) * 100) + '%' : '—';
}

function initials(name) {
  return name.trim().split(/\s+/).map(w => w[0].toUpperCase()).join('').slice(0, 2);
}

const DISNEY_AVATARS = ['🐭','👸','🦁','🤠','🐠','❄️','🧚','🧞'];

function disneyAvatar(name) {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffff;
  return DISNEY_AVATARS[h % DISNEY_AVATARS.length];
}

function slugId(name) {
  return name.toLowerCase().replace(/\s+/g, '_') + '_' + Date.now();
}

const CAT_LABELS = {
  movies: '🎬 Movies', characters: '🐭 Characters', parks: '🏰 Disney Parks',
  walt: '🎩 Walt Disney', cruise: '⛴️ Cruise Line', music: '🎵 Music & Songs', pixar: '💡 Pixar'
};

function catLabel(c) { return CAT_LABELS[c] || c; }

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

// --- Daily challenge helpers ---

// Daily resets at 2am Mountain Time (UTC-6 summer / MDT).
// Subtracting 8h shifts the UTC day boundary to 8am UTC = 2am MDT = 4am EDT.
// getUTC* is correct here because the offset is baked into the timestamp.
// daysAgo=0 → today, daysAgo=1 → yesterday (same 8h offset, no string arithmetic).
function dayKey(daysAgo = 0) {
  const d = new Date(Date.now() - 8 * 3600000 - daysAgo * 86400000);
  return `${d.getUTCFullYear()}-${String(d.getUTCMonth()+1).padStart(2,'0')}-${String(d.getUTCDate()).padStart(2,'0')}`;
}
function todayKey() { return dayKey(0); }

// Returns calendar days between two "YYYY-MM-DD" keys. Returns Infinity if prev is falsy.
function computeDaysDiff(prev, today) {
  if (!prev) return Infinity;
  const [py, pm, pd] = prev.split('-').map(Number);
  const [ty, tm, td] = today.split('-').map(Number);
  return Math.round((new Date(ty, tm - 1, td) - new Date(py, pm - 1, pd)) / 86400000);
}

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

// --- Weekly Homework helpers ---

// Same 8h-shift trick as dayKey(): rolls over at 08:00 UTC = 3am EST / 4am EDT.
// Returns the date key ("YYYY-MM-DD") of the most recent Thursday at/after that boundary,
// i.e. the identifier for the current homework week.
function homeworkWeekKey() {
  const shifted = new Date(Date.now() - 8 * 3600000);
  const day  = shifted.getUTCDay();       // 0=Sun ... 4=Thu
  const diff = (day - 4 + 7) % 7;         // days since the most recent Thursday
  shifted.setUTCDate(shifted.getUTCDate() - diff);
  return `${shifted.getUTCFullYear()}-${String(shifted.getUTCMonth()+1).padStart(2,'0')}-${String(shifted.getUTCDate()).padStart(2,'0')}`;
}

// Picks a random movie not in excludeIds. If that leaves nothing, falls back to the
// full pool (reset: true) so the pool never runs dry.
function pickFromMoviePool(excludeIds) {
  const excl = new Set(excludeIds);
  let candidates = MOVIES.filter(m => !excl.has(m.id));
  let reset = false;
  if (candidates.length === 0) { candidates = MOVIES; reset = true; }
  return { movie: candidates[Math.floor(Math.random() * candidates.length)], reset };
}

// Stable-sorts by id first so shard/load order doesn't affect the result.
function getDailyQuestions(count = 10, daysAgo = 0) {
  const sorted = [...QUESTIONS].sort((a, b) => a.id - b.id);
  return seededShuffle(sorted, dateToSeed(dayKey(daysAgo))).slice(0, count);
}

// =============================================================================
// Scoring
// =============================================================================
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
function scoreBreakdown(answers, earnDailyBonus, dailyStreak) {
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
  const perfectBonus = (answers.length > 0 && answers.every(a => a.correct)) ? SCORING.perfect : 0;
  let dailyBonus = 0;
  if (earnDailyBonus) {
    dailyBonus = SCORING.dailyFlat + Math.min(dailyStreak, SCORING.dailyStreakCap) * SCORING.dailyPerDay;
  }
  return { base, streakBonus, perfectBonus, dailyBonus, total: base + streakBonus + perfectBonus + dailyBonus };
}

// =============================================================================
// Sound effects (Web Audio API, synthesized — no audio files needed)
// =============================================================================
const sounds = (() => {
  let ctx = null;
  let _muted = localStorage.getItem('disney_sound_muted') === '1';

  function getCtx() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function tone(freq, start, dur, type = 'sine', vol = 0.28) {
    try {
      const c  = getCtx();
      const osc = c.createOscillator();
      const g   = c.createGain();
      osc.connect(g); g.connect(c.destination);
      osc.type = type;
      osc.frequency.value = freq;
      const t0 = c.currentTime + start;
      g.gain.setValueAtTime(0, t0);
      g.gain.linearRampToValueAtTime(vol, t0 + 0.01);
      g.gain.linearRampToValueAtTime(0,   t0 + dur);
      osc.start(t0);
      osc.stop(t0 + dur + 0.02);
    } catch(e) {}
  }

  return {
    get muted() { return _muted; },
    toggle() {
      _muted = !_muted;
      localStorage.setItem('disney_sound_muted', _muted ? '1' : '0');
      return _muted;
    },
    correct() {
      if (_muted) return;
      tone(523.25, 0,   0.12); // C5
      tone(659.25, 0.1, 0.20); // E5
    },
    wrong() {
      if (_muted) return;
      tone(220, 0, 0.30, 'triangle', 0.18); // A3 — dull thud
    },
    fanfare() {
      if (_muted) return;
      [[523.25,0],[659.25,0.13],[783.99,0.26],[1046.5,0.39]].forEach(([f,t]) => tone(f, t, 0.22));
    }
  };
})();

// =============================================================================
// Screen navigation
// =============================================================================
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');
  window.scrollTo(0, 0);
}

// =============================================================================
// HOME SCREEN
// =============================================================================
async function renderHome() {
  showScreen('screen-home');
  document.getElementById('app-version').textContent = 'v' + APP_VERSION;

  document.getElementById('add-user-form').classList.add('hidden');
  document.getElementById('btn-show-add-user').classList.remove('hidden');
  document.getElementById('new-user-input').value = '';

  const list = document.getElementById('user-list');
  list.innerHTML = '';

  let users;
  try {
    users = await storage.getUsers();
  } catch (e) {
    list.innerHTML = `<p class="load-error">Couldn't load players.<br><small>${e.message || e}</small><br><a href="" onclick="location.reload()">Tap to retry</a></p>`;
    return;
  }

  const lastId = localStorage.getItem('disney_last_user');
  const today  = todayKey();

  users.forEach(user => {
    const card       = document.createElement('div');
    card.className   = 'user-card';
    const streak     = user.dailyStreak || 0;
    const streakText = streak > 0 ? ` · 🔥 ${streak}` : '';
    const pts        = user.totalPoints || 0;
    const stat       = user.totalAnswered
      ? `${pts.toLocaleString()} pts · ${pct(user.totalCorrect, user.totalAnswered)} correct${streakText}`
      : streak > 0 ? `🔥 ${streak} day streak` : 'No games yet';
    card.innerHTML = `
      <div class="user-avatar">${disneyAvatar(user.name)}</div>
      <div class="user-info">
        <div class="user-name">${user.name}</div>
        <div class="user-stats">${stat}</div>
      </div>
      <span class="user-arrow">›</span>
    `;
    card.addEventListener('click', () => selectUser(user));
    list.appendChild(card);
    if (user.id === lastId) card.style.borderColor = 'var(--primary)';
  });

  // Daily challenge comparison card
  const dailyCard = document.getElementById('daily-card');
  const dailyBody = document.getElementById('daily-card-body');
  dailyBody.innerHTML = '';
  users.forEach(user => {
    const played = user.lastDailyDate === today;
    const row    = document.createElement('div');
    row.className = 'daily-cmp-row';
    if (played) {
      row.innerHTML = `
        <span class="dcmp-name">${disneyAvatar(user.name)} ${user.name}</span>
        <span class="dcmp-score">${user.lastDailyScore ?? 0}/10 · <strong>${(user.lastDailyPoints||0).toLocaleString()} pts</strong> ✓</span>
      `;
    } else {
      row.innerHTML = `
        <span class="dcmp-name">${disneyAvatar(user.name)} ${user.name}</span>
        <span class="dcmp-not-played">—</span>
      `;
    }
    dailyBody.appendChild(row);
  });
  dailyCard.classList.toggle('hidden', users.length === 0);

  // Yesterday's challenge — checks lastDailyDate (haven't played today yet) and
  // prevDailyDate (already played today, yesterday's data shifted to prev slot)
  const yesterday     = dayKey(1);
  const yesterdayCard = document.getElementById('yesterday-card');
  const yesterdayBody = document.getElementById('yesterday-card-body');
  yesterdayBody.innerHTML = '';
  const getYesterdayData = u => {
    if (u.lastDailyDate === yesterday) return { score: u.lastDailyScore, points: u.lastDailyPoints };
    if (u.prevDailyDate === yesterday) return { score: u.prevDailyScore, points: u.prevDailyPoints };
    return null;
  };
  const anyYesterday = users.some(u => getYesterdayData(u));
  if (anyYesterday) {
    users.forEach(user => {
      const yd  = getYesterdayData(user);
      const row = document.createElement('div');
      row.className = 'daily-cmp-row';
      if (yd) {
        row.innerHTML = `
          <span class="dcmp-name">${disneyAvatar(user.name)} ${user.name}</span>
          <span class="dcmp-score">${yd.score ?? 0}/10 · <strong>${(yd.points||0).toLocaleString()} pts</strong> ✓</span>
        `;
      } else {
        row.innerHTML = `
          <span class="dcmp-name">${disneyAvatar(user.name)} ${user.name}</span>
          <span class="dcmp-not-played">—</span>
        `;
      }
      yesterdayBody.appendChild(row);
    });
  }
  yesterdayCard.classList.toggle('hidden', !anyYesterday);

  renderHomeworkCard();
}

function selectUser(user) {
  currentUser = user;
  localStorage.setItem('disney_last_user', user.id);
  renderSettings();
}

// Add player
document.getElementById('btn-show-add-user').addEventListener('click', () => {
  document.getElementById('add-user-form').classList.remove('hidden');
  document.getElementById('btn-show-add-user').classList.add('hidden');
  document.getElementById('new-user-input').focus();
});

document.getElementById('btn-cancel-add-user').addEventListener('click', () => {
  document.getElementById('add-user-form').classList.add('hidden');
  document.getElementById('btn-show-add-user').classList.remove('hidden');
  document.getElementById('new-user-input').value = '';
});

document.getElementById('btn-add-user').addEventListener('click', addUser);
document.getElementById('new-user-input').addEventListener('keydown', e => { if (e.key === 'Enter') addUser(); });

async function addUser() {
  const input = document.getElementById('new-user-input');
  const name  = input.value.trim();
  if (!name) return;
  await storage.saveUser({ id: slugId(name), name, totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0 });
  renderHome();
}

// Leaderboard links
document.getElementById('btn-go-leaderboard').addEventListener('click', renderLeaderboard);
document.getElementById('btn-leaderboard-back').addEventListener('click', () => renderHome());
document.getElementById('btn-results-leaderboard').addEventListener('click', renderLeaderboard);

// =============================================================================
// LEADERBOARD
// =============================================================================
async function renderLeaderboard() {
  showScreen('screen-leaderboard');
  const users = await storage.getLeaderboard();
  const list  = document.getElementById('leaderboard-list');
  const empty = document.getElementById('leaderboard-empty');
  list.innerHTML = '';

  const medals = ['🥇', '🥈', '🥉'];

  if (!users.length) { empty.classList.remove('hidden'); return; }
  empty.classList.add('hidden');

  users.forEach((u, i) => {
    const entry      = document.createElement('div');
    entry.className  = `lb-entry${i < 3 ? ' rank-' + (i + 1) : ''}`;
    const percentage = u.totalAnswered ? Math.round((u.totalCorrect / u.totalAnswered) * 100) : null;
    const detail     = u.totalAnswered
      ? `${u.totalAnswered} q · ${u.gamesPlayed} game${u.gamesPlayed !== 1 ? 's' : ''}`
      : 'No games yet';
    const pts = (u.totalPoints || 0).toLocaleString();
    entry.innerHTML = `
      <div class="lb-rank">${medals[i] || (i + 1)}</div>
      <div class="lb-avatar">${disneyAvatar(u.name)}</div>
      <div class="lb-info">
        <div class="lb-name">${u.name}</div>
        <div class="lb-detail">${detail}</div>
      </div>
      <div class="lb-score-block">
        <div class="lb-pts">${pts}</div>
        <div class="lb-pct">${percentage !== null ? percentage + '%' : '—'}</div>
      </div>
    `;
    list.appendChild(entry);
  });
}

// =============================================================================
// WEEKLY HOMEWORK — a new movie assigned every Thursday for family movie night
// =============================================================================

// Called once at boot. If the stored pick belongs to a prior homework week, the
// outgoing movie is assumed watched (homework complete!) and a fresh one is drawn
// from the unwatched pool. Never called by the shuffle button — rollover and veto
// must stay separate, since only rollover marks a movie watched.
async function rollHomeworkIfStale() {
  let state = null;
  try { state = await storage.getHomeworkState(); } catch(e) {}
  const wk = homeworkWeekKey();

  if (state && state.weekKey === wk) {
    homeworkState = state;
    return;
  }

  let watchedIds = state ? [...new Set(state.watchedIds || [])] : [];
  if (state && state.movieId != null && !watchedIds.includes(state.movieId)) {
    watchedIds.push(state.movieId);
  }

  const { movie, reset } = pickFromMoviePool(watchedIds);
  if (reset) watchedIds = []; // pool exhausted — everything's fair game again

  homeworkState = { weekKey: wk, movieId: movie.id, pickedAt: new Date().toISOString(), watchedIds };
  try { await storage.saveHomeworkState(homeworkState); } catch(e) {}
}

// Vetoes the current pick and draws a new one from the pool. The vetoed movie goes
// back into the pool — it is NOT added to watchedIds. Kristen-only (gated in the UI).
async function shuffleHomework() {
  if (!homeworkState) return;
  const exclude = [...(homeworkState.watchedIds || []), homeworkState.movieId];
  const { movie } = pickFromMoviePool(exclude);
  homeworkState = { ...homeworkState, movieId: movie.id, pickedAt: new Date().toISOString() };
  try { await storage.saveHomeworkState(homeworkState); } catch(e) {}
}

function renderHomeworkCard() {
  const card = document.getElementById('homework-card');
  if (!homeworkState || !MOVIES.length) { card.classList.add('hidden'); return; }
  const movie = MOVIES.find(m => m.id === homeworkState.movieId);
  if (!movie) { card.classList.add('hidden'); return; }

  card.classList.remove('hidden');
  document.getElementById('homework-movie-title').textContent = `${movie.title} (${movie.year})`;

  const isKristen = localStorage.getItem('disney_last_user') === 'kristen';
  document.getElementById('btn-shuffle-homework').classList.toggle('hidden', !isKristen);
}

document.getElementById('btn-shuffle-homework').addEventListener('click', async () => {
  const btn = document.getElementById('btn-shuffle-homework');
  btn.disabled = true;
  await shuffleHomework();
  renderHomeworkCard();
  btn.disabled = false;
});

// =============================================================================
// SETTINGS SCREEN
// =============================================================================
const CAT_ORDER = ['movies', 'characters', 'parks', 'walt', 'cruise', 'music', 'pixar'];

function renderCatStats(user) {
  const section = document.getElementById('cat-stats-section');
  const body    = document.getElementById('cat-stats-body');
  const stats   = user.categoryStats || {};
  const played  = CAT_ORDER.filter(c => stats[c] && stats[c].answered > 0);
  if (played.length === 0) { section.classList.add('hidden'); return; }
  section.classList.remove('hidden');
  body.innerHTML = played.map(c => {
    const { answered, correct } = stats[c];
    const p = Math.round(correct / answered * 100);
    return `<div class="cstat-row">
      <span class="cstat-label">${catLabel(c)}</span>
      <div class="cstat-bar-wrap"><div class="cstat-bar cstat-${c}" style="width:${p}%"></div></div>
      <span class="cstat-pct">${p}%</span>
      <span class="cstat-count">${answered}q</span>
    </div>`;
  }).join('');
}

function renderSettings() {
  showScreen('screen-settings');
  document.getElementById('settings-user-name').textContent = currentUser.name;
  renderCatStats(currentUser);
  updateAvailableHint();

  const today    = todayKey();
  const streak   = currentUser.dailyStreak || 0;
  const played   = currentUser.lastDailyDate === today;
  const statusEl = document.getElementById('daily-status');
  const btn      = document.getElementById('btn-daily-challenge');

  if (played) {
    statusEl.textContent = `✓ Played today · 🔥 ${streak} day streak`;
    statusEl.className   = 'daily-status daily-done';
    btn.textContent      = '📋 Review Today\'s Questions';
    btn.classList.add('done');
  } else if (streak > 0) {
    statusEl.textContent = `🔥 ${streak} day streak — keep it going!`;
    statusEl.className   = 'daily-status daily-active';
    btn.textContent      = '⭐ Daily Challenge';
    btn.classList.remove('done');
  } else {
    statusEl.textContent = 'Same 10 questions for everyone today. Start your streak!';
    statusEl.className   = 'daily-status';
    btn.textContent      = '⭐ Daily Challenge';
    btn.classList.remove('done');
  }
}

document.getElementById('btn-settings-back').addEventListener('click', renderHome);

document.getElementById('btn-daily-challenge').addEventListener('click', async () => {
  const today = todayKey();
  if (currentUser.lastDailyDate === today) {
    renderDailyReview('settings', 0);
    return;
  }

  const btn = document.getElementById('btn-daily-challenge');
  btn.disabled = true;

  let questions;
  try {
    const pinnedIds = await storage.getDailyPins(today);
    if (pinnedIds && pinnedIds.length > 0) {
      const qMap = new Map(QUESTIONS.map(q => [q.id, q]));
      const qs = pinnedIds.map(id => qMap.get(id)).filter(Boolean);
      if (qs.length > 0) questions = qs;
    }
  } catch(e) {}

  if (!questions) {
    questions = getDailyQuestions(10);
    try { await storage.saveDailyPins(today, questions.map(q => q.id)); } catch(e) {}
  }

  btn.disabled = false;
  gameState = { questions, currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: true, pointsEarned: 0, scoreBreakdown: null };
  renderGameQuestion();
});

// Difficulty pills
document.getElementById('difficulty-group').addEventListener('click', e => {
  const pill = e.target.closest('.pill');
  if (!pill) return;
  document.querySelectorAll('#difficulty-group .pill').forEach(p => p.classList.remove('active'));
  pill.classList.add('active');
  gameSettings.difficulty = pill.dataset.value;
  updateAvailableHint();
});

// Count pills
document.getElementById('count-group').addEventListener('click', e => {
  const pill = e.target.closest('.pill');
  if (!pill) return;
  document.querySelectorAll('#count-group .pill').forEach(p => p.classList.remove('active'));
  pill.classList.add('active');
  gameSettings.questionCount = parseInt(pill.dataset.value, 10);
  updateAvailableHint();
});

// Category checkboxes
document.getElementById('category-grid').addEventListener('change', () => {
  gameSettings.categories = [...document.querySelectorAll('#category-grid input:checked')].map(i => i.value);
  const err = document.getElementById('cat-error');
  err.classList.toggle('hidden', gameSettings.categories.length > 0);
  updateAvailableHint();
});

function filteredPool() {
  return QUESTIONS.filter(q => {
    const diffOk = gameSettings.difficulty === 'all' || q.difficulty === gameSettings.difficulty;
    return diffOk && gameSettings.categories.includes(q.category);
  });
}

function updateAvailableHint() {
  const pool    = filteredPool();
  const desired = gameSettings.questionCount;
  const hint    = document.getElementById('available-hint');
  if (pool.length === 0) {
    hint.textContent = 'No questions match these filters.';
  } else if (pool.length < desired) {
    hint.textContent = `Only ${pool.length} question${pool.length !== 1 ? 's' : ''} match — the game will use all of them.`;
  } else {
    hint.textContent = `${pool.length} questions available.`;
  }
}

document.getElementById('btn-start-game').addEventListener('click', () => {
  if (gameSettings.categories.length === 0) {
    document.getElementById('cat-error').classList.remove('hidden');
    return;
  }
  const pool  = filteredPool();
  if (pool.length === 0) return;
  const count = Math.min(gameSettings.questionCount, pool.length);

  const seen  = new Set(getSeenIds(currentUser.id));
  const fresh = pool.filter(q => !seen.has(q.id));
  const src   = fresh.length >= count ? fresh : pool;

  gameState = { questions: shuffle(src).slice(0, count), currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: false, pointsEarned: 0, scoreBreakdown: null };
  renderGameQuestion();
});

// =============================================================================
// GAME SCREEN
// =============================================================================
function renderGameQuestion() {
  showScreen('screen-game');
  const q     = gameState.questions[gameState.currentIndex];
  const total = gameState.questions.length;
  const cur   = gameState.currentIndex + 1;

  document.getElementById('game-progress').textContent      = `Q ${cur} of ${total}`;
  document.getElementById('progress-fill').style.width      = `${((cur - 1) / total) * 100}%`;
  document.getElementById('game-score-display').textContent = `${gameState.score} ✓`;
  document.getElementById('game-cat-badge').textContent     = catLabel(q.category);

  const diffEl = document.getElementById('question-diff');
  diffEl.textContent = q.difficulty.charAt(0).toUpperCase() + q.difficulty.slice(1);
  diffEl.className   = `diff-badge diff-${q.difficulty}`;

  document.getElementById('question-text').textContent = q.question;

  const indices = shuffle([0, 1, 2, 3]);
  shuffledOpts  = indices.map(i => ({ text: q.answers[i], originalIndex: i }));

  const grid   = document.getElementById('answers-grid');
  grid.innerHTML = '';
  const letters = ['A', 'B', 'C', 'D'];

  shuffledOpts.forEach((opt, i) => {
    const btn = document.createElement('button');
    btn.className = 'answer-btn';
    btn.dataset.idx = i;
    btn.innerHTML = `<span class="answer-letter">${letters[i]}</span><span>${opt.text}</span>`;
    btn.addEventListener('click', () => handleAnswer(i));
    grid.appendChild(btn);
  });

  const banner = document.getElementById('streak-banner');
  if (gameState.currentStreak >= 2) {
    document.getElementById('streak-count').textContent = gameState.currentStreak;
    banner.classList.remove('hidden');
  } else {
    banner.classList.add('hidden');
  }

  const muteBtn = document.getElementById('btn-mute-sound');
  muteBtn.textContent = sounds.muted ? '🔇' : '🔊';
  muteBtn.classList.toggle('muted', sounds.muted);

  document.getElementById('feedback-area').classList.add('hidden');
  document.getElementById('flag-form').classList.add('hidden');
  document.getElementById('flag-thanks').classList.add('hidden');
  document.getElementById('flag-comment').value = '';
  document.getElementById('btn-flag').classList.remove('active');
}

function handleAnswer(selectedIdx) {
  const q         = gameState.questions[gameState.currentIndex];
  const chosen    = shuffledOpts[selectedIdx];
  const isCorrect = chosen.originalIndex === 0;

  document.querySelectorAll('.answer-btn').forEach(b => b.disabled = true);

  document.querySelectorAll('.answer-btn').forEach((b, i) => {
    if (shuffledOpts[i].originalIndex === 0) {
      b.classList.add(i === selectedIdx ? 'correct' : 'reveal');
    } else if (i === selectedIdx && !isCorrect) {
      b.classList.add('wrong');
    }
  });

  if (isCorrect) {
    gameState.score++;
    gameState.currentStreak++;
    sounds.correct();
  } else {
    gameState.currentStreak = 0;
    sounds.wrong();
  }

  const banner = document.getElementById('streak-banner');
  if (gameState.currentStreak >= 2) {
    document.getElementById('streak-count').textContent = gameState.currentStreak;
    banner.classList.remove('hidden');
    // Re-trigger pop animation
    banner.style.animation = 'none';
    banner.offsetHeight;
    banner.style.animation = '';
  } else {
    banner.classList.add('hidden');
  }

  gameState.answers.push({ question: q, selectedText: chosen.text, correct: isCorrect });
  document.getElementById('game-score-display').textContent = `${gameState.score} ✓`;

  const feedbackMsg = document.getElementById('feedback-msg');
  if (isCorrect) {
    feedbackMsg.textContent = '✓ Correct!';
    feedbackMsg.className   = 'feedback-msg fb-correct';
  } else {
    feedbackMsg.textContent = `✗ The correct answer was: ${q.answers[0]}`;
    feedbackMsg.className   = 'feedback-msg fb-wrong';
  }

  const isLast = gameState.currentIndex === gameState.questions.length - 1;
  document.getElementById('btn-next').textContent = isLast ? 'See Results ✨' : 'Next →';
  document.getElementById('feedback-area').classList.remove('hidden');
}

document.getElementById('btn-next').addEventListener('click', () => {
  gameState.currentIndex++;
  if (gameState.currentIndex >= gameState.questions.length) {
    endGame();
  } else {
    renderGameQuestion();
  }
});

// Exit game
document.getElementById('btn-exit-game').addEventListener('click', async () => {
  const answered = gameState.answers.length;
  const msg = answered > 0
    ? `Exit this game? Your ${answered} answered question${answered !== 1 ? 's' : ''} will be saved to your stats.`
    : 'Exit this game? You haven\'t answered any questions yet.';
  if (confirm(msg)) {
    if (answered > 0) {
      const pts = scoreBreakdown(gameState.answers, false, 0).total;
      await storage.updateStats(currentUser.id, answered, gameState.score, pts, null, buildCatStats(gameState.answers));
      addSeenIds(currentUser.id, gameState.answers.map(a => a.question.id));
    }
    renderHome();
  }
});

// Mute toggle
document.getElementById('btn-mute-sound').addEventListener('click', () => {
  const muted = sounds.toggle();
  const btn   = document.getElementById('btn-mute-sound');
  btn.textContent = muted ? '🔇' : '🔊';
  btn.classList.toggle('muted', muted);
});

// Flag / thumbs-down
document.getElementById('btn-flag').addEventListener('click', () => {
  const form   = document.getElementById('flag-form');
  const thanks = document.getElementById('flag-thanks');
  const btn    = document.getElementById('btn-flag');
  if (thanks.classList.contains('hidden')) {
    const opening = form.classList.toggle('hidden');
    btn.classList.toggle('active', !opening);
    if (!opening) document.getElementById('flag-comment').focus();
  }
});

document.getElementById('btn-flag-cancel').addEventListener('click', () => {
  document.getElementById('flag-form').classList.add('hidden');
  document.getElementById('btn-flag').classList.remove('active');
});

document.getElementById('btn-flag-submit').addEventListener('click', submitFlag);
document.getElementById('flag-comment').addEventListener('keydown', e => { if (e.key === 'Enter') submitFlag(); });

async function submitFlag() {
  const q       = gameState.questions[gameState.currentIndex];
  const comment = document.getElementById('flag-comment').value.trim();
  await storage.flagReport({
    questionId:    q.id,
    questionText:  q.question,
    correctAnswer: q.answers[0],
    allAnswers:    q.answers,
    difficulty:    q.difficulty,
    category:      q.category,
    reportedBy:    currentUser.name,
    comment:       comment || null,
    timestamp:     new Date().toISOString()
  });
  document.getElementById('flag-form').classList.add('hidden');
  document.getElementById('flag-thanks').classList.remove('hidden');
  document.getElementById('btn-flag').classList.remove('active');
  document.getElementById('btn-flag').disabled = true;
}

// =============================================================================
// RESULTS SCREEN
// =============================================================================
async function endGame() {
  const today             = todayKey();
  const isFirstDailyToday = gameState.isDaily && currentUser.lastDailyDate !== today;

  // Compute new daily streak before scoring so the bonus uses the correct level
  let newDailyStreak = currentUser.dailyStreak || 0;
  if (isFirstDailyToday) {
    const diff = computeDaysDiff(currentUser.lastDailyDate, today);
    newDailyStreak = diff === 1 ? (currentUser.dailyStreak || 0) + 1 : 1;
  }

  const bd = scoreBreakdown(gameState.answers, isFirstDailyToday, newDailyStreak);
  gameState.pointsEarned   = bd.total;
  gameState.scoreBreakdown = bd;

  // Always save score/pts display fields for any daily game.
  // streak/answers only updated on first play (null tells storage to leave them unchanged).
  const dailyUpdate = gameState.isDaily ? {
    score:   gameState.score,
    points:  bd.total,
    dateKey: today,
    streak:  isFirstDailyToday ? newDailyStreak : null,
    answers: isFirstDailyToday ? gameState.answers.map(a => ({
      questionId:   a.question.id,
      correct:      a.correct,
      selectedText: a.selectedText
    })) : null
  } : null;

  await storage.updateStats(currentUser.id, gameState.questions.length, gameState.score, bd.total, dailyUpdate, buildCatStats(gameState.answers));
  addSeenIds(currentUser.id, gameState.questions.map(q => q.id));

  const users = await storage.getUsers();
  currentUser = users.find(u => u.id === currentUser.id) || currentUser;
  renderResults();
}

function renderResults() {
  showScreen('screen-results');
  sounds.fanfare();

  const total      = gameState.questions.length;
  const score      = gameState.score;
  const percentage = Math.round((score / total) * 100);

  let emoji, title;
  if (percentage === 100)      { emoji = '🏰'; title = 'Perfect Score!'; }
  else if (percentage >= 80)   { emoji = '✨'; title = 'Enchanting!'; }
  else if (percentage >= 60)   { emoji = '🐭'; title = 'Well Done!'; }
  else if (percentage >= 40)   { emoji = '📚'; title = 'Keep Practicing!'; }
  else                         { emoji = '🪄'; title = 'Keep Trying!'; }

  document.getElementById('results-emoji').textContent    = emoji;
  document.getElementById('results-title').textContent    = title;
  document.getElementById('results-fraction').textContent = `${score} out of ${total} correct`;
  document.getElementById('results-pct').textContent      = percentage + '%';

  // Points breakdown
  const bd   = gameState.scoreBreakdown;
  const ptEl = document.getElementById('results-points-display');
  if (bd) {
    const lines = [];
    if (bd.base > 0)         lines.push(`Base: ${bd.base.toLocaleString()}`);
    if (bd.streakBonus > 0)  lines.push(`🔥 Streak: +${bd.streakBonus.toLocaleString()}`);
    if (bd.perfectBonus > 0) lines.push(`⭐ Perfect: +${bd.perfectBonus.toLocaleString()}`);
    if (bd.dailyBonus > 0)   lines.push(`📅 Daily: +${bd.dailyBonus.toLocaleString()}`);
    ptEl.innerHTML = `<div class="pts-total">+${bd.total.toLocaleString()} pts</div>` +
      (lines.length > 1 ? `<div class="pts-breakdown">${lines.join(' · ')}</div>` : '');
  } else {
    ptEl.innerHTML = '';
  }

  // Category breakdown
  const breakdown = {};
  gameState.answers.forEach(a => {
    const c = a.question.category;
    if (!breakdown[c]) breakdown[c] = { correct: 0, total: 0 };
    breakdown[c].total++;
    if (a.correct) breakdown[c].correct++;
  });

  const breakdownEl = document.getElementById('results-breakdown');
  breakdownEl.innerHTML = '';
  Object.entries(breakdown).forEach(([cat, data]) => {
    const row = document.createElement('div');
    row.className = 'breakdown-row';
    row.innerHTML = `
      <span class="breakdown-cat">${catLabel(cat)}</span>
      <span class="breakdown-score">${data.correct}/${data.total} (${Math.round(data.correct / data.total * 100)}%)</span>
    `;
    breakdownEl.appendChild(row);
  });

  // Rematch / review daily
  document.getElementById('btn-rematch').classList.toggle('hidden', gameState.isDaily);
  document.getElementById('btn-review-daily').classList.toggle('hidden', !gameState.isDaily);

  // Missed questions
  const missed    = gameState.answers.filter(a => !a.correct);
  const missedSec = document.getElementById('missed-section');
  const reviewBtn = document.getElementById('btn-review-missed');
  const missedList = document.getElementById('missed-list');

  if (missed.length === 0) {
    missedSec.classList.add('hidden');
  } else {
    missedSec.classList.remove('hidden');
    reviewBtn.textContent = `Review ${missed.length} Missed Question${missed.length !== 1 ? 's' : ''}`;
    missedList.classList.add('hidden');
    missedList.innerHTML = '';
    missed.forEach(a => {
      const item = document.createElement('div');
      item.className = 'missed-item';
      item.innerHTML = `
        <div class="missed-q">${a.question.question}</div>
        <div class="missed-ca">✓ ${a.question.answers[0]}</div>
        <div class="missed-ua">✗ You said: ${a.selectedText}</div>
      `;
      missedList.appendChild(item);
    });
  }
}

document.getElementById('btn-review-missed').addEventListener('click', () => {
  const list   = document.getElementById('missed-list');
  const btn    = document.getElementById('btn-review-missed');
  const hidden = list.classList.toggle('hidden');
  const count  = gameState.answers.filter(a => !a.correct).length;
  btn.textContent = hidden
    ? `Review ${count} Missed Question${count !== 1 ? 's' : ''}`
    : 'Hide Missed Questions';
});

document.getElementById('btn-review-daily').addEventListener('click', () => renderDailyReview('results', 0));
document.getElementById('btn-view-yesterday').addEventListener('click', () => renderDailyReview('home', 1));
document.getElementById('btn-daily-review-back').addEventListener('click', () => {
  if (_dailyReviewBack === 'results') renderResults();
  else if (_dailyReviewBack === 'home') renderHome();
  else renderSettings();
});

let _dailyReviewBack = 'settings';

// backTarget: 'results' | 'settings' | 'home'
// daysAgo: 0 = today, 1 = yesterday
async function renderDailyReview(backTarget = 'settings', daysAgo = 0) {
  _dailyReviewBack = backTarget;
  showScreen('screen-daily-review');
  document.getElementById('daily-review-title').textContent =
    daysAgo === 0 ? '📅 Today\'s Review' : '📅 Yesterday\'s Review';

  const targetDate = dayKey(daysAgo);
  const list = document.getElementById('daily-review-list');
  list.innerHTML = '<p class="dr-loading">Loading…</p>';

  let users;
  try {
    users = await storage.getUsers();
  } catch(e) {
    list.innerHTML = `<p class="load-error">Couldn't load player data.<br><a href="" onclick="location.reload()">Tap to retry</a></p>`;
    return;
  }

  const getUserAnswers = u => {
    if (u.lastDailyDate === targetDate && u.lastDailyAnswers) return u.lastDailyAnswers;
    if (u.prevDailyDate === targetDate && u.prevDailyAnswers) return u.prevDailyAnswers;
    return null;
  };

  const qMap = new Map(QUESTIONS.map(q => [q.id, q]));

  // 1. Canonical pinned list — written by the first player who played that day.
  //    Immune to any pool changes before or after play.
  let questions = null;
  try {
    const pinnedIds = await storage.getDailyPins(targetDate);
    if (pinnedIds && pinnedIds.length > 0) {
      const qs = pinnedIds.map(id => qMap.get(id)).filter(Boolean);
      if (qs.length > 0) questions = qs;
    }
  } catch(e) {}

  // 2. Stored answer questionIds — stable for the player who has them, may
  //    differ from other players if the pool changed during that day.
  if (!questions) {
    const currentUserFresh = users.find(u => u.id === currentUser?.id);
    const orderedSources = [
      ...(currentUserFresh ? [currentUserFresh] : []),
      ...users.filter(u => u.id !== currentUser?.id)
    ];
    for (const u of orderedSources) {
      const ans = getUserAnswers(u);
      if (ans && ans.length > 0) {
        const qs = ans.map(a => qMap.get(a.questionId)).filter(Boolean);
        if (qs.length > 0) { questions = qs; break; }
      }
    }
  }

  // 3. Last resort: regenerate from live pool.
  if (!questions) questions = getDailyQuestions(10, daysAgo);

  // Classify players for the footer of each question card.
  // "played — details unavailable": lastDailyDate matches but no stored answers.
  const hasPlayedDate = u => u.lastDailyDate === targetDate || u.prevDailyDate === targetDate;
  const playedNoDetailUsers = users.filter(u => !getUserAnswers(u) && hasPlayedDate(u));
  const notPlayedUsers      = users.filter(u => !getUserAnswers(u) && !hasPlayedDate(u));

  list.innerHTML = '';
  const letters = ['A', 'B', 'C', 'D'];
  questions.forEach((q, idx) => {
    const item = document.createElement('div');
    item.className = 'dr-item';

    // Shuffle answer order consistently per question so correct isn't always first
    const answerOrder = seededShuffle([0, 1, 2, 3], q.id);

    let choicesHtml = '';
    answerOrder.forEach((origIdx, displayPos) => {
      const text      = q.answers[origIdx];
      const isCorrect = origIdx === 0;

      // Which players chose this answer?
      const choosers = [];
      users.forEach(u => {
        const uAnswers = getUserAnswers(u);
        if (!uAnswers) return;
        const ans = uAnswers.find(a => a.questionId === q.id);
        if (ans && ans.selectedText === text) choosers.push({ user: u, correct: ans.correct });
      });

      const cls = 'dr-choice' + (isCorrect ? ' dr-choice-correct' : choosers.length ? ' dr-choice-wrong-picked' : '');

      const chipsHtml = choosers.length
        ? `<div class="dr-chips">${choosers.map(c =>
            `<span class="dr-chip ${c.correct ? 'dr-chip-correct' : 'dr-chip-wrong'}">${disneyAvatar(c.user.name)} ${c.user.name} ${c.correct ? '✓' : '✗'}</span>`
          ).join('')}</div>`
        : '';

      choicesHtml += `<div class="${cls}">
        <span class="dr-choice-letter">${letters[displayPos]}</span>
        <div class="dr-choice-body">
          <span class="dr-choice-text">${text}${isCorrect ? ' <span class="dr-tick">✓</span>' : ''}</span>
          ${chipsHtml}
        </div>
      </div>`;
    });

    const footerHtml = [
      ...playedNoDetailUsers.map(u =>
        `<div class="dr-player-ans dr-not-played">${disneyAvatar(u.name)} ${u.name}: played — details unavailable</div>`),
      ...notPlayedUsers.map(u =>
        `<div class="dr-player-ans dr-not-played">${disneyAvatar(u.name)} ${u.name}: —</div>`)
    ].join('');

    item.innerHTML = `
      <div class="dr-header">
        <span class="dr-qnum">Q${idx + 1}</span>
        <span class="dr-cat">${catLabel(q.category)}</span>
      </div>
      <div class="dr-question">${q.question}</div>
      <div class="dr-choices">${choicesHtml}</div>
      ${footerHtml ? `<div class="dr-players">${footerHtml}</div>` : ''}
    `;
    list.appendChild(item);
  });
}

document.getElementById('btn-rematch').addEventListener('click', () => {
  if (gameState.isDaily) return;
  {
    const pool  = filteredPool();
    const count = Math.min(gameSettings.questionCount, pool.length);
    const seen  = new Set(getSeenIds(currentUser.id));
    const fresh = pool.filter(q => !seen.has(q.id));
    const src   = fresh.length >= count ? fresh : pool;
    gameState = { questions: shuffle(src).slice(0, count), currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: false, pointsEarned: 0, scoreBreakdown: null };
  }
  renderGameQuestion();
});

document.getElementById('btn-play-again').addEventListener('click', renderSettings);
document.getElementById('btn-results-home').addEventListener('click', renderHome);

// =============================================================================
// Boot
// =============================================================================
async function loadQuestions() {
  const manifest = await fetch('questions/manifest.json', { cache: 'no-cache' }).then(r => r.json());
  const shards = await Promise.all(manifest.shards.map(s => fetch(s, { cache: 'no-cache' }).then(r => r.json())));
  QUESTIONS = shards.flat();
}

async function loadMovies() {
  const data = await fetch('movies.json', { cache: 'no-cache' }).then(r => r.json());
  MOVIES = data.movies;
}

async function init() {
  try {
    await loadQuestions();
  } catch (e) {
    document.getElementById('app').innerHTML =
      `<p style="padding:2rem;color:var(--red)">Failed to load questions: ${e.message}.<br><a href="" onclick="location.reload()">Tap to retry</a></p>`;
    return;
  }
  // Weekly Homework is a bonus feature — never let it block the trivia app from loading.
  try {
    await loadMovies();
    await rollHomeworkIfStale();
  } catch (e) {
    MOVIES = [];
    homeworkState = null;
  }
  renderHome();
}
init();
