const APP_VERSION = '1.36';

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
// Pure rules (shuffle, dates, scoring, daily selection, checkpoint reconcile)
// live in game-logic.js, loaded before this file and unit-tested by
// test/game-logic.test.js. This file only adds DOM, storage, and globals.

function getSeenIds(userId) {
  try { return JSON.parse(localStorage.getItem('disney_seen_' + userId)) || []; }
  catch { return []; }
}

// Pure — computes the next capped seen-ids list without writing anything, so
// callers can pass it to storage.updateStats() first and only persist locally
// once that save actually succeeds (mirrors the existing "don't mark seen on
// a failed/offline save" behavior).
function computeSeenIds(userId, newIds) {
  return capSeenIds(getSeenIds(userId), newIds);
}

function saveSeenIds(userId, seen) {
  localStorage.setItem('disney_seen_' + userId, JSON.stringify(seen));
}

// How far back to exclude past daily-challenge pins when generating a new
// day's pick. A rolling window, not all-time: with a ~2,050-question corpus
// and 10 exclusions added/day, permanent history would exhaust the corpus in
// ~205 days and then silently fall back to zero exclusion every day after
// (see getDailyQuestions' fresh/src fallback) — 180 days keeps ~1,800 IDs
// excluded at steady state, safely under the corpus size, while still being
// far longer than anyone will remember a specific daily's questions.
const DAILY_HISTORY_DAYS = 180;

// Exclusion set for generating a brand new day's daily-challenge pin: the
// union of (a) every player's recently-seen question IDs (synced to each
// user's Firestore doc as `recentQuestionIds`), so it doesn't repeat
// something any player, in any mode, on any device, *just* played, and
// (b) every question ID pinned as a daily challenge in the last
// DAILY_HISTORY_DAYS days (`dailies/*`), regardless of whether anyone
// actually played that day. (b) exists because (a) alone has two gaps: a
// pinned daily nobody ever finishes/exits never marks its questions seen
// anywhere, and (a) is capped at SEEN_MAX per user — heavy regular-game play
// can push a genuinely-recent daily question out of that window well before
// it should be eligible to repeat as a daily. Each source fails open
// (silently contributes nothing) on its own read error — daily generation
// must never be blocked by this.
async function dailyExclusionSet() {
  const ids = new Set();
  try {
    const users = await storage.getUsers();
    users.forEach(u => (u.recentQuestionIds || []).forEach(id => ids.add(id)));
  } catch (e) {}
  try {
    const pastDaily = await storage.getAllDailyQuestionIds(dayKey(DAILY_HISTORY_DAYS));
    pastDaily.forEach(id => ids.add(id));
  } catch (e) {}
  return ids;
}

// --- Daily challenge in-progress state (per-device, per-user) ---
// Lets a player exit mid-daily and resume later without losing or re-answering
// already-locked-in questions. Cleared only once that day's daily is actually
// completed and saved (see endGame). Not synced to Firestore — resuming on a
// different device just starts fresh, same as this app's other local-only state.
function dailyProgressKey(userId) { return 'disney_daily_progress_' + userId; }

function getDailyProgress(userId) {
  try { return JSON.parse(localStorage.getItem(dailyProgressKey(userId))); }
  catch { return null; }
}

function saveDailyProgress(userId, dateKey, answers) {
  localStorage.setItem(dailyProgressKey(userId), JSON.stringify({ dateKey, answers }));
}

function clearDailyProgress(userId) {
  localStorage.removeItem(dailyProgressKey(userId));
}

// --- Regular game checkpoint (per-device, per-user) ---
// Written after every answer so a game survives the app being killed, a
// reload, or the update toast's "Update now". Cleared once the game's answers
// are committed to Firestore (endGame or an Exit); kept on a failed save so
// they can be committed later. See offerGameResume().
function gameCheckpointKey(userId) { return 'disney_game_progress_' + userId; }

function getGameCheckpoint(userId) {
  try { return JSON.parse(localStorage.getItem(gameCheckpointKey(userId))); }
  catch { return null; }
}

function clearGameCheckpoint(userId) {
  try { localStorage.removeItem(gameCheckpointKey(userId)); } catch (e) {}
}

// Checkpoints the active game. Called from handleAnswer() right after the
// answer is recorded — not on Next — since the correct answer is revealed on
// tap, and saving later would let a killed app re-answer a revealed question.
function checkpointGame() {
  if (!currentUser || gameState.answers.length === 0) return;
  try {
    if (gameState.isDaily) {
      saveDailyProgress(currentUser.id, gameState.dateKey || todayKey(), serializeAnswers(gameState.answers));
    } else {
      localStorage.setItem(gameCheckpointKey(currentUser.id), JSON.stringify({
        questionIds: gameState.questions.map(q => q.id),
        answers:     serializeAnswers(gameState.answers),
        savedAt:     new Date().toISOString()
      }));
    }
  } catch (e) {
    // storage full / blocked — the game still plays, it just can't be resumed
  }
}

// Commits a regular game's answers to stats — the shared path for finishing,
// exiting, and settling a leftover checkpoint. Perfect bonus only if complete.
async function commitRegularAnswers(answers, complete) {
  const pts     = scoreBreakdown(answers, false, 0, complete).total;
  const newSeen = computeSeenIds(currentUser.id, answers.map(a => a.question.id));
  await storage.updateStats(currentUser.id, answers.length, answers.filter(a => a.correct).length, pts, null, buildCatStats(answers), newSeen, monthKey());
  saveSeenIds(currentUser.id, newSeen);
}

