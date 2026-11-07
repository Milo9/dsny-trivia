"""Explicit final finding decisions and retained-edit classifications."""
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def run(*a):
    p=subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,a)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    print(' '.join(map(str,a[:3])),p.returncode,p.stdout.strip()[-180:])
    if p.returncode:raise RuntimeError(p.stderr+p.stdout)
decisions={
'duplicate-43bf229196226bc8bf5c':'Luisa and Bob are different characters in different films. Knowing Luisa has strength does not establish Bob has it.',
'duplicate-63bc70033647aaac85f9':'22 is a career Oscar count in q123 and an individual soul identifier in q661. No shared fact or inference connects them.',
'duplicate-7b969034443a1ee891ef':'q90 identifies a current Magic Kingdom ride from its singing children. q692 independently tests the 1964 Pepsi-Cola/UNICEF sponsorship and fair presentation. Shared attraction identity alone does not establish that historical connection.',
'duplicate-ac7d6106688044a5ef1c':'First posthumous release is a chronological event; last personally supervised production is a separate relationship. The feature catalog establishes the former, and the D23 production account the latter; neither necessarily implies the other.',
'duplicate-d71679f0b4aae952634a':'q609 identifies the haunted elevator at Hollywood Studios. q1160 asks the predecessor of Mission BREAKOUT in California. Distinct park version and replacement history require a new fact.',
'duplicate-f431c3816868a941386e':'Rose paint in Alice and McQueen\'s classic car livery have unrelated causes and subjects. Sharing red does not make them duplicates.',
'leak-0c1ee0a248c637d613e9':'All four options are real coaster names. The generic word coaster identifies their common ride type; the discriminating information is the 1999 Aerosmith debut, not a copied answer title.',
'scope-668deebbfe9b915e315b':'Alice Comedies are silent theatrical film shorts made in the 1920s, not a television series. Final question explicitly says theatrical shorts; secondary-film coverage remains modest.'}
report=read('artifacts/question-audit.json')
scope=set(read('audit/runs/next-shard-0012-plan.json')['questionIds'])
applies=[f for f in report['openFindings'] if scope.intersection(f['questionIds'])]
assert {f['id'] for f in applies}==set(decisions)
record=[]
for f in applies:
    record.append(dict(finding=f,reason=decisions[f['id']],reviewer='Codex',reference='audit/runs/next-shard-0012-evidence-notes.json'))
(ROOT/'audit/runs/next-shard-0012-finding-decisions.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in applies:run('decide',f['id'],'accepted','--reviewer','Codex','--reason',decisions[f['id']],'--reference','audit/runs/next-shard-0012-finding-decisions.json')
types={600:['clarification'],609:['clarification'],619:['clarification','distractors','difficulty'],620:['clarification'],623:['clarification','distractors'],624:['clarification','distractors'],634:['clarification'],636:['clarification'],638:['clarification','distractors'],640:['factual','clarification','distractors','difficulty'],647:['clarification','distractors','difficulty'],648:['clarification','distractors'],656:['difficulty'],657:['clarification','difficulty'],659:['difficulty'],661:['difficulty'],663:['difficulty'],664:['distractors','difficulty'],680:['clarification'],682:['factual','clarification','distractors','difficulty'],688:['clarification','distractors'],692:['clarification'],693:['clarification','distractors'],695:['factual','clarification','distractors','difficulty']}
reasons={640:'Corrected the electricity premise to the collected scream-energy source, eliminated overlapping powered systems and specified the opening state.',682:'Corrected first-studio claim to first Hollywood studio, isolated numeric suffix meaning, and made options parallel.',695:'Removed Project X, which was also a true planning pseudonym, and fixed the event to the November 1965 public announcement.'}
for i,ts in types.items():
    args=['classify',i]
    for t in ts:args+=['--type',t]
    run(*args,'--reviewer','Codex','--reason',reasons.get(i,'Final reviewed wording clarifies the precise context or removes option overlap/giveaways; named-role recall difficulty calibrated where recorded. See the question-specific final challenge.'),'--reference','audit/runs/next-shard-0012-evidence-notes.json')
