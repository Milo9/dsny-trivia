"""Hash-bound findings and classifications after explicit batch 23 review."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def load(p):
    return json.loads((ROOT/p).read_text(encoding='utf-8'))
def command(*args):
    subprocess.run([sys.executable,'scripts/question_audit.py',*args],cwd=ROOT,check=True)

reasons={
 'answer-style-9a637e772a2ea3886ae5':'All four are ordinary song titles. Everybody Wants to Be a Cat has its normal full title, not an explanatory answer extension. The band/location scene distinguishes the answer.',
 'answer-style-9e82e495e6cc0e610924':'The full standard film title Snow White and the Seven Dwarfs is longer naturally. All four options are film titles; no explanatory material singles out the answer.',
 'answer-style-d9dd1638f01da1049772':'Mickey & Friends Festival of Foods is the complete normal venue name. The stem no longer repeats Mickey and Friends; all answers are venue names, not asymmetric explanations.',
 'duplicate-0cc1f0d9252544fb3034':'Dream Admiral Donald and Wish Cinderella are separate statue-ship assignments. Neither question supplies the other character location; knowing one mapping does not establish the other.',
 'duplicate-0f7dc73092265c56e76b':'First feature released after Walt death (#688) and last personally supervised feature (#1207) are different production milestones. Removed the 1967 stem clue; first posthumous release does not logically establish personal supervision.',
 'duplicate-a143b4f17948ae9a85c7':'Wish Cinderella statue and Treasure sharing Wish dimensions/class concern separate attributes. Ship size does not identify an atrium character.',
 'duplicate-bda7dea8d2cbcc461c8e':'Dream Admiral Donald statue and Dream Beauty and Beast stage show concern different onboard features. Knowing a show ship does not identify the statue ship.',
 'duplicate-bdcdcfaa2f54bb2c8523':'Fantasy Minnie and Wish Cinderella are independent statue assignments, not a repeated character-ship fact. Neither stem provides the other answer.',
 'duplicate-d09431dfbcbd8ff5d9c5':'Dream Donald and Fantasy Minnie are independent statue-ship mappings. There is no exhaustive two-ship premise allowing one mapping to deduce the other.',
 'duplicate-d7b0b43243f26803bf23':'Fantasy Minnie statue and Fantasy Aladdin show require knowledge of two different onboard features. Same ship answer does not duplicate the tested fact.',
 'leak-3149f999306fc5dbc794':'Mickey Mouse identifies which character silhouettes are asked about; hidden was removed from the stem. The needed term is Hidden Mickeys; generic hidden-character wording would include unrelated Easter eggs.',
 'leak-4889a0fac77b67964057':'Tramp appears in the necessary film title Lady and the Tramp. It does not supply Peg song: all four options belong to that film and the pound performance determines the answer.',
 'leak-90f5d4be529a09bf51b4':'Street context describes the scene, but Why Should I Worry also concerns street life. Rita as singer and her lesson uniquely identify Streets of Gold; street alone is not enough.',
 'leak-9bd22d152d7671044c9a':'Rescue is a stemmed overlap from the necessary film title The Rescuers. All four options are songs from that film; the opening delegates anthem distinguishes the answer.',
 'leak-d6ce016b0ce065bc1f5a':'Great in the film title Great Mouse Detective is stemmed to greatest in the answer. This incidental title overlap does not identify Ratigan henchmen song or the Bartholomew interruption.',
}
report=load('artifacts/question-audit.json')
plan=load('audit/runs/next-shard-0023-plan.json')
scope=set(plan['questionIds'])
applicable=[f for f in report['openFindings'] if scope.intersection(f['questionIds'])]
assert {f['id'] for f in applicable}==set(reasons), 'Inspect any fresh warnings before proceeding.'
catalog={q['id']:q for p in sorted((ROOT/'questions').glob('q-*.json')) for q in json.loads(p.read_text(encoding='utf-8'))}
decisions=[]
for f in applicable:
    decisions.append(dict(finding=f,reason=reasons[f['id']],questions=[catalog[i] for i in f['questionIds']],reviewer='Codex',at='2026-11-08'))
(ROOT/'audit/runs/next-shard-0023-finding-decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in applicable:
    command('decide',f['id'],'accepted','--reviewer','Codex','--reason',reasons[f['id']],
            '--reference','audit/runs/next-shard-0023-finding-decisions.json')

edits={
1207:('clarification','Use supervised, excluding preliminary work on later releases; remove year clue.'),
1208:('clarification','Identify Walt Disney Productions as purchaser and specify 1959.'),
1209:('clarification','State art-department vacancy context and 1919; avoid firing legend interpretation.'),
1214:('clarification','Distinguish storm-damaged splash attraction from other child water-play areas.'),
1216:('clarification','Remove Mickey and friends repetition; specify poolside counter grouping.'),
1218:('clarification','Specify Fantasy children science workshops rather than broad interactive youth activities.'),
1224:('clarification distractors','Use exact Dream room categories, distinguishing real from virtual portholes and balcony suites.'),
1229:('clarification distractors','Specify issued physical card and replace overlapping band alternative with card names.'),
1236:('clarification','Restrict to Mickey silhouettes and remove hidden from stem.'),
1238:('clarification','Specify complimentary vehicle service between beach stops; remove island answer repetition.'),
1240:('clarification distractors','Ask official category label; replace legitimate cabin/suite synonyms with competing labels.'),
1242:('clarification','Identify original 1940 film to exclude changed remake songs.'),
1243:('clarification','Specify 1941 film and surreal visions rather than an ordinary dream.'),
1244:('clarification distractors','Isolate launch of mice dress plan and remove Dream reprise which can also fit later dressmaking.'),
1246:('clarification','Specify 1953 film and Darling children.'),
1247:('clarification','Supply film, year and dog-pound context for Peg.'),
1249:('clarification','Specify 1967 animated film.'),
1250:('clarification difficulty','Use Scat Cat band at OMalley home, raise to medium for specific scene association.'),
1251:('clarification','Specify Little John forest celebration to distinguish Not in Nottingham lament.'),
1252:('clarification','Ask delegates anthem, avoiding unsupported assertion of Bernard singing with them.'),
1253:('clarification','Identify henchmen celebration and Bartholomew interruption, excluding Ratigan later vocal recording.'),
1254:('clarification','Add 1988 film and Rita street-survival lesson.'),
1255:('clarification','Specify 1991 snowy garden sequence for changing feelings.'),
}
template=load('audit/runs/next-shard-0023-final-active-template.json')
actual={r['questionId'] for r in template['reviews'] if r['hash']!=plan['startingHashes'][str(r['questionId'])]}
assert actual==set(edits)
for i,(kinds,reason) in edits.items():
    args=['classify',str(i)]
    for kind in kinds.split():
        args+=['--type',kind]
    command(*args,'--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0023-reviews.json')
print('Resolved',len(applicable),'applicable findings; classified',len(edits),'retained edits.')
