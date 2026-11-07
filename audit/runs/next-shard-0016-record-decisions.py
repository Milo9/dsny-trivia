"""Preserve explicit comparisons; invoke supported retirement/decision commands."""
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(*args): subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,check=True)
bank={q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
retirements=[
 (883,2398,'Both questions encode Mr. Big as the arctic-shrew crime boss in Zootopia. The identity/species relationship is simply reversed. Retain the direct species question.'),
 (896,1468,'Both test the France pavilion / Remy\'s Ratatouille Adventure relationship at EPCOT. Reversing the location and attraction name does not add a fact. Retain the fuller ride-identification question.'),
]
for old,new,reason in retirements:
    ref=f'audit/runs/next-shard-0016-comparison-{old}-{new}.json'
    write(ref,{'reviewer':'Codex','at':'2026-11-07','retiredQuestion':bank[old],'retainedQuestion':bank[new],'reason':reason,'evidenceReference':'artifacts/question-audit/current-compact.json','challenge':'Compared every option in both questions. Memorizing the character/species or attraction/pavilion association answers the reversed question without a new fact. Only the planned question is removed; the replacement is context, not newly approved.'})
    run('retire',old,'--replaced-by',new,'--reviewer','Codex','--reason',reason,'--reference',ref)

ref='audit/runs/next-shard-0016-reviews.json'
decisions={
 (859,1594):'Little John is a bear; Friar Tuck is a badger. Different characters have separately learned animal identities.',
 (863,2479):'Taran\'s occupation/identity and Grant Bardsley\'s voice performance are separate story and production facts; knowing the actor answer does not supply Taran\'s name.',
 (886,887):'Adventureland is the land; Temple of the Forbidden Eye is the subtitle. Neither answer provides the other attribute.',
 (854,1104):'George is Wendy\'s father and Mary her mother. Naming one parent does not identify the other.',
 (888,1139):'Working greenhouses describes an environment the ride visits; The Land identifies the pavilion housing it with Soarin\' and does not by itself establish the greenhouse feature.',
 (100,886):'The Magic Kingdom Pirates location and Disneyland Indiana Jones location are separate attraction/park mappings despite the common land name.',
 (890,1484):'The safari ride\'s identity and the African village name Harambe are separate facts. Final wording asks the truck attraction, not which village surrounds it.',
 (866,1342):'Louis the palace cook in The Little Mermaid and Louis the alligator in The Princess and the Frog are distinct characters with different roles.',
 (855,856):'Lady is a cocker spaniel; Tramp is a mixed-breed dog. Each animal\'s ancestry is a separate fact.',
 (895,1171):'Gran Fiesta Tour\'s location and Mexico pavilion\'s pyramid architecture are different attributes of the same pavilion.',
 (882,1134):'Wasabi\'s forearm plasma blades and Honey Lemon\'s chemistry spheres are separate equipment/character mappings, supported by distinct descriptions.',
 (886,2525):'Indiana Jones Adventure at California Disneyland and Skull Rock at Disneyland Paris are distinct attraction locations, even though both lands are called Adventureland.',
}
manual={
875:'Final wording asks whose recovered memory circuit Jim finds with Flint\'s skeleton; removed the unsupported map-fragment premise. Rechecked transcript and independent scene account.',
877:'Final wording fixes the action-hero movie counterpart named Ace, corroborated by the Buena Vista press release and film cast/ending. No real-first-name assertion remains.',
890:'Removed Wild Africa Trek, which genuinely fit the original wording, and replaced it with Kali River Rapids. Final truck-ride wording excludes raft, train and walking-trail alternatives.',
891:'Past-tense before-closure wording now reflects the February 2026 closure; Time Rovers remains the supported vehicle name.',
898:'The stem now asks about Engineer Goofy\'s train without repeating Mickey, Minnie or railway. Distractors are real, differently themed rides.',
}
report=read('artifacts/question-audit.json')
saved=[]
for f in report['findings']:
    ids=tuple(f['questionIds'])
    if not any(852<=i<=901 for i in ids): continue
    if f.get('decision',{} ) and f['decision'].get('status')=='accepted' and f['decision'].get('signature')==f['signature']: continue
    if f['kind']=='duplicate' and ids in decisions:
        reason=decisions[ids]; status='accepted'
    elif f['kind']=='leak' and ids==(886,):
        reason='Adventure in the attraction name shares a root with Adventureland, but the stem does not give the land name. Indiana Jones attractions have different land names internationally; the California location must be learned.'; status='accepted'
    elif f['kind']=='leak' and ids==(891,):
        reason='Time-traveling explains the attraction premise. Other options include Chrono and Primeval, so the context does not identify the exact proper name Time Rovers.'; status='accepted'
    elif f['kind']=='manual' and ids[0] in manual:
        reason=manual[ids[0]]; status='fixed'
    else: continue
    run('decide',f['id'],status,'--reviewer','Codex','--reason',reason,'--reference',ref)
    saved.append({'findingId':f['id'],'questionIds':list(ids),'status':status,'reason':reason})
write('audit/runs/next-shard-0016-finding-decisions.json',saved)

plan=read('audit/runs/next-shard-0016-plan.json')
reviews=read(ref)
special={864:['distractors'],866:['clarification','distractors'],875:['factual','clarification'],877:['factual','clarification'],887:['clarification','distractors'],890:['factual','clarification','distractors'],891:['factual','clarification'],898:['clarification','distractors']}
changes=[]
for r in reviews:
    i=r['questionId']
    if r['hash']==plan['startingHashes'][str(i)]: continue
    types=special.get(i,['clarification'])
    reason=manual.get(i,'Specified historical/film context, tightened identification wording or improved parallel distractors; no correction to the stored correct identity.')
    args=['classify',i]
    for t in types: args+=['--type',t]
    run(*args,'--reviewer','Codex','--reason',reason,'--reference',ref)
    changes.append({'questionId':i,'types':types,'reason':reason})
write('audit/runs/next-shard-0016-change-notes.json',changes)
