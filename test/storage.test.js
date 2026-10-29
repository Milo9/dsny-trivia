const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const {scoreReset,prepareStatsUpdate,mutateHomework,effectivePeriodPoints}=require('../data-logic.js');
function adapter() {
  const data=new Map();
  const context=vm.createContext({console,Date,Math,Set,Map,Promise,setTimeout,clearTimeout,
    localStorage:{getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)}});
  for(const file of ['game-logic.js','data-logic.js','storage.js']) vm.runInContext(fs.readFileSync(require.resolve('../'+file),'utf8')
    .replace('const storage = new FirebaseAdapter();','globalThis.storage = new LocalStorageAdapter();'),context);
  return context.storage;
}
const question={id:10,question:'Q?',answers:['A','B','C','D'],difficulty:'easy',category:'movies'};
function submit(s,{daily=false,date='2026-10-29',id='game-a',revision=0,correct=true}={}) {
  const answers=[{question,selectedText:correct?'A':'B',correct}];
  return s.updateStats('kristen',1,Number(correct),0,daily?{dateKey:date,answers:serializeAnswers(answers)}:null,
    buildCatStats(answers),[10],date.slice(0,7),{mode:daily?'daily':'regular',status:'complete',points:0},
    {gameId:id,resetRevision:revision,dateKey:date,answers,complete:true});
}
test('a retry after a lost response returns the receipt without applying stats twice',async()=>{
  const s=adapter();const first=await submit(s),retry=await submit(s);
  assert.equal(retry.alreadySaved,true);assert.equal(retry.user.gamesPlayed,1);assert.equal(retry.points,first.points);
});
test('two device game ids for the same daily award stats and bonus once',async()=>{
  const s=adapter();const [a,b]=await Promise.all([submit(s,{daily:true,id:'device-a'}),submit(s,{daily:true,id:'device-b'})]);
  assert.equal(b.alreadySaved,true);assert.equal(b.user.totalAnswered,1);assert.equal(a.points,b.points);
});
test('daily completion uses its captured date and month, even after rollover',async()=>{
  const s=adapter();const r=await submit(s,{daily:true,date:'2026-09-30'});
  assert.equal(r.user.lastDailyDate,'2026-09-30');assert.equal(r.user.monthlyKey,'2026-09');
});
test('late games credit their own month without corrupting newer totals',async()=>{
  const s=adapter();await submit(s,{id:'new',date:'2026-11-01'});const r=await submit(s,{id:'old',date:'2026-10-31'});
  assert.equal(r.user.monthlyKey,'2026-11');assert.equal(effectivePeriodPoints(r.user,'2026-10'),600);
  assert.equal(effectivePeriodPoints(r.user,'2026-11'),600);
});
test('late daily completion preserves newer review slots and repairs a streak gap',async()=>{
  const s=adapter();await submit(s,{daily:true,date:'2026-10-27'});await submit(s,{daily:true,date:'2026-10-29'});
  const r=await submit(s,{daily:true,date:'2026-10-28'});
  assert.equal(r.user.lastDailyDate,'2026-10-29');assert.equal(r.user.prevDailyDate,'2026-10-28');assert.equal(r.user.dailyStreak,3);
});
test('score reset clears monthly scores and invalidates old checkpoints',async()=>{
  const s=adapter();const r=await submit(s);const d=s._load();d.users.kristen=scoreReset(r.user);s._save(d);
  assert.equal(effectivePeriodPoints(d.users.kristen,'2026-10'),0);
  await assert.rejects(submit(s),e=>e.code==='reset-game');
  const fresh=await submit(s,{id:'fresh',revision:1});assert.equal(fresh.user.gamesPlayed,1);
});
test('per-question attempts and missed ids accumulate and correct answers clear misses',async()=>{
  const s=adapter();let r=await submit(s,{correct:false});assert.deepEqual(Array.from(r.user.missedQuestionIds),[10]);
  r=await submit(s,{id:'second'});assert.equal(r.user.missedQuestionIds.length,0);assert.equal(r.user.questionStats[10].answered,2);
});
test('recent history merges across devices without duplicate ids',async()=>{
  const s=adapter();await s.saveRecentQuestionIds('kristen',[1,2]);await s.saveRecentQuestionIds('kristen',[2,3]);
  assert.deepEqual(Array.from((await s.getUsers()).find(u=>u.id==='kristen').recentQuestionIds),[1,2,3]);
});
test('published daily snapshots survive content removal and competing candidates',async()=>{
  const s=adapter();const qs=Array.from({length:10},(_,i)=>({...question,id:i+1}));
  const first=await s.claimDailyQuestions('2026-10-29',qs,qs);
  const again=await s.claimDailyQuestions('2026-10-29',[{...question,id:99}],[]);
  assert.equal(again.length,10);assert.equal(again[0].id,first[0].id);
});
test('legacy pins migrate in order and missing ids never get private replacements',async()=>{
  const s=adapter();await s.saveDailyPins('2026-10-29',[10]);
  await assert.rejects(s.claimDailyQuestions('2026-10-29',[question],[]));
  const qs=await s.claimDailyQuestions('2026-10-29',[question],[question]);assert.equal(qs[0].id,10);
});
test('homework updates preserve server history and rollover does not assume a watch',async()=>{
  const movies=[{id:1},{id:2},{id:3}];
  const old={weekKey:'2026-10-22',movieId:1,pickedAt:'2026-10-22',watched:[{id:2,watchedAt:'2026-10-20'}]};
  const next=mutateHomework(old,{type:'refresh'},movies,'2026-10-29','2026-10-29',()=>0);
  assert.deepEqual(next.watched,old.watched);assert.equal(next.movieId,3);
  const watched=mutateHomework(next,{type:'watch'},movies,'2026-10-29','2026-10-29');
  assert.equal(watched.watched.length,2);assert.equal(old.watched.length,1);
});
module.exports={adapter,question};
