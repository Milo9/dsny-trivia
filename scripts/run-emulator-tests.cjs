const fs=require('node:fs');
const path=require('node:path');
const {spawnSync}=require('node:child_process');
const root=path.resolve(__dirname,'..');
const env={...process.env,FIREBASE_CLI_DISABLE_TELEMETRY:'1',FIREBASE_EMULATORS_PATH:path.join(root,'.tools','firebase')};
const portable=path.join(root,'.tools','jre');
if(process.platform==='win32' && fs.existsSync(portable)) {
  const folder=fs.readdirSync(portable).find(name=>fs.existsSync(path.join(portable,name,'bin','java.exe')));
  if(folder) {
    env.JAVA_HOME=path.join(portable,folder);
    const pathKey=Object.keys(env).find(key=>key.toLowerCase()==='path') || 'PATH';
    env[pathKey]=path.join(env.JAVA_HOME,'bin')+path.delimiter+(env[pathKey] || '');
  }
}
const cli=path.join(root,'node_modules','firebase-tools','lib','bin','firebase.js');
const result=spawnSync(process.execPath,[cli,'emulators:exec','--only','firestore','--project','demo-disney-trivia',
  `"${process.execPath}" --test test/firestore.emulator.test.js`],{cwd:root,env,stdio:'inherit'});
if(result.error)console.error(result.error.message);
process.exit(result.status ?? 1);
