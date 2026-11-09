import json
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'questions/q-008.json';qs=json.loads(p.read_text(encoding='utf8'))
c=json.loads((r/'audit/runs/next-shard-0036-changes.json').read_text(encoding='utf8'))
updates={2338:('In The Hunchback of Notre Dame II, what do Quasimodo and Madellaine share at the end while Zephyr rings La Fidèle?','Remove a needless first-ever claim; the final romantic scene is sufficient.'),2340:("In 101 Dalmatians II: Patch's London Adventure, what does Lightning reveal to Patch about Thunderbolt?",'Avoid a lexical hint shared only by the correct option.'),2344:('In November 2026, which lounge on Disney Dream and Disney Fantasy features changing digital views of famous cities?','Remove the answer word skyline from the stem.'),2350:('Which venue was designed to celebrate Bahamian Junkanoo at Disney Lookout Cay at Lighthouse Point for its 2024 debut?','Avoid repeating two words of the correct venue name in the stem.')}
for i,(stem,reason) in updates.items():
 q=next(x for x in qs if x['id']==i)
 if str(i) not in c:c[str(i)]={'before':q.copy(),'types':['clarification'],'reason':reason}
 q['question']=stem;c[str(i)]['after']=q.copy()
p.write_text('[\n'+',\n'.join(json.dumps(q,ensure_ascii=False) for q in qs)+'\n]\n',encoding='utf8')
(r/'audit/runs/next-shard-0036-changes.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