// If this player has a leftover regular-game checkpoint, offers to resume it
// (or, if every question was answered but the save failed, to save it).
//   mode 'select' — on picking a player. "Not now" and dismiss both leave the
//                   checkpoint for later.
//   mode 'start'  — about to start a different game. Cancel ("Start new")
//                   commits the leftover answers first so they're never
//                   silently dropped; dismiss aborts the new game.
// Returns 'resumed' | 'proceed' | 'abort'.
async function offerGameResume(mode) {
  const cp = getGameCheckpoint(currentUser.id);
  if (!cp) return 'proceed';
  const gs = reconcileRegularCheckpoint(cp, new Map(QUESTIONS.map(q => [q.id, q])));
  if (!gs || gs.answers.length === 0) { clearGameCheckpoint(currentUser.id); return 'proceed'; }

  const n = gs.answers.length, total = gs.questions.length, complete = n >= total;
  const choice = await showConfirm({
    title:       complete ? 'Unsaved game' : 'Resume your game?',
    message:     complete
      ? `Your last ${total}-question game didn't get saved. Save it to your stats now?`
      : `You were ${n} of ${total} questions into a game. Pick up where you left off?`,
    confirmText: complete ? 'Save it' : 'Resume',
    cancelText:  mode === 'start' ? (complete ? 'Save & start new' : 'Start new') : 'Not now'
  });

  if (choice === true) {
    gameState = gs;
    if (complete) endGame(); else renderGameQuestion();
    return 'resumed';
  }
  if (mode === 'select' || choice === null) return mode === 'select' ? 'proceed' : 'abort';

  // mode 'start' + explicit cancel: commit the leftover answers, then go on.
  try {
    await commitRegularAnswers(gs.answers, complete);
    clearGameCheckpoint(currentUser.id);
    return 'proceed';
  } catch (e) {
    await showAlert("Couldn't save", "Your unfinished game couldn't be saved — check your connection. It's still kept on this device.");
    return 'abort';
  }
}

// Rebuilds gameState for the daily challenge, resuming from saved progress
// (see reconcileDailyProgress in game-logic.js for the matching rules).
function buildDailyGameState(questions, today) {
  return reconcileDailyProgress(questions, getDailyProgress(currentUser.id), today);
}

function pct(correct, total) {
  return total ? Math.round((correct / total) * 100) + '%' : '—';
}

// Escapes user-entered text (player names) before innerHTML interpolation.
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

const DISNEY_AVATARS = ['🐭','👸','🦁','🤠','🐠','❄️','🧚','🧞'];

function disneyAvatar(name) {
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffff;
  return DISNEY_AVATARS[h % DISNEY_AVATARS.length];
}

function streakStars(streak) {
  const filled = Math.min(streak, 5);
  const empty  = 5 - filled;
  return `<span class="stars-filled">${'★'.repeat(filled)}</span><span class="stars-empty">${'☆'.repeat(empty)}</span>`;
}

function slugId(name) {
  return name.toLowerCase().replace(/\s+/g, '_') + '_' + Date.now();
}

const CAT_LABELS = {
  movies: '🎬 Movies', characters: '🐭 Characters', parks: '🏰 Disney Parks',
  walt: '🎩 Walt Disney', cruise: '⛴️ Cruise Line', music: '🎵 Music & Songs', pixar: '💡 Pixar'
};

function catLabel(c) { return CAT_LABELS[c] || c; }

// Thin wrappers binding game-logic.js's pure functions to app globals.
function pickFromMoviePool(excludeIds) { return pickMovie(MOVIES, excludeIds); }

// excludeIds only matters for a brand-new day's pin generation (see the
// btn-daily-challenge handler) — the review screen's regenerate-from-live-pool
// fallback deliberately calls this with no excludeIds, since "what's recently
// seen right now" has no meaning when reconstructing a past day.
function getDailyQuestions(count = 10, daysAgo = 0, excludeIds = new Set()) {
  return pickDailyQuestions(QUESTIONS, dayKey(daysAgo), count, excludeIds);
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

  // Frequency sweep — used for the wrong-answer slide-whistle-down. exponentialRamp
  // needs both endpoints > 0, which a musical pitch always satisfies.
  function slide(freqStart, freqEnd, start, dur, type = 'sine', vol = 0.28) {
    try {
      const c   = getCtx();
      const osc = c.createOscillator();
      const g   = c.createGain();
      osc.connect(g); g.connect(c.destination);
      osc.type = type;
      const t0 = c.currentTime + start;
      osc.frequency.setValueAtTime(freqStart, t0);
      osc.frequency.exponentialRampToValueAtTime(freqEnd, t0 + dur);
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
      slide(520, 140, 0, 0.32, 'triangle', 0.2); // comedic slide-whistle-down
    },
    fanfare() {
      if (_muted) return;
      // "When you wish upon a star" — Leigh Harline's opening phrase (Pinocchio,
      // 1940), transcribed from a beginner letter-note sheet (noobnotes.net) so the
      // synthesized fanfare is actually recognizable instead of a generic arpeggio.
      // One note corrected from that source: "wish" is the leading tone (C#), not
      // the natural C a beginner sheet would simplify to for playability.
      [
        [293.66, 0],     // D4   When
        [587.33, 0.18],  // D5   you
        [554.37, 0.36],  // C#5  wish  (leading tone — do-do'-ti; a beginner
                         //             sheet's un-sharped "C" reads flat-7 here)
        [493.88, 0.54],  // B4   up-
        [415.30, 0.70],  // G#4  on
        [440.00, 0.86],  // A4   a
        [659.25, 1.04]   // E5   star
      ].forEach(([f, t]) => tone(f, t, 0.22));
    }
  };
})();

// =============================================================================
// Pixie-dust sparkle burst — fired from the tapped answer button on a correct
// answer. Appended to document.body with fixed coords from getBoundingClientRect()
// (not appended inside the button) so ancestor transforms/overflow can't clip it.
// Skipped entirely under prefers-reduced-motion rather than relying on the global
// animation-duration override, since that would still churn the DOM for nothing.
function spawnSparkles(originEl) {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const rect  = originEl.getBoundingClientRect();
  const cx    = rect.left + rect.width / 2;
  const cy    = rect.top + rect.height / 2;
  const count = 7;
  for (let i = 0; i < count; i++) {
    const spark = document.createElement('span');
    spark.className   = 'pixie-spark';
    spark.textContent = i % 2 === 0 ? '✦' : '✧';
    const angle = (Math.PI * 2 * i) / count + (Math.random() * 0.6 - 0.3);
    const dist  = 40 + Math.random() * 30;
    spark.style.left = cx + 'px';
    spark.style.top  = cy + 'px';
    spark.style.setProperty('--dx', (Math.cos(angle) * dist) + 'px');
    spark.style.setProperty('--dy', (Math.sin(angle) * dist) + 'px');
    spark.addEventListener('animationend', () => spark.remove());
    document.body.appendChild(spark);
  }
}

