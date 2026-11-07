"""Preserve the individually reviewed Hank identity duplicate."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
qs = {q['id']: q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
reason = 'Same Hank-octopus association in reverse. Question 1036 supplies Hank and asks his species; question 494 supplies the species and asks Hank. Seven arms adds a clue rather than a separately tested fact. Retain the shorter species question.'
out = ROOT/'audit/runs/next-shard-0010-comparisons.json'
out.write_text(json.dumps({'reviewer':'Codex','at':'2026-11-07','comparisons':[{'retiredId':494,'replacementId':1036,'question':qs[494],'replacement':qs[1036],'reason':reason,'evidence':'audit/source-notes.json#b9-dory; Pixar Finding Dory, Hank character section: seven-armed octopus.','challenge':'Read both complete questions and all eight answers. Hank is the octopus in both; Bailey, Destiny and Gerald do not create a separate fact in the removed inverse question.'}]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
subprocess.run([sys.executable,'scripts/question_audit.py','retire','494','--replaced-by','1036','--reviewer','Codex','--reason',reason,'--reference',str(out.relative_to(ROOT))],cwd=ROOT,check=True)
