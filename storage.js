// Persistent operations share pure rules in data-logic.js. Never retry a score
// by inventing a new game id; its receipt and counters commit atomically.
class LocalStorageAdapter {
  constructor() { this.KEY = 'disney_trivia_v1'; this._seed(); }
  _load() { try { return JSON.parse(localStorage.getItem(this.KEY)) || {}; } catch { return {}; } }
  _save(data) { localStorage.setItem(this.KEY, JSON.stringify(data)); }
  _seed() {
    const d = this._load();
    if (!d.users) {
      d.users = Object.fromEntries(['Kristen', 'Cara'].map(name => [name.toLowerCase(), {
        id: name.toLowerCase(), name, totalAnswered: 0, totalCorrect: 0, gamesPlayed: 0, totalPoints: 0
      }]));
      this._save(d);
    }
  }
  async getUsers() { return Object.values(this._load().users || {}); }
  async saveUser(user) {
    const d = this._load();
    if (Object.values(d.users).some(u => u.name.toLowerCase() === user.name.toLowerCase())) throw new Error('Player already exists.');
    d.users[user.id] = user; this._save(d); return user;
  }
  async updateStats(userId, answered, correct, points, daily, cats, recent, period, log, op) {
    const d = this._load(), u = d.users[userId];
    if (!u) throw new Error('Player not found.');
    if (op && (op.resetRevision || 0) !== (u.resetRevision || 0)) throw Object.assign(new Error('Scores were reset. Start a new game.'), {code:'reset-game'});
    const key = op ? `${u.resetRevision || 0}_${daily ? 'daily_' + daily.dateKey : op.gameId}` : null;
    d.receipts ||= {};
    const saved = key && d.receipts[userId + '/' + key];
    if (saved) return {...saved, user:u, alreadySaved:true};
    // Existing pre-receipt daily results also block duplicate awards.
    if (daily && (u.completedDailyDates || [u.lastDailyDate, u.prevDailyDate]).includes(daily.dateKey)) {
      return {user:u, alreadySaved:true, points:0, breakdown:scoreBreakdown([],false,0), score:correct};
    }
    const result = prepareStatsUpdate(u, [answered,correct,points,daily,cats,recent,period,log], op);
    const receipt = {...result}; delete receipt.user;
    if (key) d.receipts[userId + '/' + key] = receipt;
    d.users[userId] = result.user; this._save(d); return result;
  }
  async saveRecentQuestionIds(userId, ids, log) {
    const d = this._load(), u = d.users[userId];
    u.recentQuestionIds = capSeenIds(u.recentQuestionIds || [], ids);
    if (log) u.gameLog = appendGameLog(u.gameLog, log);
    this._save(d);
  }
  async getDailyPins(date) {
    const entry = this._load().dailies?.[date];
    return Array.isArray(entry) ? entry : entry?.questionIds || null;
  }
  async getDailyQuestions(date) { return this._load().dailies?.[date]?.questions || null; }
  async claimDailyQuestions(date, candidates, pool) {
    const d = this._load(); d.dailies ||= {};
    if (!d.dailies[date]?.questions) d.dailies[date] = canonicalDaily(d.dailies[date], candidates, pool);
    this._save(d); return d.dailies[date].questions;
  }
  async saveDailyPins(date, ids) {
    const d = this._load(); d.dailies ||= {};
    if (!d.dailies[date]) { d.dailies[date] = ids; this._save(d); }
  }
  async claimDailyPins(date, ids) { await this.saveDailyPins(date,ids); return this.getDailyPins(date); }
  // Local dailies are already one small map, so they are the history.
  async getDailyHistory(since) {
    return mergeDailyHistory(since, Object.fromEntries(Object.entries(this._load().dailies || {})
      .map(([date, d]) => [date, Array.isArray(d) ? d : d.questionIds || []])));
  }
  async getHomeworkState() { return this._load().weeklyHomework || null; }
  async updateHomework(action, movies, week, at) {
    const d = this._load(); const next = mutateHomework(d.weeklyHomework,action,movies,week,at);
    d.weeklyHomework = next; this._save(d); return next;
  }
  async flagReport(report) { const d=this._load(); (d.flags ||= []).push(report); this._save(d); }
  async getFlags() { return this._load().flags || []; }
  async getLeaderboard(period = null) { return sortLeaderboard(await this.getUsers(),period); }
  _effectivePeriodPoints(u,k) { return effectivePeriodPoints(u,k); }
}

