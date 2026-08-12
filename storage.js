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
  // recentQuestionIds — this player's full capped seen-ids list (already computed
  //   client-side), or null to leave the field untouched. Mirrors localStorage's
  //   `disney_seen_{userId}` into Firestore so daily-pin generation can exclude
  //   anything any player has recently played, in any mode.
  // monthKey — "YYYY-MM" for the month this game's points count toward (primary
  //   state, same reset-on-new-key pattern as the daily streak fields below —
  //   not derived, since there's no history of past games to recompute it from).
  async updateStats(userId, answered, correct, points, dailyUpdate, catStats, recentQuestionIds, monthKey) {
    const data = this._load();
    const u = data.users[userId];
    if (!u) throw new Error('User not found: ' + userId);
    u.totalAnswered += answered;
    u.totalCorrect  += correct;
    u.gamesPlayed   += 1;
    u.totalPoints    = (u.totalPoints || 0) + points;
    if (monthKey) {
      u.monthlyPoints = (u.monthlyKey === monthKey ? (u.monthlyPoints || 0) : 0) + points;
      u.monthlyKey    = monthKey;
    }
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
    if (recentQuestionIds) u.recentQuestionIds = recentQuestionIds;
    this._save(data);
    return u;
  }

  async saveRecentQuestionIds(userId, ids) {
    const data = this._load();
    const u = data.users[userId];
    if (!u) throw new Error('User not found: ' + userId);
    u.recentQuestionIds = ids;
    this._save(data);
  }

  async getDailyPins(dateKey) {
    const data = this._load();
    return (data.dailies && data.dailies[dateKey]) ? data.dailies[dateKey] : null;
  }

  async saveDailyPins(dateKey, questionIds) {
    const data = this._load();
    if (!data.dailies) data.dailies = {};
    data.dailies[dateKey] = questionIds;
    this._save(data);
  }

  // Every question ID pinned as a daily challenge on or after sinceDateKey
  // ("YYYY-MM-DD", lexically comparable) — independent of whether anyone
  // actually played that day. Used alongside recentQuestionIds so daily-pin
  // generation doesn't depend on someone having recently played. Rolling
  // window, not all-time: see the caller in app.js for why an unbounded
  // history isn't safe long-term.
  async getAllDailyQuestionIds(sinceDateKey) {
    const data = this._load();
    const ids = new Set();
    Object.entries(data.dailies || {}).forEach(([dateKey, arr]) => {
      if (dateKey >= sinceDateKey) (arr || []).forEach(id => ids.add(id));
    });
    return Array.from(ids);
  }

  async getHomeworkState() {
    const data = this._load();
    return data.weeklyHomework || null;
  }

  async saveHomeworkState(state) {
    const data = this._load();
    data.weeklyHomework = state;
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

  // monthKey — optional "YYYY-MM". When passed, each returned user gets an
  // `effectiveMonthlyPoints` field (0 if their stored monthlyKey isn't this
  // month, i.e. they haven't played yet this month) and the sort uses that
  // instead of lifetime totalPoints. Computed here for display only — never
  // written back, per the no-derived-values-in-storage rule.
  async getLeaderboard(monthKey = null) {
    let users = Object.values(this._load().users || {});
    if (monthKey) {
      users = users.map(u => ({ ...u, effectiveMonthlyPoints: u.monthlyKey === monthKey ? (u.monthlyPoints || 0) : 0 }));
      return users.sort((a, b) => b.effectiveMonthlyPoints - a.effectiveMonthlyPoints);
    }
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
    // Fire-and-forget: swallow so an offline load doesn't surface an unhandled
    // rejection. getUsers() will show its own error UI if Firestore is unreachable.
    this._seed().catch(() => {});
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
  // recentQuestionIds — this player's full capped seen-ids list (already computed
  //   client-side), or null to leave the field untouched. Mirrors localStorage's
  //   `disney_seen_{userId}` into Firestore so daily-pin generation can exclude
  //   anything any player has recently played, in any mode. Written inside this
  //   same transaction (no extra round trip) since every call site that reaches
  //   here already has stats to commit.
  // monthKey — "YYYY-MM" for the month this game's points count toward (primary
  //   state — resets on a new key, same pattern as the daily streak fields below).
  async updateStats(userId, answered, correct, points, dailyUpdate, catStats, recentQuestionIds, monthKey) {
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
      if (monthKey) {
        update.monthlyPoints = (d.monthlyKey === monthKey ? (d.monthlyPoints || 0) : 0) + points;
        update.monthlyKey    = monthKey;
      }
      if (recentQuestionIds) update.recentQuestionIds = recentQuestionIds;
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

  // Standalone (no stats transaction) sync point for a partial daily-challenge
  // exit — nothing is committed to stats until the daily is fully finished, but
  // the already-answered questions still need to count as "recently seen" for
  // daily-pin exclusion. Callers treat this as best-effort and swallow errors.
  async saveRecentQuestionIds(userId, ids) {
    await this.db.collection('users').doc(userId).update({ recentQuestionIds: ids });
  }

  async getDailyPins(dateKey) {
    const doc = await this.db.collection('dailies').doc(dateKey).get();
    return doc.exists ? (doc.data().questionIds || null) : null;
  }

  async saveDailyPins(dateKey, questionIds) {
    await this.db.collection('dailies').doc(dateKey).set({ questionIds });
  }

  // Every question ID pinned as a daily challenge on or after sinceDateKey
  // ("YYYY-MM-DD") — independent of whether anyone actually played that day.
  // Used alongside recentQuestionIds so daily-pin generation doesn't depend
  // on someone having recently played, and doesn't get bypassed by heavy
  // regular-game play pushing a daily question out of any one player's
  // capped seen-ids window. Rolling window (not all-time): doc IDs are
  // "YYYY-MM-DD" so they sort lexically = chronologically, letting Firestore
  // do the filtering server-side instead of reading the whole collection —
  // this also keeps the read cost flat as the app ages instead of growing
  // ~1 doc/day forever. See the caller in app.js for why unbounded history
  // isn't safe: with a ~2,050-question corpus and 10 exclusions/day, an
  // all-time union would exhaust the corpus in ~205 days and then silently
  // fall back to zero exclusion every day after that.
  async getAllDailyQuestionIds(sinceDateKey) {
    const snap = await this.db.collection('dailies')
      .where(firebase.firestore.FieldPath.documentId(), '>=', sinceDateKey)
      .get();
    const ids = new Set();
    snap.docs.forEach(d => (d.data().questionIds || []).forEach(id => ids.add(id)));
    return Array.from(ids);
  }

  async getHomeworkState() {
    const doc = await this.db.collection('weeklyHomework').doc('state').get();
    return doc.exists ? doc.data() : null;
  }

  async saveHomeworkState(state) {
    await this.db.collection('weeklyHomework').doc('state').set(state);
  }

  async flagReport(report) {
    await this.db.collection('flags').add(report);
  }

  async getFlags() {
    const snap = await this.db.collection('flags').get();
    return snap.docs.map(d => ({ _id: d.id, ...d.data() }));
  }

  // monthKey — optional "YYYY-MM". When passed, each returned user gets an
  // `effectiveMonthlyPoints` field (0 if their stored monthlyKey isn't this
  // month, i.e. they haven't played yet this month) and the sort uses that
  // instead of lifetime totalPoints. Computed here for display only — never
  // written back, per the no-derived-values-in-storage rule.
  async getLeaderboard(monthKey = null) {
    const snap  = await this.db.collection('users').get();
    let users = snap.docs.map(d => d.data());
    if (monthKey) {
      users = users.map(u => ({ ...u, effectiveMonthlyPoints: u.monthlyKey === monthKey ? (u.monthlyPoints || 0) : 0 }));
      return users.sort((a, b) => b.effectiveMonthlyPoints - a.effectiveMonthlyPoints);
    }
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
