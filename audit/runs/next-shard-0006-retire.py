"""Preserve the six duplicate questions evaluated by Codex in batch 6."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAIRS = {
    259: (537, 'Both ask for the cyborg pirate who mentors Jim in Treasure Planet. Retain 537, which uses the film name John Silver and concrete cyborg-cook role instead of subjective morally complex wording.'),
    261: (279, 'Inverse Sven/reindeer identity. Knowing either question and answer supplies the other. Retain the easy character-species question.'),
    265: (1339, 'Both test Merryweather mitigating the death curse into sleep. The retained question gives the complete sleep/true-love-kiss outcome; neither option set requires a different fact.'),
    269: (514, 'Both identify the Dukas Sorcerer\'s Apprentice music for Mickey\'s Fantasia segment. The Dukas attribution is already included in both complete questions; retain 514.'),
    276: (330, 'Inverse Madam Mim / Sword in the Stone wizard-duel association. Memorizing either complete question solves the other without a new fact. Retain the direct character identification.'),
    299: (1458, 'Both identify Kaa as a python in The Jungle Book, with the same hypnotizing-Mowgli context. Retain 1458, whose answer has no extra Kaa parenthesis cue.'),
}
bank = {q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
out = ROOT/'audit/runs/next-shard-0006-retirements'
out.mkdir(exist_ok=True)
for old,(replacement,reason) in PAIRS.items():
    ref=out/f'{old}-{replacement}.json'
    ref.write_text(json.dumps({'reviewer':'Codex','at':'2026-11-06','retired':bank[old],'retained':bank[replacement],'rationale':reason,'scope':'Only the planned question is retired; comparison does not confer factual approval on an unreviewed replacement.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    r=subprocess.run([sys.executable,'scripts/question_audit.py','retire',str(old),'--replaced-by',str(replacement),'--reviewer','Codex','--reason',reason,'--reference',str(ref.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stdout+r.stderr)
    print(f'Retired {old}; retained {replacement}')
