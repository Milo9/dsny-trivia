import json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
def read(p): return json.loads((root/p).read_text(encoding='utf-8'))
def write(p,v): (root/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qs=read('questions/q-005.json')
for q in qs:
    if q['id']==1270: q['question']='In Wish (2023), what solo does Asha sing as she looks to the stars for a better future for the people of Rosas?'
    if q['id']==1274: q['answers']=['Camouflage','Echolocation','Bioluminescence','Hypnosis']
    if q['id']==1279: q['answers']=['A boot','A lunchbox','A flowerpot','A toolbox']
    if q['id']==1295: q['question']='In Lightyear, what fuel source does Buzz repeatedly test in an effort to get the stranded crew home?'
    if q['id']==1292: q.update(read('artifacts/question-audit/current-compact.json')['catalog']['1292'])
write('questions/q-005.json',qs)
c={q['id']:q for p in (root/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf-8'))}
v=read('audit/runs/next-shard-0024-comparisons.json')
v['retirements'].append({'question':c[1292],'replacement':c[1316],
 'reason':'#1316 explicitly supplies Half Note as the club where Joe plays. That alone answers #1292; retain the more specific musician-identification question.',
 'sources':['https://www.pixar.com/soul'],'locator':'The Half Note setting and Dorothea Williams character sections'})
v['retainedComparisons']=[x for x in v['retainedComparisons'] if x['ids']!=[1292,1437]]
write('audit/runs/next-shard-0024-comparisons.json',v)
