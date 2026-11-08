"""Explicit content decisions for batch 24; no evidence inferred."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,v): (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
edits={
1256: "In Aladdin (1992), which song does Genie perform when Aladdin first summons him inside the cave?",
1258: "In The Hunchback of Notre Dame (1996), which song does Esmeralda sing as a prayer for people in need inside the cathedral?",
1260: "In Mulan (1998), which song do the soldiers sing on their march while imagining their ideal partners?",
1263: "In Brother Bear (2003), which song accompanies Kenai and Koda's travel montage, including their mammoth ride?",
1264: "In Home on the Range (2004), which early song introduces the idyllic dairy farm where Maggie arrives?",
1268: "Which Fall Out Boy song accompanies the team's super-suit training montage in Big Hero 6 (2014)?",
1269: "Who composed the orchestral score for Zootopia (2016)?",
1270: "In Wish (2023), what solo does Asha sing as she wishes for a better future for the people of Rosas?",
1272: "In A Bug's Life, which princess is preparing to succeed the Queen as the colony's ruler?",
1274: "In Monsters, Inc., what is Randall's chameleon-like method of blending into his surroundings called?",
1275: "In Finding Nemo, which adult sea turtle carries Marlin along the East Australian Current?",
1278: "In Ratatouille, what job does Skinner hold at Gusteau's when Linguini first arrives?",
1279: "Early in WALL-E, what object does WALL-E use as a planter for the seedling he discovers?",
1291: "In Onward, which part of Ian and Barley's father is restored by their first attempt at the visitation spell?",
1292: "In Soul, at which jazz club does Joe audition for Dorothea Williams and later perform with her band?",
1295: "In Lightyear, what fuel source does Buzz test in his attempts to achieve hyperspeed?",
}
qs=read('questions/q-005.json')
for q in qs:
    if q['id'] in edits: q['question']=edits[q['id']]
write('questions/q-005.json',qs)
catalog={q['id']:q for p in (ROOT/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf-8'))}
write('audit/runs/next-shard-0024-comparisons.json',{
 'reviewer':'Codex','at':'2026-11-08','topicContext':'Read all 810 unique complete questions from the 30 packet topic digests, plus batch comparisons. Only planned questions are changed.',
 'retirements':[{'question':catalog[1265],'replacement':catalog[1511],
 'reason':'Inverse film/song association for the same Dr. Facilier performance; #1511 already names the song, performer and shadow context. Knowing that mapping solves #1265 without a new fact.',
 'sources':['b19-1014'],'reference':'audit/source-notes.json'}],
 'retainedComparisons':[
 {'ids':[1269,1502],'reason':'Independent score credits for Zootopia and Up. Knowing one composer credit does not establish the other.'},
 {'ids':[1271,1298],'reason':'Slinky stretching from the truck and RC carrying Woody/Buzz are different toy identities and separate rescue actions.'},
 {'ids':[1292,1437],'reason':'The Half Note club identity and Joe playing piano are independent facts.'},
 {'ids':[1284,1313],'reason':'Disgust green and Joy yellow are separate character-color mappings; no exhaustive two-color assignment makes one imply the other.'}
 ]})
print('Edited',len(edits),'planned questions; saved complete duplicate comparison.')
