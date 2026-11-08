import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def read(p): return json.loads((R/p).read_text(encoding='utf-8'))
def command(*a): subprocess.run([sys.executable,'scripts/question_audit.py',*a],cwd=R,check=True)
reasons={
 'duplicate-1ea2d3f112d55b04fca9':'Independent composer credits for Zootopia and Up; knowing one film score does not establish who scored the other.',
 'duplicate-5e4f78bf56655957a1f8':'Slinky spring-body rescue and RC remote-car rescue are separate toy identities and actions. Both help, but stretchy versus remote-control makes the answers exclusive.',
 'duplicate-f27ba23a6878ef644716':'Disgust green and Joy yellow are independent character-color mappings. One mapping does not establish the other; other characters and colors exist.',
 'leak-c42fd93452c6375a1bb0':'Wish is the necessary film title, and all four answers are songs from Wish. Removed the redundant wishes verb; film identity alone does not identify this specific Asha solo.',
}
plan=read('audit/runs/next-shard-0024-plan.json'); scope=set(plan['questionIds'])
fs=[f for f in read('artifacts/question-audit.json')['openFindings'] if scope.intersection(f['questionIds'])]
assert {f['id'] for f in fs}==set(reasons), 'Inspect new applicable findings.'
c={q['id']:q for p in (R/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf-8'))}
out='audit/runs/next-shard-0024-finding-decisions.json'
(R/out).write_text(json.dumps([dict(finding=f,reason=reasons[f['id']],questions=[c[i] for i in f['questionIds']],reviewer='Codex',at='2026-11-08') for f in fs],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in fs: command('decide',f['id'],'accepted','--reviewer','Codex','--reason',reasons[f['id']],'--reference',out)
edits={
1256:('clarification','Identify first cave summons, excluding the later Prince Ali performance.'),
1258:('clarification','Specify the 1996 film and Esmeralda cathedral prayer.'),
1260:('clarification','Specify 1998 animated film and the marching sequence rather than training.'),
1263:('clarification','Identify mammoth travel montage and avoid implying Collins is its sole singing voice.'),
1264:('clarification','Identify early farm introduction rather than any song about home.'),
1268:('clarification','Identify the super-suit training montage rather than any soundtrack placement.'),
1269:('clarification','Date Zootopia to the original 2016 film.'),
1270:('clarification','Supply missing film and year; identify Asha solo without repeating wishes.'),
1272:('clarification','Both Atta and Dot are princesses; ask which is preparing to succeed the Queen.'),
1274:('clarification distractors','Ask the name of the chameleon mechanism; replace overlapping invisibility wording with distinct mechanisms.'),
1275:('clarification','Ask for the adult turtle carrying Marlin; Squirt also helps the travellers under the old wording.'),
1278:('clarification','Specify Linguini arrival, before Skinner loses control of the restaurant.'),
1279:('clarification','Ask specifically for the planter and make all answers parallel noun phrases, excluding nested collection storage.'),
1291:('clarification','Specify first attempted visitation and restored body part.'),
1295:('factual clarification','Remove unsupported instantaneous travel premise; ask which fuel Buzz tests to get the crew home.'),
}
t=read('audit/runs/next-shard-0024-active-template.json')
actual={r['questionId'] for r in t['reviews'] if r['hash']!=plan['startingHashes'][str(r['questionId'])]}
assert actual==set(edits)
for i,(kinds,reason) in edits.items():
    args=['classify',str(i)]
    for k in kinds.split(): args+=['--type',k]
    command(*args,'--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0024-reviews.json')
print('Decided',len(fs),'findings; classified',len(edits),'retained edits.')
