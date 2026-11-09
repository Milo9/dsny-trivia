import json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parents[2]
bank={q['id']:q for p in (r/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf8'))}
data=[(2289,2165,'The earlier question supplies Jon Batiste in its stem and Reznor/Ross in its answer. That same trio solves #2289; keep the already-approved question about their distinct musical roles.','https://www.oscars.org/oscars/ceremonies/2021'),(2293,2646,'#2646 explicitly asks who wrote both Yo Ho and Grim Grinning Ghosts, subsuming the Yo Ho lyricist fact in #2293. Retain the broader two-song relationship.','https://d23.com/a-to-z/atencio-francis-x/')]
for old,new,reason,url in data:
    ref=f'audit/runs/next-shard-0035-comparison-{old}-{new}.json'
    (r/ref).write_text(json.dumps(dict(reviewer='Codex',at='2026-11-09',retired=bank[old],replacement=bank[new],reason=reason,evidence=url,topicContext='Complete combined topic digests and cross-bank searches read, including all four options.'),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    subprocess.run([sys.executable,'scripts/question_audit.py','retire',str(old),'--replaced-by',str(new),'--reviewer','Codex','--reason',reason,'--reference',ref],cwd=r,check=True)
