class LocalStorageAdapter {
  constructor() {
    this.KEY = 'disney_trivia_v1';
    this._seed();
  }

  _load() {
    try { return JSON.parse(localStorage.getItem(this.KEY)) || {}; }
    catch { return {}; }
  }

  _save(data) { localStorage.setItem(this.KEY, JSON.stringify(data)); }

  _seed() {
    const data = this._load();
    if (!data.users) {
      data.users = {
        kristen: { id: 'kristen', name: 'Kristen', totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0 },
        cara:    { id: 'cara',    name: 'Cara',    totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0 }
      };
      this._save(data);
    }
  }

  async getUsers() {
    return Object.values(this._load().users || {});
  }

  async saveUser(user) {
    const data = this._load();
    if (!data.users) data.users = {};
    data.users[user.id] = user;
    this._save(data);
    return user;
  }

  // points — pts earned this game (primary state; not recomputable from counters alone)
  // dailyUpdate — {score, points, dateKey, streak} or null
  // catStats    — {category: {answered, correct}, ...} or null
  async updateStats(userId, answered, correct, points, dailyUpdate, catStats) {
    const data = this._load();
    const u = data.users[userId];
    if (!u) throw new Error('User not found: ' + userId);
    u.totalAnswered += answered;
    u.totalCorrect  += correct;
    u.gamesPlayed   += 1;
    u.totalPoints    = (u.totalPoints || 0) + points;
    if (catStats) {
      if (!u.categoryStats) u.categoryStats = {};
      for (const [cat, counts] of Object.entries(catStats)) {
        const prev = u.categoryStats[cat] || { answered: 0, correct: 0 };
        u.categoryStats[cat] = { answered: prev.answered + counts.answered, correct: prev.correct + counts.correct };
      }
    }
    if (dailyUpdate) {
      // First play of a new day: shift current slot into prev before overwriting
      if (dailyUpdate.streak !== null && u.lastDailyDate && u.lastDailyDate !== dailyUpdate.dateKey) {
        u.prevDailyDate    = u.lastDailyDate;
        u.prevDailyScore   = u.lastDailyScore  ?? 0;
        u.prevDailyPoints  = u.lastDailyPoints ?? 0;
        u.prevDailyAnswers = u.lastDailyAnswers || null;
      }
      u.lastDailyScore  = dailyUpdate.score;
      u.lastDailyPoints = dailyUpdate.points;
      u.lastDailyDate   = dailyUpdate.dateKey;
      if (dailyUpdate.streak !== null) u.dailyStreak = dailyUpdate.streak;
      if (dailyUpdate.answers)         u.lastDailyAnswers = dailyUpdate.answers;
    }
    this._save(data);
    return u;
  }

  async updateDailyStreak(userId, streak, dateKey) {
    const data = this._load();
    const u = data.users[userId];
    if (!u) throw new Error('User not found: ' + userId);
    u.dailyStreak    = streak;
    u.lastDailyDate  = dateKey;
    this._save(data);
  }

  async flagReport(report) {
    const data = this._load();
    if (!data.flags) data.flags = [];
    data.flags.push(report);
    this._save(data);
  }

  async getFlags() {
    return this._load().flags || [];
  }

  async getLeaderboard() {
    const users = Object.values(this._load().users || {});
    return users.sort((a, b) => {
      const ptsDiff = (b.totalPoints || 0) - (a.totalPoints || 0);
      if (ptsDiff !== 0) return ptsDiff;
      const pa = a.totalAnswered ? a.totalCorrect / a.totalAnswered : -1;
      const pb = b.totalAnswered ? b.totalCorrect / b.totalAnswered : -1;
      return pb - pa;
    });
  }
}

