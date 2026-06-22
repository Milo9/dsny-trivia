const APP_VERSION = '1.6';

// =============================================================================
// State
// =============================================================================
let QUESTIONS     = [];
let currentUser   = null;
let gameSettings  = { difficulty: 'all', categories: ['movies','characters','parks','walt','cruise','music','pixar'], questionCount: 10 };
let gameState     = { questions: [], currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: false };
let shuffledOpts  = [];   // [{text, originalIndex}] for current question display

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

// --- Daily challenge helpers ---

function todayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

// Returns number of calendar days between two "YYYY-MM-DD" keys (today - prev).
// Returns Infinity if prev is falsy (never played).
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

// Returns the same 10 questions for all players on a given calendar day.
// Stable-sorts by id first so shard/load order doesn't affect the result.
function getDailyQuestions(count = 10) {
  const sorted = [...QUESTIONS].sort((a, b) => a.id - b.id);
  return seededShuffle(sorted, dateToSeed(todayKey())).slice(0, count);
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

  // Reset add-user form state
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

  users.forEach(user => {
    const card = document.createElement('div');
    card.className = 'user-card';
    const streak     = user.dailyStreak || 0;
    const streakText = streak > 0 ? ` · 🔥 ${streak}` : '';
    const stat = user.totalAnswered
      ? `${user.totalAnswered} questions · ${pct(user.totalCorrect, user.totalAnswered)} correct${streakText}`
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

    // Auto-highlight last player (subtle — just border tint)
    if (user.id === lastId) card.style.borderColor = 'var(--primary)';
  });
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
  await storage.saveUser({ id: slugId(name), name, totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0 });
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
    const entry = document.createElement('div');
    entry.className = `lb-entry${i < 3 ? ' rank-' + (i + 1) : ''}`;
    const percentage = u.totalAnswered ? Math.round((u.totalCorrect / u.totalAnswered) * 100) : null;
    const detail = u.totalAnswered
      ? `${u.totalAnswered} q · ${u.gamesPlayed} game${u.gamesPlayed !== 1 ? 's' : ''}`
      : 'No games yet';
    entry.innerHTML = `
      <div class="lb-rank">${medals[i] || (i + 1)}</div>
      <div class="lb-avatar">${disneyAvatar(u.name)}</div>
      <div class="lb-info">
        <div class="lb-name">${u.name}</div>
        <div class="lb-detail">${detail}</div>
      </div>
      <div class="lb-pct">${percentage !== null ? percentage + '%' : '—'}</div>
    `;
    list.appendChild(entry);
  });
}

// =============================================================================
// SETTINGS SCREEN
// =============================================================================
function renderSettings() {
  showScreen('screen-settings');
  document.getElementById('settings-user-name').textContent = currentUser.name;
  updateAvailableHint();

  // Daily challenge card
  const today   = todayKey();
  const streak  = currentUser.dailyStreak || 0;
  const played  = currentUser.lastDailyDate === today;
  const statusEl = document.getElementById('daily-status');
  const btn      = document.getElementById('btn-daily-challenge');

  if (played) {
    statusEl.textContent = `✓ Played today · 🔥 ${streak} day streak`;
    statusEl.className   = 'daily-status daily-done';
    btn.textContent      = '⭐ Daily Challenge (Replay)';
  } else if (streak > 0) {
    statusEl.textContent = `🔥 ${streak} day streak — keep it going!`;
    statusEl.className   = 'daily-status daily-active';
    btn.textContent      = '⭐ Daily Challenge';
  } else {
    statusEl.textContent = 'Same 10 questions for everyone today. Start your streak!';
    statusEl.className   = 'daily-status';
    btn.textContent      = '⭐ Daily Challenge';
  }
}

document.getElementById('btn-settings-back').addEventListener('click', renderHome);

document.getElementById('btn-daily-challenge').addEventListener('click', () => {
  gameState = { questions: getDailyQuestions(10), currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: true };
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

  gameState = { questions: shuffle(src).slice(0, count), currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: false };
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

  // Shuffle answer positions
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

  // Sync streak banner
  const banner = document.getElementById('streak-banner');
  if (gameState.currentStreak >= 2) {
    document.getElementById('streak-count').textContent = gameState.currentStreak;
    banner.classList.remove('hidden');
  } else {
    banner.classList.add('hidden');
  }

  // Sync mute button
  const muteBtn = document.getElementById('btn-mute-sound');
  muteBtn.textContent = sounds.muted ? '🔇' : '🔊';
  muteBtn.classList.toggle('muted', sounds.muted);

  // Reset feedback area
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

  // Update streak banner
  const banner = document.getElementById('streak-banner');
  if (gameState.currentStreak >= 2) {
    document.getElementById('streak-count').textContent = gameState.currentStreak;
    banner.classList.remove('hidden');
    // Re-trigger pop animation
    banner.style.animation = 'none';
    banner.offsetHeight; // force reflow
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
      await storage.updateStats(currentUser.id, answered, gameState.score);
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
  await storage.updateStats(currentUser.id, gameState.questions.length, gameState.score);

  // Daily challenge streak update (idempotent — only increments once per calendar day)
  if (gameState.isDaily) {
    const today = todayKey();
    if (currentUser.lastDailyDate !== today) {
      const diff      = computeDaysDiff(currentUser.lastDailyDate, today);
      const newStreak = diff === 1 ? (currentUser.dailyStreak || 0) + 1 : 1;
      try {
        await storage.updateDailyStreak(currentUser.id, newStreak, today);
      } catch(e) {}
    }
  }

  addSeenIds(currentUser.id, gameState.questions.map(q => q.id));
  // Refresh user data
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

  // Missed questions
  const missed      = gameState.answers.filter(a => !a.correct);
  const missedSec   = document.getElementById('missed-section');
  const reviewBtn   = document.getElementById('btn-review-missed');
  const missedList  = document.getElementById('missed-list');

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

document.getElementById('btn-rematch').addEventListener('click', () => {
  if (gameState.isDaily) {
    gameState = { questions: getDailyQuestions(10), currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: true };
  } else {
    const pool  = filteredPool();
    const count = Math.min(gameSettings.questionCount, pool.length);
    const seen  = new Set(getSeenIds(currentUser.id));
    const fresh = pool.filter(q => !seen.has(q.id));
    const src   = fresh.length >= count ? fresh : pool;
    gameState = { questions: shuffle(src).slice(0, count), currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: false };
  }
  renderGameQuestion();
});

document.getElementById('btn-play-again').addEventListener('click', renderSettings);
document.getElementById('btn-results-home').addEventListener('click', renderHome);

// =============================================================================
// Boot
// =============================================================================
async function loadQuestions() {
  const manifest = await fetch('questions/manifest.json').then(r => r.json());
  const shards = await Promise.all(manifest.shards.map(s => fetch(s).then(r => r.json())));
  QUESTIONS = shards.flat();
}

async function init() {
  try {
    await loadQuestions();
  } catch (e) {
    document.getElementById('app').innerHTML =
      `<p style="padding:2rem;color:var(--red)">Failed to load questions: ${e.message}.<br><a href="" onclick="location.reload()">Tap to retry</a></p>`;
    return;
  }
  renderHome();
}
init();
