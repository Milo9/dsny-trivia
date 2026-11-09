"""Classify retained edits and save specific, hash-bound warning comparisons."""
import json
import subprocess
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def command(*args):
    for attempt in range(5):
        result=subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True)
        if result.returncode==0:return
        if 'WinError 5' not in result.stdout+result.stderr:break
        time.sleep(0.5)
    raise RuntimeError(result.stdout+result.stderr)
plan=read('audit/runs/next-shard-0033-plan.json')
bank={q['id']:q for p in (ROOT/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf-8'))}
ref='audit/runs/next-shard-0033-reviews.json'
changes=read('audit/runs/next-shard-0033-changes.json')
existing=read('audit/ledger.json').get('changeClassifications',{})
for k,v in changes.items():
    i=int(k)
    if i not in bank:continue
    if existing.get(k,{}).get('types')==v['types']:continue
    opts=[x for t in v['types'] for x in ('--type',t)]
    command('classify',i,*opts,'--reviewer','Codex','--reason',v['reason'],'--reference',ref)
decisions={
'duplicate-4c8c167434d4f8c1e8b8':'Different works and facts: Cinderella 1950 animation production history versus the live-action Cinderella 2015 theatrical pairing with Frozen Fever. The shared short title does not establish the pairing.',
'duplicate-5ecd68e0ce9b1f6e44e4':'Different original English cast assignments: Tina Fey as Soul 22 versus Julia Louis-Dreyfus as Onward Laurel. Memorizing either credit does not identify the other role.',
'duplicate-8348d148246a36242230':'An actual Frida Kahlo cameo helping stage a performance and Héctor impersonating her at the departures checkpoint are separate actions by separate characters. The cameo alone does not establish the disguise; both scenes were inspected.',
'duplicate-b24fe42ecf3063375e09':'Different original English cast assignments: Jamie Foxx as Soul Joe versus Julia Louis-Dreyfus as Onward Laurel. Similar question structure is not a duplicate credit.',
'duplicate-dbf41ec7a88227b72dd9':'Kristoff being an ice harvester in Frozen does not establish Elsa explicitly delegates the courtyard to him in the different short Frozen Fever. Different role and event.',
'duplicate-e0b7801e475f5791fc3d':'Coco plaza-performance song identity/translation and a later Magic Kingdom attraction update require distinct knowledge. Knowing a song is in Coco does not show it was chosen for PhilharMagic.',
'leak-6adb6857bd15078da18a':'Adventure Book is the identifying prop name. It does not state the final note or tell the player whether Ellie encourages a new adventure, returning home, preserving belongings or rejecting Russell. The note passage establishes the chosen interpretation.',
'leak-7ee64969fba9c8adbae7':'Nita names the subject whose future is at stake, not which character is transformed or into what. Kenai restoration is a plausible competing story proposal that the ending expressly rejects.',
'leak-c95c7cb0215728d6f6dc':'The stem contains the ordinary preposition under in race under, not the answer Underdogs. It supplies neither dogs nor the team name; all four possible team names remain grammatical.'
}
report=read('artifacts/question-audit.json')
applicable=[f for f in report['openFindings'] if any(i in plan['questionIds'] for i in f['questionIds'])]
assert {f['id'] for f in applicable}==set(decisions), [f['id'] for f in applicable]
comparison={'reviewer':'Codex','at':'2026-11-09','scope':plan['questionIds'],
 'findings':[dict(f,comparisonQuestions=[bank[i] for i in f['questionIds']],rationale=decisions[f['id']]) for f in applicable],
 'additionalComparisons':[
  {'questionIds':[2208,2324],'questions':[bank[i] for i in [2208,2324]],'rationale':'Prize item and the mechanism of winning are separate facts. 2324 retains a reversed-persona premise and is tracked as manual-3b00745a4acea7907790, outside this batch; it was not approved or edited.'},
  {'questionIds':[2199,2098],'questions':[bank[i] for i in [2199,2098]],'rationale':'Papi name versus successful home/family life Kronk pretends to have; different factual targets.'},
  {'questionIds':[2185,2188],'questions':[bank[i] for i in [2185,2188]],'rationale':'Segment title versus the assigned banquet task; a title does not supply the task.'},
  {'questionIds':[2202,2203],'questions':[bank[i] for i in [2202,2203]],'rationale':'Bambi headbutting practice and his father blowing a raspberry are different actions, despite being in the same play scene.'},
  {'questionIds':[2211,1401],'questions':[bank[i] for i in [2211,1401]],'rationale':'Independently rechecked existing accepted comparison: Bao and Turning Red are separate Toronto-set works.'}],
 'retirementReference':'audit/runs/next-shard-0033-comparison-2196-2198.json',
 'scopeLimitations':'No connected production flag export was available locally. Player flags were not changed or resolved. Detailed secondary text corroboration was used where primary scene playback was unavailable; limitations are embedded in source notes.'}
comparison_ref='audit/runs/next-shard-0033-comparisons.json'
(ROOT/comparison_ref).write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in applicable:command('decide',f['id'],'accepted','--reviewer','Codex','--reason',decisions[f['id']],'--reference',comparison_ref)
print('Classified',len(changes)-1,'retained edits and decided',len(applicable),'applicable findings.')
