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
        kristen: { id: 'kristen', name: 'Kristen', totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0 },
        cara:    { id: 'cara',    name: 'Cara',    totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0 }
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

  async updateStats(userId, answered, correct) {
    const data = this._load();
    const u = data.users[userId];
    if (!u) throw new Error('User not found: ' + userId);
    u.totalAnswered += answered;
    u.totalCorrect  += correct;
    u.gamesPlayed   += 1;
    this._save(data);
    return u;
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
      const pa = a.totalAnswered ? a.totalCorrect / a.totalAnswered : -1;
      const pb = b.totalAnswered ? b.totalCorrect / b.totalAnswered : -1;
      if (pb !== pa) return pb - pa;
      return b.totalAnswered - a.totalAnswered;
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
      { id: 'kristen', name: 'Kristen', totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0 },
      { id: 'cara',    name: 'Cara',    totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0 }
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

  async updateStats(userId, answered, correct) {
    const ref = this.db.collection('users').doc(userId);
    await this.db.runTransaction(async tx => {
      const doc = await tx.get(ref);
      const d   = doc.data();
      tx.update(ref, {
        totalAnswered: d.totalAnswered + answered,
        totalCorrect:  d.totalCorrect  + correct,
        gamesPlayed:   d.gamesPlayed   + 1
      });
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
      const pa = a.totalAnswered ? a.totalCorrect / a.totalAnswered : -1;
      const pb = b.totalAnswered ? b.totalCorrect / b.totalAnswered : -1;
      if (pb !== pa) return pb - pa;
      return b.totalAnswered - a.totalAnswered;
    });
  }
}

const storage = new FirebaseAdapter();
