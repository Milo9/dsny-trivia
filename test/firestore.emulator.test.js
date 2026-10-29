const {test,before,after,beforeEach}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {initializeTestEnvironment,assertFails,assertSucceeds}=require('@firebase/rules-unit-testing');
const firebase=require('firebase/compat/app');require('firebase/compat/firestore');
const L=require('../game-logic.js');const {scoreReset}=require('../data-logic.js');
const project='demo-disney-trivia';
let env,adapter,db;
const question={id:1,question:'Question?',answers:['A','B','C','D'],category:'movies',difficulty:'easy'};
before(async()=>{
  assert.ok(process.env.FIRESTORE_EMULATOR_HOST,'Run through npm run test:emulator; never use production.');
  const [host,port]=process.env.FIRESTORE_EMULATOR_HOST.split(':');
  env=await initializeTestEnvironment({projectId:project,firestore:{host,port:Number(port),rules:fs.readFileSync('firestore.rules','utf8')}});
  firebase.initializeApp({projectId:project,apiKey:'demo-key'});
  db=firebase.firestore();db.useEmulator(host,Number(port));
});
beforeEach(async()=>{
  await env.clearFirestore();
  // Run production code in this realm: the SDK intentionally rejects objects
  // constructed in a separate VM realm as custom class instances.
  const source=['game-logic.js','data-logic.js','storage.js'].map(file=>fs.readFileSync(file,'utf8')).join('\n');
  adapter=new Function('firebase','module','require',source+'\nreturn storage;')(firebase,undefined,undefined);
  await adapter.getUsers();
});
after(async()=>{if(db)await db.terminate();if(env)await env.cleanup();if(firebase.apps.length)await firebase.app().delete();});
function submit(id='a',daily=false,revision=0,date='2026-10-29') {
  const answers=[{question,correct:true,selectedText:'A'}];
  return adapter.updateStats('kristen',1,1,0,daily?{dateKey:date,answers:L.serializeAnswers(answers)}:null,
    L.buildCatStats(answers),[1],date.slice(0,7),{mode:daily?'daily':'regular',status:'complete',points:0},
    {gameId:id,resetRevision:revision,dateKey:date,answers,complete:true});
}
test('real transactions deduplicate simultaneous regular submissions and later retries',async()=>{
  await Promise.all([submit(),submit()]);await submit();
  const u=(await db.collection('users').doc('kristen').get()).data();
  assert.equal(u.gamesPlayed,1);assert.equal(u.totalAnswered,1);assert.equal(u.totalPoints,600);
});
test('real transactions award a concurrent daily from two devices exactly once',async()=>{
  const results=await Promise.all([submit('device-a',true),submit('device-b',true)]);
  const u=(await db.collection('users').doc('kristen').get()).data();
  assert.equal(u.gamesPlayed,1);assert.equal(u.totalPoints,810);assert.equal(u.dailyStreak,1);
  assert.equal(results.filter(r=>r.alreadySaved).length,1);
});
test('late daily credits its captured month without overwriting the latest daily',async()=>{
  await submit('new',true,0,'2026-11-01');await submit('old',true,0,'2026-10-31');
  const u=(await db.collection('users').doc('kristen').get()).data();
  assert.equal(u.lastDailyDate,'2026-11-01');assert.equal(u.prevDailyDate,'2026-10-31');
  assert.equal(u.monthlyTotals['2026-10'],810);assert.equal(u.monthlyTotals['2026-11'],810);
});
test('rules reject corrupt counters, unexpected fields, deletes, and receipt replacement',async()=>{
  await submit();const user=db.collection('users').doc('kristen');
  await assertFails(user.update({totalPoints:-1}));await assertFails(user.update({unexpected:'bad'}));
  await assertFails(user.delete());await assertFails(user.collection('games').doc('0_a').update({points:99}));
  await assertFails(db.collection('unknown').doc('x').set({data:true}));
});
test('immutable daily snapshots survive competing creators and reject replacement',async()=>{
  const a=Array.from({length:10},(_,i)=>({...question,id:i+1}));
  const b=a.map(q=>({...q,id:q.id+10}));
  const [one,two]=await Promise.all([adapter.claimDailyQuestions('2026-10-29',a,a),adapter.claimDailyQuestions('2026-10-29',b,b)]);
  assert.deepEqual(Array.from(one,q=>q.id),Array.from(two,q=>q.id));
  await assertFails(db.collection('dailies').doc('2026-10-29').set({questionIds:b.map(q=>q.id),questions:b}));
});
test('legacy ID-only pins can be upgraded once without changing the IDs',async()=>{
  const qs=Array.from({length:10},(_,i)=>({...question,id:i+1}));
  await env.withSecurityRulesDisabled(async ctx=>{
    await ctx.firestore().collection('dailies').doc('2026-10-29').set({questionIds:qs.map(q=>q.id)});
  });
  const r=await adapter.claimDailyQuestions('2026-10-29',[],qs);
  assert.equal(r.length,10);assert.equal(r[0].id,1);
  await assertFails(db.collection('dailies').doc('2026-10-29').update({questions:[]}));
});
test('transactional homework changes merge against fresh server history',async()=>{
  const movies=[{id:1},{id:2},{id:3}];
  await adapter.updateHomework({type:'refresh'},movies,'2026-10-29','2026-10-29');
  await Promise.all([adapter.updateHomework({type:'watch'},movies,'2026-10-29','2026-10-29'),
    adapter.updateHomework({type:'unwatch',movieId:99},movies,'2026-10-29','2026-10-29')]);
  assert.equal((await adapter.getHomeworkState()).watched.length,1);
});
test('reset snapshot is immutable and old game revisions cannot restore reset points',async()=>{
  await submit();const ref=db.collection('users').doc('kristen'),backup=ref.collection('backups').doc('reset');
  await db.runTransaction(async tx=>{const s=await tx.get(ref);tx.set(backup,{at:'2026-10-29',user:s.data()});tx.set(ref,scoreReset(s.data()));});
  await assertFails(backup.update({at:'changed'}));await assertFails(backup.delete());
  await assert.rejects(submit('old',false,0),e=>e.code==='reset-game');
  await assertSucceeds(submit('new',false,1));
  assert.equal((await ref.get()).data().gamesPlayed,1);
});
test('flag schema rejects markup in enums and accepts normal reports',async()=>{
  const report={questionId:1,questionText:'Q?',correctAnswer:'A',allAnswers:['A','B','C','D'],
    category:'movies',difficulty:'easy',reportedBy:'Kristen',comment:null,timestamp:'2026-10-29T12:00:00Z'};
  await assertSucceeds(adapter.flagReport(report));
  await assertFails(adapter.flagReport({...report,category:'<img onerror=alert(1)>'}));
});
