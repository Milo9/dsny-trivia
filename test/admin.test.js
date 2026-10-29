const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const {validPlayerBackup}=require('../data-logic.js');
function admin() {
  const clone=x=>x===undefined?undefined:JSON.parse(JSON.stringify(x));
  const original={id:'kristen',name:'Kristen',totalAnswered:10,totalCorrect:7,gamesPlayed:1,totalPoints:1200,
    monthlyKey:'2026-10',monthlyPoints:1200,prevMonthlyKey:'2026-09',prevMonthlyPoints:300,
    monthlyTotals:{'2026-10':1200,'2026-09':300},resetRevision:0};
  const data=new Map([['users/kristen',clone(original)],['dailies/2026-10-29',{questionIds:[1]}],['flags/f',{comment:'test'}]]);
  const listeners=new Map(), elements=new Map();let serial=0;
  const doc=path=>({id:path.split('/').at(-1),collection:name=>collection(path+'/'+name),
    get:async()=>({id:path.split('/').at(-1),ref:doc(path),exists:data.has(path),data:()=>clone(data.get(path))}),
    set:async value=>{data.set(path,clone(value));},update:async patch=>{data.set(path,{...data.get(path),...clone(patch)});}});
  const collection=path=>({doc:id=>doc(path+'/'+(id || 'generated-'+(++serial))),orderBy:()=>collection(path),limit:()=>collection(path),
    get:async()=>{const docs=await Promise.all([...data.keys()].filter(k=>k.startsWith(path+'/') && k.split('/').length===path.split('/').length+1).map(k=>doc(k).get()));
      docs.sort((a,b)=>(b.data().at||'').localeCompare(a.data().at||''));return {docs,empty:!docs.length};}});
  const db={collection,runTransaction:async fn=>fn({get:ref=>ref.get(),set:(ref,value)=>ref.set(value),update:(ref,value)=>ref.update(value)})};
  const firestore=()=>db;firestore.FieldValue={delete:()=>null};
  const context=vm.createContext({console,Date,Set,Map,Promise,setTimeout,clearTimeout,confirm:()=>true,
    firebase:{initializeApp(){},firestore},window:{addEventListener(){}},
    document:{getElementById:id=>{if(!elements.has(id))elements.set(id,{textContent:'',innerHTML:'',addEventListener:(event,fn)=>listeners.set(id+':'+event,fn)});return elements.get(id);}},
    Blob,URL,fetch:async()=>({json:async()=>({shards:[]})})});
  for(const file of ['game-logic.js','data-logic.js'])vm.runInContext(fs.readFileSync(require.resolve('../'+file),'utf8'),context);
  const html=fs.readFileSync(require.resolve('../review.html'),'utf8');
  let script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
  script=script.slice(0,script.indexOf("window.addEventListener('unhandledrejection'"));
  vm.runInContext(script,context);
  vm.runInContext('downloadJSON=(value,name)=>{globalThis.downloaded={value,name};}',context);
  return {data,context,original,listeners,run:code=>vm.runInContext(code,context)};
}
test('actual admin reset clears monthly points and undo restores the pre-reset snapshot',async()=>{
  const a=admin();await a.run('loadUsers()');await a.run('resetUser(0)');
  assert.equal(a.data.get('users/kristen').monthlyPoints,0);assert.equal(a.data.get('users/kristen').resetRevision,1);
  assert.equal([...a.data.keys()].filter(k=>k.startsWith('users/kristen/backups/')).length,1);
  await a.run('restoreLastReset(0)');
  assert.equal(a.data.get('users/kristen').totalPoints,a.original.totalPoints);
  assert.equal(a.data.get('users/kristen').monthlyPoints,1200);assert.equal(a.data.get('users/kristen').resetRevision,2);
});
test('actual admin export includes users, daily pins, flags and receipts',async()=>{
  const a=admin();await a.run('downloadBackup()');
  const backup=a.context.downloaded.value;
  assert.equal(backup.schema,1);assert.equal(backup.users[0].id,'kristen');
  assert.equal(backup.dailies.length,1);assert.equal(backup.flags.length,1);assert.ok(backup.games.kristen);
});
test('actual file restore backs up current stats, invalidates checkpoints and preserves pins',async()=>{
  const a=admin();const backup={schema:1,at:'2026-10-29',users:[{...a.original,totalPoints:800}]};
  await a.listeners.get('restore-file:change')({target:{files:[{size:100,text:async()=>JSON.stringify(backup)}],value:'file'}});
  assert.equal(a.data.get('users/kristen').totalPoints,800);assert.equal(a.data.get('users/kristen').resetRevision,1);
  assert.equal(a.data.get('dailies/2026-10-29').questionIds[0],1);
  assert.equal([...a.data.keys()].filter(k=>k.startsWith('users/kristen/backups/')).length,1);
});
test('invalid nested stats and duplicate players are rejected before any restore write',async()=>{
  const a=admin();assert.equal(validPlayerBackup({...a.original,monthlyTotals:{'2026-10':'<script>'}}),false);
  const before=JSON.stringify([...a.data]);const backup={schema:1,users:[a.original,a.original]};
  await a.listeners.get('restore-file:change')({target:{files:[{size:100,text:async()=>JSON.stringify(backup)}],value:'file'}});
  assert.equal(JSON.stringify([...a.data]),before);
});
