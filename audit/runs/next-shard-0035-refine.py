import json
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'questions/q-008.json'; bank=json.loads(p.read_text(encoding='utf8')); changes=json.loads((r/'audit/runs/next-shard-0035-changes.json').read_text(encoding='utf8'))
for q in bank:
    if q['id']==2303:
        q.update(question='Which character does Alan Tudyk voice in the original English-language Frozen (2013)?',answers=['The Duke of Weselton','Prince Hans','Olaf','Kristoff'],difficulty='medium')
        changes['2303'].update(types=['clarification','distractors','difficulty'],reason='Ask the underlying Frozen voice-credit fact without the name-pun giveaway; use four Frozen characters.')
    if q['id']==2306:
        q['question']="In Toy Story 3 (2010), which toy does Lotso order to take Mr. Potato Head to 'the box'?"
        changes['2306']['reason']='Use the specific enforcer scene, removing the baby-doll description that repeats the keyed name.'
    if str(q['id']) in changes: changes[str(q['id'])]['after']=q
p.write_text('[\n'+',\n'.join(json.dumps(q,ensure_ascii=False) for q in bank)+'\n]\n',encoding='utf8')
(r/'audit/runs/next-shard-0035-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