function canonicalDaily(existing, candidates, pool) {
  if (existing?.questions?.length) return existing;
  const ids = Array.isArray(existing) ? existing : existing?.questionIds;
  // Upgrade legacy ID-only records without changing their order or replacing a question.
  const questions = ids?.length ? ids.map(id => pool.find(q => q.id === id)) : candidates;
  if (!questions?.length || questions.some(q=>!q)) throw new Error('This older challenge is unavailable. Please try another game.');
  return {questionIds:questions.map(q=>q.id), questions:JSON.parse(JSON.stringify(questions))};
}
function sortLeaderboard(users, period) {
  if (period) return users.map(u=>({...u,effectivePeriodPoints:effectivePeriodPoints(u,period)}))
    .sort((a,b)=>b.effectivePeriodPoints-a.effectivePeriodPoints || a.name.localeCompare(b.name));
  return users.sort((a,b)=>(b.totalPoints||0)-(a.totalPoints||0)
    || (b.totalAnswered ? b.totalCorrect/b.totalAnswered : -1)-(a.totalAnswered ? a.totalCorrect/a.totalAnswered : -1)
    || a.name.localeCompare(b.name));
}

class FirebaseAdapter {
  constructor() { this.initialization=null; }
  async _initialize() {
    try {
      if(globalThis.loadFirebase) await globalThis.loadFirebase();
      else if(globalThis.firebaseReady) await globalThis.firebaseReady;
      if (typeof firebase === 'undefined') throw new Error('The online connection could not load. Check your connection or use offline practice.');
      if (!firebase.apps.length) firebase.initializeApp({
        apiKey:'AIzaSyC_keHyGc1Z46rzqB9wNKJ36wZgHscfGrQ', authDomain:'disneytrivia-38ac6.firebaseapp.com',
        projectId:'disneytrivia-38ac6', storageBucket:'disneytrivia-38ac6.firebasestorage.app',
        messagingSenderId:'817552679289', appId:'1:817552679289:web:1e82c3f0c72eeed2020fa8'
      });
      this.db = firebase.firestore();
      this.seedReady = this._seed(); this.seedReady.catch(()=>{});
    } catch (e) { return e; }
  }
  async _ready() {
    // A failed load is not permanent: clear it so the next call retries the CDN
    // (see bootstrap.js). Each caller checks the attempt it actually awaited.
    const attempt=this.initialization ||= this._initialize();
    const error=await attempt;
    if(error) { if(this.initialization===attempt) this.initialization=null; throw error; }
  }
  async _withTimeout(fn, {attempts=2,timeoutMs=8000}={}) {
    await this._ready(); let error;
    for(let i=0;i<attempts;i++) {
      let timer;
      try { return await Promise.race([Promise.resolve().then(fn),new Promise((_,reject)=>{
        timer=setTimeout(()=>reject(new Error('Request timed out. Check your connection.')),timeoutMs);
      })]); } catch(e) {error=e;} finally {clearTimeout(timer);}
    }
    throw error;
  }
  async _seed() {
    await Promise.all(['Kristen','Cara'].map(name=>this.db.runTransaction(async tx=>{
      const ref=this.db.collection('users').doc(name.toLowerCase()), snap=await tx.get(ref);
      if(!snap.exists) tx.set(ref,{id:name.toLowerCase(),name,totalAnswered:0,totalCorrect:0,gamesPlayed:0,totalPoints:0});
    })));
  }
  async getUsers() {
    return this._withTimeout(async()=>{
      await this.seedReady;
      return (await this.db.collection('users').get()).docs.map(d=>d.data());
    });
  }
  async saveUser(user) {
    await this._ready();
    // A normalized name claim prevents simultaneous devices creating duplicates.
    const claim=this.db.collection('playerNames').doc(encodeURIComponent(user.name.trim().toLowerCase()));
    await this.db.runTransaction(async tx=>{
      const s=await tx.get(claim);
      if(s.exists) throw new Error('Player already exists.');
      tx.set(claim,{userId:user.id}); tx.set(this.db.collection('users').doc(user.id),user);
    }); return user;
  }
  async updateStats(userId, answered, correct, points, daily, cats, recent, period, log, op) {
    await this._ready();
    if(!op?.gameId) throw new Error('A persistent game ID is required.');
    const ref=this.db.collection('users').doc(userId);
    const key=`${op.resetRevision || 0}_${daily ? 'daily_'+daily.dateKey : op.gameId}`;
    const receiptRef=ref.collection('games').doc(key);
    // Bounded so a stalled connection reports failure (and the app retries)
    // instead of "Saving…" forever. A timed-out transaction may still land; the
    // receipt makes the retry return it as already saved, never a second award.
    return this._withTimeout(()=>this.db.runTransaction(async tx=>{
      const [snap,saved]=await Promise.all([tx.get(ref),tx.get(receiptRef)]);
      if(!snap.exists) throw new Error('Player not found.');
      const u=snap.data();
      if((op.resetRevision||0)!==(u.resetRevision||0)) throw Object.assign(new Error('Scores were reset. Start a new game.'),{code:'reset-game'});
      if(saved.exists) return {...saved.data(),user:u,alreadySaved:true};
      if(daily && (u.completedDailyDates || [u.lastDailyDate,u.prevDailyDate]).includes(daily.dateKey)) {
        return {user:u,alreadySaved:true,points:0,breakdown:scoreBreakdown([],false,0),score:correct};
      }
      const result=prepareStatsUpdate(u,[answered,correct,points,daily,cats,recent,period,log],op);
      const receipt={...result}; delete receipt.user;
      tx.set(receiptRef,receipt); tx.update(ref,result.user); return result;
    }),{attempts:1,timeoutMs:20000});
  }
  async saveRecentQuestionIds(userId,ids,log) {
    await this._ready(); const ref=this.db.collection('users').doc(userId);
    await this.db.runTransaction(async tx=>{
      const snap=await tx.get(ref); if(!snap.exists) return;
      const u=snap.data(); const patch={recentQuestionIds:capSeenIds(u.recentQuestionIds||[],ids)};
      if(log) patch.gameLog=appendGameLog(u.gameLog,log);
      tx.update(ref,patch);
    });
  }
  async getDailyPins(date) {
    return this._withTimeout(async()=>{const s=await this.db.collection('dailies').doc(date).get();return s.exists?s.data().questionIds:null;});
  }
  async getDailyQuestions(date) {
    return this._withTimeout(async()=>{const s=await this.db.collection('dailies').doc(date).get();return s.exists?s.data().questions||null:null;});
  }
  // `history` ({since, days} from getDailyHistory) is optional. Recording it is
  // best effort and separate from the claim: meta/dailyHistory is only a cache
  // of dailies/*, and getDailyHistory refills any day it lacks.
  async claimDailyQuestions(date,candidates,pool,history=null) {
    const questions=await this._withTimeout(()=>this.db.runTransaction(async tx=>{
      const ref=this.db.collection('dailies').doc(date), s=await tx.get(ref);
      const old=s.exists?s.data():null;
      const canonical=canonicalDaily(old,candidates,pool);
      if(!old?.questions?.length) tx.set(ref,canonical);
      return canonical.questions;
    }));
    if(history) {
      await this._withTimeout(()=>this._recordDailyHistory(history.since,history.days,date,questions.map(q=>q.id)),
        {attempts:1,timeoutMs:5000}).catch(()=>{});
    }
    return questions;
  }
  // Stored entries win over new ones, so no existing day is ever rewritten
  // (the rules allow adding and pruning days only).
  async _recordDailyHistory(since,days,date,ids) {
    const ref=this.db.collection('meta').doc('dailyHistory');
    await this.db.runTransaction(async tx=>{
      const s=await tx.get(ref), stored=s.exists?s.data().days||{}:{};
      const next=mergeDailyHistory(since,stored,days,{[date]:ids});
      if(!s.exists || JSON.stringify(next)!==JSON.stringify(mergeDailyHistory('',stored))) tx.set(ref,{days:next});
    });
  }
  async saveDailyPins(date,ids) { return this.claimDailyPins(date,ids); }
  async claimDailyPins(date,ids) {
    return this._withTimeout(()=>this.db.runTransaction(async tx=>{
      const ref=this.db.collection('dailies').doc(date),s=await tx.get(ref);
      if(s.exists) return s.data().questionIds;
      tx.set(ref,{questionIds:ids});return ids;
    }));
  }
  // Daily pins from `since` up to (not including) `before`, as {date: [ids]}.
  // Reads the small meta/dailyHistory cache, then fills gaps from dailies/*
  // directly: a few missing days one by one, many (first run, or an old app
  // version pinned days without recording them) with one query. Days with no
  // pin are recorded as [] so they aren't re-read. Throws if the pins can't be
  // read; the caller must not pick a new daily without them.
  async getDailyHistory(since,before) {
    return this._withTimeout(async()=>{
      let stored={};
      try { const s=await this.db.collection('meta').doc('dailyHistory').get(); stored=s.exists?s.data().days||{}:{}; }
      catch(e) { /* a missing or unreadable cache only means more reads below */ }
      let days=mergeDailyHistory(since,stored);
      const missing=missingHistoryDates(days,since,before);
      if(missing.length>14) {
        const s=await this.db.collection('dailies').where(firebase.firestore.FieldPath.documentId(),'>=',since).get();
        days=mergeDailyHistory(since,days,Object.fromEntries(s.docs.map(d=>[d.id,d.data().questionIds||[]])));
      } else if(missing.length) {
        const docs=await Promise.all(missing.map(d=>this.db.collection('dailies').doc(d).get()));
        days=mergeDailyHistory(since,days,Object.fromEntries(docs.filter(d=>d.exists).map(d=>[d.id,d.data().questionIds||[]])));
      }
      return mergeDailyHistory(since,days,Object.fromEntries(missingHistoryDates(days,since,before).map(d=>[d,[]])));
    },{attempts:3,timeoutMs:10000});
  }
  async getHomeworkState() {
    return this._withTimeout(async()=>{const s=await this.db.collection('weeklyHomework').doc('state').get();return s.exists?s.data():null;});
  }
  async updateHomework(action,movies,week,at) {
    await this._ready();
    return this.db.runTransaction(async tx=>{
      const ref=this.db.collection('weeklyHomework').doc('state'),s=await tx.get(ref);
      const old=s.exists?s.data():null, next=mutateHomework(old,action,movies,week,at);
      if(JSON.stringify(old)!==JSON.stringify(next)) tx.set(ref,next);
      return next;
    });
  }
  async flagReport(report) { await this._ready(); await this.db.collection('flags').add(report); }
  async getFlags() { return this._withTimeout(async()=>(await this.db.collection('flags').get()).docs.map(d=>({_id:d.id,...d.data()}))); }
  async getLeaderboard(period=null) {return sortLeaderboard(await this.getUsers(),period);}
  _effectivePeriodPoints(u,k) {return effectivePeriodPoints(u,k);}
}

const storage = new FirebaseAdapter();
