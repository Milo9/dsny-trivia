"""Classify reviewed edits and record explicit batch 32 finding decisions."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from question_audit import digest

def command(*args):
    for attempt in range(5):
        result=subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True)
        if not result.returncode:
            return
        if 'WinError 5' not in result.stdout+result.stderr:
            break
        time.sleep(0.5)
    raise RuntimeError(result.stdout+result.stderr)

changes={
2118:('clarification distractors','Specified the 1960 film and replaced a gunpowder/fuse giveaway with parallel explosive-container choices.'),
2119:('clarification distractors','Removed tree-in-stem giveaway and unnecessary plumbing/skylight details; made all choices elevated homes.'),
2120:('clarification distractors','Removed unsupported near-bankruptcy rhetoric and made the causal alternatives explicit.'),
2121:('clarification distractors','Replaced an undated inflation-adjusted loss estimate with the documented development title.'),
2122:('clarification','Separated the California opening title from the later EPCOT attraction.'),
2123:('clarification','Removed an unnecessary last-Walt-project claim.'),
2124:('clarification','Specified the historical original show and used its documented song assignment instead of subjective tone-deafness.'),
2127:('factual clarification','Removed the false implication that the worthy entrant may claim the cave treasures.'),
2128:('factual clarification distractors','Replaced an incorrect eligibility/burial premise with the actual Abu ruby, lava and collapse scene.'),
2129:('factual clarification','Framed absence of traditions as the sisters initial belief; the ending reveals they already have one.'),
2130:('clarification','Removed Norway/Norwegian-roots hint from the question.'),
2131:('clarification distractors','Made family relationship options parallel and removed unsupported adoption scenario.'),
2132:('clarification distractors','Narrowed Owl characterization and replaced potentially overlapping Rabbit distractor.'),
2134:('factual clarification distractors category difficulty scope','Replaced a TV-series Pascal snake incident misattributed to the movie with the theatrical-film tear revival; moved to movies/medium.'),
2135:('clarification','Specified loss of healing power in the hair, preserving the separate tear revival.'),
2136:('clarification','Focused on live fawn origin and removed incidental studio-location language.'),
2138:('clarification','Specified the mother actual word instead of an unbounded all-animals/whenever claim.'),
2139:('clarification','Replaced vague causal influence with documented historical campaign succession.'),
2140:('factual clarification','Distinguished father as source of advice from mother as prompter and Thumper as on-screen speaker.'),
2141:('clarification distractors difficulty','Replaced ill-formed cycle wording with one season and four parallel seasonal answers; calibrated easy.'),
2144:('clarification','Distinguished a development working title from release title.'),
2146:('clarification distractors','Asked about auroral association of the spirit mountain rather than natural lights performing magic.'),
2148:('clarification','Removed U.S. clue against Canadian distractors and unnecessary closure date.'),
2149:('clarification','Focused on supported character-design attribution without compound job-title and style claims.'),
2150:('clarification category','Specified predominant musical influence rather than exclusivity; moved to music.'),
2151:('clarification','Bound the reference-feature answer to Goldberg specific recollection, avoiding broad simultaneous-reference possibilities.'),
2153:('factual clarification distractors','Corrected two to three heads in the Disney first-regrowth scene; used parallel numeric alternatives and distinguished monster-identification question 829.'),
2155:('clarification distractors','Replaced a record superlative with approximate nominal 1981 production budget.'),
2156:('clarification','Attributed the Vixey assignment to Keane firsthand recollection and removed unnecessary uncredited/acclaimed claims.'),
2157:('clarification','Used the documented historical Pixar leadership role instead of co-founder shorthand.'),
2159:('factual clarification','Replaced motion-capture/MIDI characterization with documented filmed hand reference for frame-by-frame animation.'),
2160:('clarification','Specified original English voice credit and removed extra historical superlative.'),
2161:('clarification','Focused on directing credit and removed extra first-in-history claim.'),
2163:('clarification','Added missing film/version context and removed eons rhetoric.'),
2164:('clarification distractors','Attributed brainstorm to Docter and replaced actual final-job teacher distractor.'),
2165:('clarification','Distinguished electronic soul-world music from jazz; removed implication Oscar was awarded for specific sequences.'),
2167:('clarification distractors','Asked observed behavior in neutral language with parallel action choices.'),
}
plan=json.loads((ROOT/'audit/runs/next-shard-0032-plan.json').read_text(encoding='utf8'))
bank={q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf8'))}
actual={i for i in plan['questionIds'] if digest(bank[i])!=plan['startingHashes'][str(i)]}
assert actual==set(changes),(actual-set(changes),set(changes)-actual)
ref='audit/runs/next-shard-0032-reviewed-notes.json'
for i,(types,reason) in changes.items():
    ledger=json.loads((ROOT/'audit/ledger.json').read_text(encoding='utf8'))
    existing=ledger.get('changeClassifications',{}).get(str(i),{})
    if existing.get('hash')==digest(bank[i]) and set(existing.get('types',[]))==set(types.split()):
        continue
    opts=[x for t in types.split() for x in ('--type',t)]
    command('classify',i,*opts,'--reviewer','Codex','--reason',reason,'--reference',ref)

decisions={
'duplicate-2e0e76861497dcd965b0':'Different cast assignments: Joe Gardner is Jamie Foxx, while 22 is Tina Fey. Memorizing either actor does not identify the other character voice.',
'duplicate-95ff74ee98c0952273a7':'Distinct production facts: 2159 asks who supplied filmed piano-hand reference; 2289 asks the score Oscar recipient. Being a composer/award recipient does not establish animation-reference performance.',
'duplicate-bfeb09e4e913ca3511db':'Unrelated counts: three first-regrowth Hydra heads versus three Disney Wish rotational restaurants. Neither supplies the other fact.',
'duplicate-daa77c481be06a9e9036':'Unrelated counts: three Hydra heads versus three Genie wishes in Aladdin. The shared number is not a shared fact.',
'duplicate-e756061b55084ebb030d':'Unrelated counts: Hydra heads versus Lion King Oscar song nominations. The number three alone does not connect their factual premises.',
'leak-328dbc7ba878036d478d':'Bear identifies the film subject, but not the exact plural development title Bears. Other plausible titles remain; the stem does not state the working title.',
'leak-7aa96deef744dfa7a9fc':'City is a generic location type and formal suffix in New York City; all four options are cities. The stem does not identify New York.',
'scope-03385285c30272cde420':'Season here means spring/summer/autumn/winter in the 1942 theatrical Bambi film; no television series or episode trivia is involved.'
}
report=json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf8'))
applicable=[f for f in report['openFindings'] if any(i in plan['questionIds'] for i in f['questionIds'])]
assert {f['id'] for f in applicable}==set(decisions)
comparisons={'reviewer':'Codex','at':'2026-11-08','scope':plan['questionIds'],
 'findings':[dict(f,comparisonQuestions=[bank[i] for i in f['questionIds']],rationale=decisions[f['id']]) for f in applicable],
 'additionalComparisons':[
  dict(questionIds=[2153,829],questions=[bank[2153],bank[829]],rationale='Exact first-regrowth count versus monster identity: numerical options now require a new fact.'),
  dict(questionIds=[2155,2478],questions=[bank[2155],bank[2478]],rationale='Nominal Fox/Hound budget versus Black Cauldron record; original shared-answer warning no longer applies.'),
  dict(questionIds=[2165,2289],questions=[bank[2165],bank[2289]],rationale='Electronic otherworld composers versus overall score Oscar recipient; musical role and award are different facts.')],
 'retirements':[], 'contentClassifications':{str(i):dict(types=t.split(),reason=r) for i,(t,r) in changes.items()}}
comparison_ref='audit/runs/next-shard-0032-comparisons.json'
(ROOT/comparison_ref).write_text(json.dumps(comparisons,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for f in applicable:
    command('decide',f['id'],'accepted','--reviewer','Codex','--reason',decisions[f['id']],'--reference',comparison_ref)
print('Classified',len(changes),'retained edits and decided',len(applicable),'applicable findings.')