// =============================================================================
// Screen navigation
// =============================================================================
// Moves focus to the new screen's heading (or the screen itself, if it has
// none) so screen-reader/keyboard users get an announcement of where they
// landed instead of focus silently staying on a now-hidden button.
let _currentScreen = 'screen-home';

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  _currentScreen = id;
  syncHistory(id);
  window.scrollTo(0, 0);
  const target = el.querySelector('h1, h2') || el;
  if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
  target.focus({ preventScroll: true });
  if (id !== 'screen-game') maybeShowUpdateToast();
}

// =============================================================================
// BACK BUTTON (browser history)
// =============================================================================
// Ported from Offline Trivia. Browser history holds at most two entries for
// this app — home (depth 0) and whichever other screen is showing (depth 1;
// moving between non-home screens replaces it). So the phone's Back button
// means "this screen's own Back" instead of closing the installed app, and
// mid-game it opens the same exit confirm as the Exit button. Route every
// screen change through showScreen(); don't push history entries elsewhere.
// No unconditional replaceState at boot: a reload ("Update now", "Tap to
// retry") from a depth-1 screen keeps that entry, and renderHome()'s
// syncHistory collapses it.
let _ignoreNextPop = false;

function historyDepth() {
  return history.state && typeof history.state.depth === 'number' ? history.state.depth : 0;
}

function syncHistory(id) {
  try {
    if (id === 'screen-home') {
      if (historyDepth() > 0) {
        _ignoreNextPop = true; // the popstate this back() triggers isn't a user Back press
        history.back();
      }
    } else if (historyDepth() > 0) {
      history.replaceState({ depth: 1, screen: id }, '');
    } else {
      history.pushState({ depth: 1, screen: id }, '');
    }
  } catch (e) {
    // history API unavailable — Back just won't be intercepted
  }
}

window.addEventListener('popstate', () => {
  if (_ignoreNextPop) { _ignoreNextPop = false; return; }
  if (_confirmState) {
    // Back while a confirm sheet is open just dismisses it; re-push the entry
    // the Back press consumed so the app stays on this screen.
    history.pushState({ depth: 1, screen: _currentScreen }, '');
    _confirmState.close(null);
    return;
  }
  if (historyDepth() > 0) {
    // Forward navigation onto our depth-1 entry — nothing to restore.
    _ignoreNextPop = true;
    history.back();
    return;
  }
  if (_currentScreen === 'screen-home') return;
  // Re-push first so a cancelled confirm (or a non-home target) leaves the app
  // on a depth-1 entry; going home collapses it again via syncHistory.
  history.pushState({ depth: 1, screen: _currentScreen }, '');
  if (_currentScreen === 'screen-game') { exitGameFlow(); return; }
  const backBtn = document.querySelector(`#${_currentScreen} .btn-back`);
  if (backBtn) backBtn.click();
  else renderHome();
});

// =============================================================================
// CONFIRM SHEET
// =============================================================================
// In-theme replacement for confirm()/alert(). Resolves true (confirm button),
// false (cancel button), or null (dismissed: Escape, tapping the backdrop, or
// the phone's Back button) — callers that need "decide later" treat null
// differently from an explicit cancel. Behaves like a real modal: #app goes
// inert, focus moves in and back out, Tab cycles between the two buttons.
// single: true hides the cancel button (alert-style).
let _confirmState = null;

function showConfirm({ title, message, confirmText = 'OK', cancelText = 'Cancel', danger = false, single = false }) {
  if (_confirmState) return Promise.resolve(null); // never stack two sheets (double-tap, Back while open)
  const overlay = document.getElementById('confirm-overlay');
  const okBtn   = document.getElementById('confirm-ok');
  const noBtn   = document.getElementById('confirm-cancel');
  const app     = document.getElementById('app');
  const previouslyFocused = document.activeElement;

  document.getElementById('confirm-title').textContent   = title;
  document.getElementById('confirm-message').textContent = message;
  okBtn.textContent = confirmText;
  noBtn.textContent = cancelText;
  overlay.querySelector('.confirm-sheet').classList.toggle('danger', danger);
  overlay.querySelector('.confirm-actions').classList.toggle('single', single);

  return new Promise(resolve => {
    function onKeyDown(e) {
      if (e.key === 'Escape') { e.preventDefault(); close(null); }
      else if (e.key === 'Tab' && !single) {
        e.preventDefault();
        (document.activeElement === noBtn ? okBtn : noBtn).focus();
      } else if (e.key === 'Tab') {
        e.preventDefault();
      }
    }
    const onOk  = () => close(true);
    const onNo  = () => close(false);
    const onBackdrop = e => { if (e.target === overlay) close(null); };
    function close(result) {
      overlay.classList.add('hidden');
      app.inert = false;
      okBtn.removeEventListener('click', onOk);
      noBtn.removeEventListener('click', onNo);
      overlay.removeEventListener('click', onBackdrop);
      document.removeEventListener('keydown', onKeyDown, true);
      _confirmState = null;
      if (previouslyFocused && document.contains(previouslyFocused) && typeof previouslyFocused.focus === 'function') {
        previouslyFocused.focus({ preventScroll: true });
      }
      resolve(result);
    }
    _confirmState = { close };
    okBtn.addEventListener('click', onOk);
    noBtn.addEventListener('click', onNo);
    overlay.addEventListener('click', onBackdrop);
    document.addEventListener('keydown', onKeyDown, true);
    overlay.classList.remove('hidden');
    app.inert = true;
    // Cancel is the safe default focus for two-button sheets.
    (single ? okBtn : noBtn).focus();
  });
}

function showAlert(title, message) {
  return showConfirm({ title, message, confirmText: 'OK', single: true });
}

// =============================================================================
// UPDATE-AVAILABLE TOAST
// =============================================================================
// No service worker here (see PWA notes in CLAUDE.md), so "is there a new
// build?" is answered by re-fetching index.html and comparing its app.js?v=
// against the one this page actually loaded with. Comparing the same string
// from the same file (not APP_VERSION) means a forgotten bump in one place
// can't produce a toast that never goes away.
const UPDATE_CHECK_MIN_GAP_MS = 60 * 1000;
const UPDATE_CHECK_INTERVAL_MS = 20 * 60 * 1000;
let _lastUpdateCheck = 0;
let _pendingUpdateVersion = null;