// =============================================================================
// Firebase adapter — shared leaderboard across devices
// =============================================================================
class FirebaseAdapter {
  constructor() {
    firebase.initializeApp({
      apiKey:            "AIzaSyC_keHyGc1Z46rzqB9wNKJ36wZgHscfGrQ",
      authDomain:        "disneytrivia-38ac6.firebaseapp.com",
      projectId:         "disneytrivia-38ac6",
      storageBucket:     "disneytrivia-38ac6.firebasestorage.app",
      messagingSenderId: "817552679289",
      appId:             "1:817552679289:web:1e82c3f0c72eeed2020fa8"
    });
    this.db = firebase.firestore();
    this._seed();
  }

  async _seed() {
    const defaults = [
      { id: 'kristen', name: 'Kristen', totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0 },
      { id: 'cara',    name: 'Cara',    totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0 }
    ];
    for (const u of defaults) {
      const ref  = this.db.collection('users').doc(u.id);
      const snap = await ref.get();
      if (!snap.exists) await ref.set(u);
    }
  }

  async getUsers() {
    const snap = await this.db.collection('users').get();
    return snap.docs.map(d => d.data());
  }

  async saveUser(user) {
    await this.db.collection('users').doc(user.id).set(user);
    return user;
  }

  // points — pts earned this game (primary state; not recomputable from counters alone)
  // dailyUpdate — {score, points, dateKey, streak} or null
  // catStats    — {category: {answered, correct}, ...} or null
  async updateStats(userId, answered, correct, points, dailyUpdate, catStats) {
    const ref = this.db.collection('users').doc(userId);
    await this.db.runTransaction(async tx => {
      const doc = await tx.get(ref);
      const d   = doc.data();
      const update = {
        totalAnswered: d.totalAnswered + answered,
        totalCorrect:  d.totalCorrect  + correct,
        gamesPlayed:   d.gamesPlayed   + 1,
        totalPoints:   (d.totalPoints || 0) + points
      };
      if (catStats) {
        const existing = d.categoryStats || {};
        const merged   = { ...existing };
        for (const [cat, counts] of Object.entries(catStats)) {
          const prev = merged[cat] || { answered: 0, correct: 0 };
          merged[cat] = { answered: prev.answered + counts.answered, correct: prev.correct + counts.correct };
        }
        update.categoryStats = merged;
      }
      if (dailyUpdate) {
        // First play of a new day: shift current slot into prev before overwriting
        if (dailyUpdate.streak !== null && d.lastDailyDate && d.lastDailyDate !== dailyUpdate.dateKey) {
          update.prevDailyDate    = d.lastDailyDate;
          update.prevDailyScore   = d.lastDailyScore  ?? 0;
          update.prevDailyPoints  = d.lastDailyPoints ?? 0;
          update.prevDailyAnswers = d.lastDailyAnswers || null;
        }
        update.lastDailyScore  = dailyUpdate.score;
        update.lastDailyPoints = dailyUpdate.points;
        update.lastDailyDate   = dailyUpdate.dateKey;
        if (dailyUpdate.streak !== null) update.dailyStreak = dailyUpdate.streak;
        if (dailyUpdate.answers)         update.lastDailyAnswers = dailyUpdate.answers;
      }
      tx.update(ref, update);
    });
  }

  async updateDailyStreak(userId, streak, dateKey) {
    await this.db.collection('users').doc(userId).update({
      dailyStreak:   streak,
      lastDailyDate: dateKey
    });
  }

  async flagReport(report) {
    await this.db.collection('flags').add(report);
  }

  async getFlags() {
    const snap = await this.db.collection('flags').get();
    return snap.docs.map(d => ({ _id: d.id, ...d.data() }));
  }

  async getLeaderboard() {
    const snap  = await this.db.collection('users').get();
    const users = snap.docs.map(d => d.data());
    return users.sort((a, b) => {
      const ptsDiff = (b.totalPoints || 0) - (a.totalPoints || 0);
      if (ptsDiff !== 0) return ptsDiff;
      const pa = a.totalAnswered ? a.totalCorrect / a.totalAnswered : -1;
      const pb = b.totalAnswered ? b.totalCorrect / b.totalAnswered : -1;
      return pb - pa;
    });
  }
}

const storage = new FirebaseAdapter();
