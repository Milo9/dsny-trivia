"""Classify final edits and record the explicit final duplicate comparisons."""
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def save(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def command(*a):
    for attempt in range(5):
        p=subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,a)],cwd=ROOT,capture_output=True,text=True)
        if not p.returncode:return
        if 'WinError 5' not in p.stdout+p.stderr:break
        time.sleep(0.5)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
plan=read('audit/runs/next-shard-0034-plan.json')
bank={q['id']:q for p in (ROOT/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf-8'))}
before=read('artifacts/question-audit/current-compact.json')['catalog']
changes={
2218:(['clarification','distractors'],'Bound song identity to the 1964 debut and replace a near-identical title option.'),
2219:(['factual','clarification'],'Replace unsupported keyed precision with Disney\'s approximately 50-foot advertised figure; specify measurement basis.'),
2220:(['clarification','difficulty'],'Remove definition supplying trackless and calibrate technology recall to medium.'),
2221:(['clarification'],'Specify English and official 2008 reopening; 2007 was the preview period, not an error to count as factual.'),
2226:(['factual','clarification'],'Replace wrong keyed threshold and unsupported construction motive with documented castle height.'),
2229:(['clarification'],'Specify California and remove unnecessary opening-interval premise.'),
2234:(['clarification','distractors'],'Remove old Gadget name clue and normalize final coaster title.'),
2237:(['clarification'],'Ask seat capacity instead of asserting every dispatch holds six riders.'),
2239:(['clarification'],'Specify that only a section of Paradise Pier was replaced.'),
2246:(['clarification'],'Remove unnecessary first/largest marketing comparison.'),
2249:(['clarification'],'Distinguish Power Run from the Florida counterpart; remove park-opening-year clue.'),
2255:(['clarification','distractors','difficulty'],'Replace unbalanced French titles with parallel princess identities; medium recall.'),
2256:(['clarification','distractors'],'Use an individual park and a historical opening event; remove resort/park mismatch.'),
2257:(['factual','clarification','distractors'],'Remove false unique multi-princess-castle premise and use parallel tribute groups.'),
2258:(['clarification','difficulty'],'Replace unsupported global size ranking with dated primary fact-sheet area; hard numeric recall.'),
2262:(['clarification','distractors'],'Bambi also was in production; alternatives now are already-released features and no exclusivity across all films is claimed.'),
2263:(['difficulty'],'Exact launch-day recall is hard rather than easy.'),
2267:(['factual','clarification'],'Remove false universal claim excluding women from other departments; ask documented cel-finishing work.')}
ref='audit/runs/next-shard-0034-reviews.json'
saved={}
for i,(types,reason) in changes.items():
    assert bank[i]!=before[str(i)]
    saved[str(i)]=dict(types=types,reason=reason,before=before[str(i)],after=bank[i])
    command('classify',i,*[x for t in types for x in ('--type',t)],'--reviewer','Codex','--reason',reason,'--reference',ref)
save('audit/runs/next-shard-0034-changes.json',saved)
decisions={
'duplicate-084fdfcd1d2c729a6220':'The 2002 park-opening name does not locate the Ratatouille ride within that park in 2014. These ask park identity at opening versus a later attraction location.',
'duplicate-446450362245f6798e05':'A geographic identification of Shanghai Disneyland does not establish that it received the original TRON coaster. Removed the 2016 clue that matched another park-opening question; attraction placement remains a new fact.',
'duplicate-5018cec32db8dadc1318':'Six passenger seats in a Racers vehicle and six Cosmic Rewind songs are unrelated counts. Neither supplies knowledge of the other object being counted.',
'duplicate-64ba3934d7a592e7227e':'Maleficent\'s film identity does not establish which princess Paris chose for its castle. A film villain and a park dedication are different relationships.',
'duplicate-667ec22c0362d7b7adcc':'Dumbo\'s economical production strategy does not establish that its production overlapped the strike. Retain the distinct labor-history relationship; the final wording does not assert that no other Disney film was in production.',
'duplicate-75790393d64a60cf9584':'Cars Land in California and Grizzly Gulch in Hong Kong are separate land openings. Their shared year 2012 is coincidental, not interchangeable evidence.',
'duplicate-978917e0e714fed1275d':'Remy and Rise of the Resistance are different attractions. Knowing one uses trackless vehicles does not establish the other\'s vehicle system.',
'duplicate-b09bb2af6d13e3520c10':'These are separately named boat attractions for different films. Knowing Rapunzel\'s Lantern Festival does not identify Anna and Elsa\'s Frozen Journey.',
'duplicate-b2e11fb7a687839ab02d':'A film\'s Super Technirama production technology does not establish the dedication of the Paris castle. Shared Sleeping Beauty answer is not the same fact.',
'duplicate-b8f6f95549a3af4d9b8a':'California Rise of the Resistance and Tokyo Enchanted Tale of Beauty and the Beast are separate opening events; coincidental year 2020 is not a duplicate fact.',
'duplicate-f714ca8307c77d5f303c':'December 2024 fleet size and seats in a California ride vehicle count different things. Knowing six ships gives no passenger-capacity evidence.',
'duplicate-f9e613f07188daadf8dd':'The resort opened in 2005 and a later land opened in November 2023. The later expansion date is not supplied by the resort-opening fact.',
'leak-8658e265a4441543c858':'Pixar Pier is the necessary named subject. Pier alone does not disclose the distinctive former name Paradise; final wording avoids implying the whole former land was replaced.',
'leak-9052586dac3786e9ac3d':'Frozen identifies the necessary film context; it does not supply the official area name Kingdom. Arendelle and North Mountain alternatives remain plausible settings until the actual area title is known.',
'leak-e706afb5bb7580068b26':'Company is an ordinary business noun, not the distinctive answer Jim Henson. The agreement specifically excludes Sesame Workshop\'s assets and identifies Henson as the seller.'}
report=read('artifacts/question-audit.json')
findings=[f for f in report['openFindings'] if set(f['questionIds'])&set(plan['questionIds'])]
assert {f['id'] for f in findings}==set(decisions)
comparison=dict(reviewer='Codex',at='2026-11-09',scope=plan['questionIds'],topicContext='Read complete combined parks, walt and ten related film digests, all four options per question. Cross-category shard search also completed.',findings=[dict(f,questions=[bank[i] for i in f['questionIds']],rationale=decisions[f['id']]) for f in findings],limitations='No current player-report export was present locally; live player reports could not be checked in this audit. No player reports were resolved. Pre-existing manual-3b00745a4acea7907790 on #2324 remains outside this fixed scope.')
cref='audit/runs/next-shard-0034-comparisons.json'
save(cref,comparison)
for f in findings:command('decide',f['id'],'accepted','--reviewer','Codex','--reason',decisions[f['id']],'--reference',cref)
print('Classified',len(changes),'edits and recorded',len(findings),'specific finding decisions.')