function loadedAppVersion() {
  const s = document.querySelector('script[src*="app.js"]');
  const m = s && s.getAttribute('src').match(/app\.js\?v=([^"'&]+)/);
  return m ? m[1] : null;
}

async function checkForUpdate() {
  if (Date.now() - _lastUpdateCheck < UPDATE_CHECK_MIN_GAP_MS) return;
  _lastUpdateCheck = Date.now();
  const current = loadedAppVersion();
  if (!current) return;
  try {
    // The ?t= buster gets past GitHub Pages' ~10 min CDN max-age; no-store only bypasses the browser cache.
    const res = await fetchWithTimeout('index.html?t=' + Date.now(), { cache: 'no-store' });
    if (!res.ok) return;
    const m = (await res.text()).match(/app\.js\?v=([^"'&]+)/);
    if (m && m[1] !== current) {
      _pendingUpdateVersion = m[1];
      maybeShowUpdateToast();
    }
  } catch (e) {
    // Offline / flaky wifi — silently try again next time.
  }
}

// Never shown mid-game: a reload there loses a regular game outright, and a
// daily's in-flight answers are only saved via the Exit path. The pending
// version is surfaced by showScreen() once the player lands anywhere else.
function maybeShowUpdateToast() {
  if (!_pendingUpdateVersion) return;
  if (!document.getElementById('screen-game').classList.contains('hidden')) return;
  let dismissed = null;
  try { dismissed = sessionStorage.getItem('disney_update_dismissed'); } catch (e) {}
  if (dismissed === _pendingUpdateVersion) return;
  document.getElementById('update-toast').classList.remove('hidden');
}

document.getElementById('btn-update-reload').addEventListener('click', () => location.reload());
document.getElementById('btn-update-dismiss').addEventListener('click', () => {
  try { sessionStorage.setItem('disney_update_dismissed', _pendingUpdateVersion); } catch (e) {}
  document.getElementById('update-toast').classList.add('hidden');
});
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') checkForUpdate();
});
setInterval(() => {
  if (document.visibilityState === 'visible') checkForUpdate();
}, UPDATE_CHECK_INTERVAL_MS);

// =============================================================================
// HOME SCREEN
// =============================================================================
async function renderHome() {
  showScreen('screen-home');
  document.getElementById('app-version').textContent = 'v' + APP_VERSION;

  document.getElementById('add-user-form').classList.add('hidden');
  document.getElementById('btn-show-add-user').classList.remove('hidden');
  document.getElementById('new-user-input').value = '';
  document.getElementById('add-user-error').classList.add('hidden');

  const list = document.getElementById('user-list');
  list.innerHTML = '<p class="load-status">Loading players…</p>';

  let users;
  try {
    users = await storage.getUsers();
  } catch (e) {
    list.innerHTML = `<p class="load-error">Couldn't load players.<br><small>${e.message || e}</small><br><a href="" onclick="location.reload()">Tap to retry</a></p>`;
    return;
  }
  list.innerHTML = '';

  const lastId = localStorage.getItem('disney_last_user');
  const today  = todayKey();
  const curMonth = monthKey();

  users.forEach(user => {
    const card       = document.createElement('div');
    card.className   = 'user-card';
    const streak     = user.dailyStreak || 0;
    const streakText = streak > 0 ? ` · 🔥 ${streak}` : '';
    // Home-card points mirror the leaderboard's "This Month" view (not
    // totalPoints) so this rivalry-facing number is the one that's always
    // winnable — see the monthly-leaderboard note in CLAUDE.md.
    const pts        = user.monthlyKey === curMonth ? (user.monthlyPoints || 0) : 0;
    const stat       = user.totalAnswered
      ? `${pts.toLocaleString()} pts this month · ${pct(user.totalCorrect, user.totalAnswered)} correct${streakText}`
      : streak > 0 ? `🔥 ${streak} day streak` : 'No games yet';
    card.innerHTML = `
      <div class="user-avatar">${disneyAvatar(user.name)}</div>
      <div class="user-info">
        <div class="user-name">${esc(user.name)}</div>
        <div class="user-stats">${stat}</div>
        ${streak > 0 ? `<div class="streak-stars" aria-hidden="true">${streakStars(streak)}</div>` : ''}
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
        <span class="dcmp-name">${disneyAvatar(user.name)} ${esc(user.name)}</span>
        <span class="dcmp-score">${user.lastDailyScore ?? 0}/10 · <strong>${(user.lastDailyPoints||0).toLocaleString()} pts</strong> ✓</span>
      `;
    } else {
      row.innerHTML = `
        <span class="dcmp-name">${disneyAvatar(user.name)} ${esc(user.name)}</span>
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
          <span class="dcmp-name">${disneyAvatar(user.name)} ${esc(user.name)}</span>
          <span class="dcmp-score">${yd.score ?? 0}/10 · <strong>${(yd.points||0).toLocaleString()} pts</strong> ✓</span>
        `;
      } else {
        row.innerHTML = `
          <span class="dcmp-name">${disneyAvatar(user.name)} ${esc(user.name)}</span>
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
  offerGameResume('select');
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
document.getElementById('new-user-input').addEventListener('input', () => {
  document.getElementById('add-user-error').classList.add('hidden');
});

async function addUser() {
  const input = document.getElementById('new-user-input');
  const errEl = document.getElementById('add-user-error');
  const btn   = document.getElementById('btn-add-user');
  const name  = input.value.trim();
  if (!name || btn.disabled) return;
  btn.disabled = true;
  errEl.classList.add('hidden');
  try {
    const users = await storage.getUsers();
    if (users.some(u => u.name.trim().toLowerCase() === name.toLowerCase())) {
      errEl.textContent = `There's already a player named ${name}.`;
      errEl.classList.remove('hidden');
      return;
    }
    await storage.saveUser({ id: slugId(name), name, totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0 });
    renderHome();
  } catch (e) {
    errEl.textContent = "Couldn't add player — check your connection.";
    errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
  }
}

// Leaderboard links
// Bound via an arrow wrapper, not passed directly — a direct listener would
// forward the click Event as renderLeaderboard's `mode` arg, corrupting _lbMode.
document.getElementById('btn-go-leaderboard').addEventListener('click', () => renderLeaderboard());
document.getElementById('btn-leaderboard-back').addEventListener('click', () => renderHome());
document.getElementById('btn-results-leaderboard').addEventListener('click', () => renderLeaderboard());

// =============================================================================
// LEADERBOARD
// =============================================================================
// Lifetime totalPoints never resets, so once one player pulls ahead the
// trailing player has nothing left to play for. "This Month" gives a
// regularly-resetting board (see monthKey()) so there's always a fresh race;
// "Last Month" (prevMonthKey()) lets that race be looked back on once it ends.
let _lbMode = 'lifetime'; // 'lifetime' | 'month' | 'lastmonth'

const LB_PERIOD_KEY = { month: monthKey, lastmonth: prevMonthKey };

async function renderLeaderboard(mode) {
  if (mode) _lbMode = mode;
  showScreen('screen-leaderboard');
  document.querySelectorAll('#lb-mode-group .pill').forEach(p => p.classList.toggle('active', p.dataset.mode === _lbMode));

  const isPeriod   = _lbMode !== 'lifetime';
  const periodKey  = isPeriod ? LB_PERIOD_KEY[_lbMode]() : null;
  const list       = document.getElementById('leaderboard-list');
  const empty      = document.getElementById('leaderboard-empty');
  empty.classList.add('hidden');
  list.innerHTML = '<p class="load-status">Loading leaderboard…</p>';

  let users;
  try {
    users = await storage.getLeaderboard(periodKey);
  } catch (e) {
    list.innerHTML = `<p class="load-error">Couldn't load the leaderboard.<br><small>${e.message || e}</small><br><a href="" onclick="location.reload()">Tap to retry</a></p>`;
    return;
  }
  list.innerHTML = '';

  const medals = ['🥇', '🥈', '🥉'];

  if (!users.length) { empty.classList.remove('hidden'); return; }
  empty.classList.add('hidden');

  const periodLabel = _lbMode === 'month' ? 'this month' : 'last month';

  users.forEach((u, i) => {
    const entry      = document.createElement('div');
    entry.className  = `lb-entry${i < 3 ? ' rank-' + (i + 1) : ''}`;
    const percentage = !isPeriod && u.totalAnswered ? Math.round((u.totalCorrect / u.totalAnswered) * 100) : null;
    const detail      = isPeriod
      ? `🗓️ Points ${periodLabel}`
      : (u.totalAnswered ? `${u.totalAnswered} q · ${u.gamesPlayed} game${u.gamesPlayed !== 1 ? 's' : ''}` : 'No games yet');
    const pts = ((isPeriod ? u.effectivePeriodPoints : u.totalPoints) || 0).toLocaleString();
    entry.innerHTML = `
      <div class="lb-rank">${medals[i] || (i + 1)}</div>
      <div class="lb-avatar">${disneyAvatar(u.name)}</div>
      <div class="lb-info">
        <div class="lb-name">${esc(u.name)}</div>
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

document.getElementById('lb-mode-group').addEventListener('click', e => {
  const pill = e.target.closest('.pill');
  if (!pill) return;
  renderLeaderboard(pill.dataset.mode);
});

// =============================================================================
// WEEKLY HOMEWORK — a new movie assigned every Thursday for family movie night
// =============================================================================

// Older saved states used a bare watchedIds:[id,...] array with no per-movie date.
// Upgrades those in place to watched:[{id, watchedAt}, ...] so date-sorting always works.
function normalizeHomeworkState(state) {
  if (state.watched) return state;
  const fallbackDate = state.pickedAt || new Date(0).toISOString();
  const watched = (state.watchedIds || []).map(id => ({ id, watchedAt: fallbackDate }));
  const { watchedIds, ...rest } = state;
  return { ...rest, watched };
}

// Adds/updates a {id, watchedAt} entry for id, keeping one entry per movie.
function upsertWatched(watched, id, watchedAt) {
  const idx = watched.findIndex(w => w.id === id);
  if (idx === -1) return [...watched, { id, watchedAt }];
  const copy = [...watched];
  copy[idx] = { id, watchedAt };
  return copy;
}

// Called once at boot. If the stored pick belongs to a prior homework week, the
// outgoing movie is assumed watched (homework complete!) and a fresh one is drawn
// from the unwatched pool. Never called by the shuffle button — rollover and veto
// must stay separate, since only rollover marks a movie watched.
async function rollHomeworkIfStale() {
  // Let a failed read propagate to init()'s catch (card stays hidden). Swallowing it
  // here would treat "couldn't read" as "no state" and roll a fresh pick with an empty
  // watched list — clobbering the real state and watch history on a transient error.
  const state = await storage.getHomeworkState();
  const wk = homeworkWeekKey();

  if (state && state.weekKey === wk) {
    homeworkState = normalizeHomeworkState(state);
    return;
  }

  let watched = state ? normalizeHomeworkState(state).watched : [];
  if (state && state.movieId != null) {
    watched = upsertWatched(watched, state.movieId, new Date().toISOString());
  }

  // pickFromMoviePool falls back to the full pool once everything's been watched —
  // history is intentionally kept (not wiped) so a rewatch just updates that entry's date.
  const { movie } = pickFromMoviePool(watched.map(w => w.id));

  homeworkState = { weekKey: wk, movieId: movie.id, pickedAt: new Date().toISOString(), watched };
  try { await storage.saveHomeworkState(homeworkState); } catch(e) {}
}

// Vetoes the current pick and draws a new one from the pool. The vetoed movie goes
// back into the pool — it is NOT added to watched. Kristen-only (gated in the UI).
async function shuffleHomework() {
  if (!homeworkState) return;
  const exclude = [...homeworkState.watched.map(w => w.id), homeworkState.movieId];
  const { movie } = pickFromMoviePool(exclude);
  homeworkState = { ...homeworkState, movieId: movie.id, pickedAt: new Date().toISOString() };
  try { await storage.saveHomeworkState(homeworkState); } catch(e) {}
}

// Un-watches a movie, putting it back in the pool. Open to any player — no Kristen gate.
async function removeFromWatched(movieId) {
  if (!homeworkState) return;
  homeworkState = { ...homeworkState, watched: homeworkState.watched.filter(w => w.id !== movieId) };
  try { await storage.saveHomeworkState(homeworkState); } catch(e) {}
}

function renderHomeworkCard() {
  const card = document.getElementById('homework-card');
  if (!homeworkState || !MOVIES.length) { card.classList.add('hidden'); return; }
  const movie = MOVIES.find(m => m.id === homeworkState.movieId);
  if (!movie) { card.classList.add('hidden'); return; }

  card.classList.remove('hidden');
  document.getElementById('homework-movie-title').textContent = `${movie.title} (${movie.year})`;

  // Gated on currentUser (this session's actual login), not the localStorage
  // "last user" — that persists across sessions on a shared device, so anyone
  // opening the app after Kristen last used it would see the button before
  // ever selecting a player. Requiring a real selectUser() call this session
  // means the button only appears once Kristen has actually logged in.
  const isKristen = currentUser && currentUser.id === 'kristen';
  document.getElementById('btn-shuffle-homework').classList.toggle('hidden', !isKristen);

  renderWatchedList();
}

const HW_DATE_FMT = d => new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

// Renders the full movie pool as two groups: Watched (newest watch date first, with an
// ✕ to un-watch) and everything not yet assigned (alphabetical, read-only). The current
// week's pick is shown separately up top already, so it's excluded from both groups here.
function renderWatchedList() {
  const toggleBtn = document.getElementById('btn-toggle-watched');
  const listEl     = document.getElementById('homework-watched-list');
  if (!MOVIES.length || !homeworkState) { toggleBtn.classList.add('hidden'); return; }

  toggleBtn.classList.remove('hidden');
  const isOpen = !listEl.classList.contains('hidden');
  toggleBtn.textContent = isOpen ? 'Hide Movie List' : '🎬 View Full Movie List';

  const watchedIdSet = new Set(homeworkState.watched.map(w => w.id));

  const watchedMovies = homeworkState.watched
    .slice()
    .sort((a, b) => new Date(b.watchedAt) - new Date(a.watchedAt))
    .map(w => { const m = MOVIES.find(mv => mv.id === w.id); return m ? { ...m, watchedAt: w.watchedAt } : null; })
    .filter(Boolean);

  const unwatchedMovies = MOVIES
    .filter(m => !watchedIdSet.has(m.id) && m.id !== homeworkState.movieId)
    .slice()
    .sort((a, b) => a.title.localeCompare(b.title));

  const watchedHtml = watchedMovies.length
    ? `<div class="watched-section-label">✅ Watched (${watchedMovies.length})</div>` +
      watchedMovies.map(m => `
        <div class="watched-row">
          <span class="watched-title">${m.title} <span class="watched-year">(${m.year})</span></span>
          <span class="watched-date">${HW_DATE_FMT(m.watchedAt)}</span>
          <button class="watched-remove" data-id="${m.id}" title="Put back in the pool">✕</button>
        </div>
      `).join('')
    : '';

  const unwatchedHtml = unwatchedMovies.length
    ? `<div class="watched-section-label">🍿 Not Yet Assigned (${unwatchedMovies.length})</div>` +
      unwatchedMovies.map(m => `
        <div class="watched-row">
          <span class="watched-title">${m.title} <span class="watched-year">(${m.year})</span></span>
        </div>
      `).join('')
    : '';

  listEl.innerHTML = watchedHtml + unwatchedHtml;
}

document.getElementById('btn-shuffle-homework').addEventListener('click', async () => {
  const btn = document.getElementById('btn-shuffle-homework');
  btn.disabled = true;
  await shuffleHomework();
  renderHomeworkCard();
  btn.disabled = false;
});

document.getElementById('btn-toggle-watched').addEventListener('click', () => {
  document.getElementById('homework-watched-list').classList.toggle('hidden');
  renderWatchedList();
});

document.getElementById('homework-watched-list').addEventListener('click', async e => {
  const btn = e.target.closest('.watched-remove');
  if (!btn) return;
  btn.disabled = true;
  await removeFromWatched(parseInt(btn.dataset.id, 10));
  renderHomeworkCard();
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

  const progress = getDailyProgress(currentUser.id);
  const resumeCount = (!played && progress && progress.dateKey === today && Array.isArray(progress.answers))
    ? progress.answers.length : 0;

  if (played) {
    statusEl.textContent = `✓ Played today · 🔥 ${streak} day streak`;
    statusEl.className   = 'daily-status daily-done';
    btn.textContent      = '📋 Review Today\'s Questions';
    btn.classList.add('done');
  } else if (resumeCount > 0) {
    statusEl.textContent = `▶️ ${resumeCount} of 10 answered — pick up where you left off`;
    statusEl.className   = 'daily-status daily-active';
    btn.textContent      = `▶️ Resume Daily Challenge (${resumeCount}/10)`;
    btn.classList.remove('done');
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
  if (btn.disabled) return;
  btn.disabled = true;
  if (await offerGameResume('start') !== 'proceed') { btn.disabled = false; return; }

  let questions;
  try {
    const pinnedIds = await storage.getDailyPins(today);
    if (pinnedIds && pinnedIds.length > 0) {
      const qMap = new Map(QUESTIONS.map(q => [q.id, q]));
      let qs = pinnedIds.map(id => qMap.get(id)).filter(Boolean);
      // Some pinned IDs may have been removed from the shards (e.g. a dedup
      // pass) since this day's pins were first written — top back up to the
      // original count from the live pool and re-save so later players/review
      // see a consistent, full-length set.
      if (qs.length > 0 && qs.length < pinnedIds.length) {
        const usedIds     = new Set(qs.map(q => q.id));
        const candidates  = QUESTIONS.filter(q => !usedIds.has(q.id));
        const excludeIds  = await dailyExclusionSet();
        const freshCands  = candidates.filter(q => !excludeIds.has(q.id));
        const extrasSrc   = freshCands.length >= (pinnedIds.length - qs.length) ? freshCands : candidates;
        const extras      = shuffle(extrasSrc).slice(0, pinnedIds.length - qs.length);
        qs = qs.concat(extras);
        try { await storage.saveDailyPins(today, qs.map(q => q.id)); } catch(e) {}
      }
      if (qs.length > 0) questions = qs;
    }
  } catch(e) {}

  if (!questions) {
    const excludeIds = await dailyExclusionSet();
    questions = getDailyQuestions(10, 0, excludeIds);
    try { await storage.saveDailyPins(today, questions.map(q => q.id)); } catch(e) {}
  }

  btn.disabled = false;
  gameState = buildDailyGameState(questions, today);
  gameState.dateKey = today; // checkpoint under the day this daily belongs to, even if answered past the rollover
  if (gameState.currentIndex >= gameState.questions.length) {
    endGame(); // all questions were answered before a previous exit — finish it now
  } else {
    renderGameQuestion();
  }
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

// Starts a fresh regular game from the current settings. Settles any leftover
// checkpoint first (resume it, or commit it and start new).
async function startRegularGame() {
  const pool  = filteredPool();
  if (pool.length === 0) return;
  if (await offerGameResume('start') !== 'proceed') return;
  const count = Math.min(gameSettings.questionCount, pool.length);
  gameState = { questions: pickRegularQuestions(pool, getSeenIds(currentUser.id), count), currentIndex: 0, answers: [], score: 0, currentStreak: 0, isDaily: false, pointsEarned: 0, scoreBreakdown: null };
  renderGameQuestion();
}

document.getElementById('btn-start-game').addEventListener('click', () => {
  if (gameSettings.categories.length === 0) {
    document.getElementById('cat-error').classList.remove('hidden');
    return;
  }
  startRegularGame();
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

  const dotsWrap = document.getElementById('progress-dots');
  dotsWrap.classList.toggle('hidden', total > 12);
  if (total <= 12) {
    dotsWrap.innerHTML = '';
    for (let i = 0; i < total; i++) {
      const dot = document.createElement('span');
      dot.className = 'progress-dot';
      if (i < gameState.answers.length) {
        dot.classList.add(gameState.answers[i].correct ? 'correct' : 'wrong');
      } else if (i === gameState.currentIndex) {
        dot.classList.add('current');
      }
      dotsWrap.appendChild(dot);
    }
  }
  const catBadge = document.getElementById('game-cat-badge');
  catBadge.textContent = catLabel(q.category);
  catBadge.className   = `cat-badge cat-${q.category}`;

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
  document.getElementById('btn-flag').disabled = false; // re-enable after a flag on a previous question

  // showScreen() only fires once per game (screen-game has no h1/h2 to land on
  // anyway); each new question is effectively its own "screen" for a screen
  // reader, so move focus to the question text every time one renders.
  document.getElementById('question-text').focus({ preventScroll: true });
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
    const selectedBtn = document.querySelector(`.answer-btn[data-idx="${selectedIdx}"]`);
    if (selectedBtn) spawnSparkles(selectedBtn);
  } else {
    gameState.currentStreak = 0;
    sounds.wrong();
    if (navigator.vibrate) navigator.vibrate(80);
  }

  // React the current dot immediately on tap rather than waiting for the next
  // renderGameQuestion() call, so the dot row feels tied to the answer itself.
  const curDot = document.getElementById('progress-dots').children[gameState.currentIndex];
  if (curDot) {
    curDot.classList.remove('current');
    curDot.classList.add(isCorrect ? 'correct' : 'wrong');
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
  checkpointGame();
  document.getElementById('game-score-display').textContent = `${gameState.score} ✓`;

  const isLast = gameState.currentIndex === gameState.questions.length - 1;
  document.getElementById('btn-next').textContent = isLast ? 'See Results ✨' : 'Next →';
  document.getElementById('feedback-area').classList.remove('hidden');

  // Set the live-region text after unhiding, not before — a screen reader won't
  // reliably announce a change to a node's content while it's still display:none.
  const feedbackMsg = document.getElementById('feedback-msg');
  if (isCorrect) {
    feedbackMsg.textContent = '✓ Correct!';
    feedbackMsg.className   = 'feedback-msg fb-correct';
  } else {
    feedbackMsg.textContent = `✗ The correct answer was: ${q.answers[0]}`;
    feedbackMsg.className   = 'feedback-msg fb-wrong';
  }
}

document.getElementById('btn-next').addEventListener('click', () => {
  gameState.currentIndex++;
  if (gameState.currentIndex >= gameState.questions.length) {
    endGame();
  } else {
    renderGameQuestion();
  }
});

// Exit game — shared by the Exit button and the phone's Back button.
let _exitInFlight = false;

async function exitGameFlow() {
  if (gameState.ended || _exitInFlight) return;
  _exitInFlight = true;
  try {
    const answered = gameState.answers.length;
    const plural   = answered !== 1 ? 's' : '';

    // Daily challenge: nothing is committed to stats until the full 10 are done.
    // Answers are already checkpointed locally after every tap (checkpointGame),
    // so re-opening the Daily Challenge resumes at the next question.
    if (gameState.isDaily) {
      const ok = await showConfirm({
        title:       'Leave the Daily Challenge?',
        message:     answered > 0
          ? `Your ${answered} answered question${plural} are locked in — come back later to finish.`
          : "You haven't answered any questions yet.",
        confirmText: 'Exit',
        cancelText:  'Keep playing'
      });
      if (ok !== true) return;
      if (answered > 0) {
        // Local marking always happens (nothing's committed to Firestore until
        // the daily is fully finished). The cross-player Firestore sync is
        // best-effort: swallow a failure so an offline exit still works.
        const newSeen = computeSeenIds(currentUser.id, gameState.answers.map(a => a.question.id));
        saveSeenIds(currentUser.id, newSeen);
        storage.saveRecentQuestionIds(currentUser.id, newSeen).catch(() => {});
      }
      renderHome();
      return;
    }

    const ok = await showConfirm({
      title:       'Leave this game?',
      message:     answered > 0
        ? `Your ${answered} answered question${plural} will be saved to your stats.`
        : "You haven't answered any questions yet.",
      confirmText: 'Exit',
      cancelText:  'Keep playing'
    });
    if (ok !== true) return;
    if (answered > 0) {
      try {
        await commitRegularAnswers(gameState.answers, false);
        clearGameCheckpoint(currentUser.id);
      } catch (e) {
        // Checkpoint stays — offerGameResume() offers it again next time.
        await showAlert("Couldn't save", "Your answers couldn't be saved — check your connection. They're kept on this device, and you'll be offered them next time you pick your player.");
      }
    }
    renderHome();
  } finally {
    _exitInFlight = false;
  }
}

document.getElementById('btn-exit-game').addEventListener('click', exitGameFlow);

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
  const submitBtn = document.getElementById('btn-flag-submit');
  if (submitBtn.disabled) return; // guard against double-click / rapid Enter
  submitBtn.disabled = true;

  const q       = gameState.questions[gameState.currentIndex];
  const comment = document.getElementById('flag-comment').value.trim();
  try {
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
  } catch (e) {
    showAlert("Couldn't send", "Your report couldn't be sent — check your connection and try again."); // form stays open for retry
  } finally {
    submitBtn.disabled = false;
  }
}

// =============================================================================
// RESULTS SCREEN
// =============================================================================
async function endGame() {
  // Guards against double-committing stats — a double-click on the final
  // "See Results" tap, or two near-simultaneous "resume already-complete
  // daily" calls, would otherwise both race storage.updateStats().
  if (gameState.ended) return;
  gameState.ended = true;

  const today             = todayKey();
  const isFirstDailyToday = gameState.isDaily && currentUser.lastDailyDate !== today;

  // Compute new daily streak before scoring so the bonus uses the correct level
  const newDailyStreak = isFirstDailyToday
    ? nextDailyStreak(currentUser.lastDailyDate, currentUser.dailyStreak, today)
    : (currentUser.dailyStreak || 0);

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

  // If the save fails (offline), still show the results screen with a warning
  // instead of stranding the player on the game screen. Seen-ids stay unmarked so
  // an unsaved game's questions can come around again.
  // saveFailed means "updateStats rejected" and nothing else — the refresh
  // below is separate so a timed-out read after a landed write can't claim
  // the score was kept on-device (it was already cleared) or leave the daily
  // replayable via a stale lastDailyDate.
  gameState.saveFailed = false;
  try {
    const newSeen = computeSeenIds(currentUser.id, gameState.questions.map(q => q.id));
    await storage.updateStats(currentUser.id, gameState.questions.length, gameState.score, bd.total, dailyUpdate, buildCatStats(gameState.answers), newSeen, monthKey());
    saveSeenIds(currentUser.id, newSeen);
    if (gameState.isDaily) clearDailyProgress(currentUser.id);
    else clearGameCheckpoint(currentUser.id);
  } catch (e) {
    gameState.saveFailed = true;
  }
  if (!gameState.saveFailed) {
    try {
      const users = await storage.getUsers();
      currentUser = users.find(u => u.id === currentUser.id) || currentUser;
    } catch (e) {
      if (isFirstDailyToday) {
        currentUser.lastDailyDate = today;
        currentUser.dailyStreak   = newDailyStreak;
      }
    }
  }
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
  document.getElementById('results-fireworks').classList.toggle('perfect', percentage === 100);
  document.getElementById('save-warning').classList.toggle('hidden', !gameState.saveFailed);
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
    row.className = `breakdown-row cat-${cat}`;
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
            `<span class="dr-chip ${c.correct ? 'dr-chip-correct' : 'dr-chip-wrong'}">${disneyAvatar(c.user.name)} ${esc(c.user.name)} ${c.correct ? '✓' : '✗'}</span>`
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
        `<div class="dr-player-ans dr-not-played">${disneyAvatar(u.name)} ${esc(u.name)}: played — details unavailable</div>`),
      ...notPlayedUsers.map(u =>
        `<div class="dr-player-ans dr-not-played">${disneyAvatar(u.name)} ${esc(u.name)}: —</div>`)
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
  startRegularGame();
});

document.getElementById('btn-play-again').addEventListener('click', renderSettings);
document.getElementById('btn-results-home').addEventListener('click', renderHome);

// =============================================================================
// Boot
// =============================================================================
// A stalled (not failed) fetch never rejects on its own, so a flaky connection
// would otherwise hang boot behind the quote rotation forever with no error
// shown. AbortController turns that stall into a real rejection the existing
// try/catch + "Tap to retry" UI can handle.
function fetchWithTimeout(url, opts = {}, timeoutMs = 10000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  return fetch(url, { ...opts, signal: controller.signal }).finally(() => clearTimeout(timer));
}

async function loadQuestions() {
  const manifest = await fetchWithTimeout('questions/manifest.json', { cache: 'no-cache' }).then(r => r.json());
  const shards = await Promise.all(manifest.shards.map(s => fetchWithTimeout(s, { cache: 'no-cache' }).then(r => r.json())));
  QUESTIONS = shards.flat();
}

async function loadMovies() {
  const data = await fetchWithTimeout('movies.json', { cache: 'no-cache' }).then(r => r.json());
  MOVIES = data.movies;
}

// Boot-screen quote rotation ("Wishing on a star…") — real Walt Disney quotes,
// cycled while questions/movies load. Most sessions load fast enough that only
// the first quote is ever seen; the rotation is for the rare slow-connection case.
const BOOT_QUOTES = [
  'All our dreams can come true, if we have the courage to pursue them.',
  "It's kind of fun to do the impossible.",
  'The way to get started is to quit talking and begin doing.',
  'If you can dream it, you can do it.'
];
let _bootQuoteTimer = null;

function startBootQuotes() {
  let i = 0;
  _bootQuoteTimer = setInterval(() => {
    const el = document.getElementById('boot-quote');
    if (!el || !document.body.contains(el)) { stopBootQuotes(); return; }
    i = (i + 1) % BOOT_QUOTES.length;
    el.classList.add('fading');
    setTimeout(() => {
      const target = document.getElementById('boot-quote');
      if (target) target.textContent = BOOT_QUOTES[i];
      if (target) target.classList.remove('fading');
    }, 250);
  }, 2600);
}

function stopBootQuotes() {
  if (_bootQuoteTimer) { clearInterval(_bootQuoteTimer); _bootQuoteTimer = null; }
}

async function init() {
  startBootQuotes();
  try {
    await loadQuestions();
  } catch (e) {
    stopBootQuotes();
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
  stopBootQuotes();
  renderHome();
  checkForUpdate();
}
init();
