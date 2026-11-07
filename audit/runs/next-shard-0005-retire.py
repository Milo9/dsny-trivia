"""Record the batch-5 comparisons read by Codex and preserve duplicate snapshots."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAIRS = {
    208: (526, 'Same Baymax / personal healthcare robot identity in reverse. Retain the direct role question; inflatable wording does not test a separate fact.'),
    213: (576, 'Same Moana / Heihei / rooster identity. Chicken and rooster refer to the same character, and both ask his name.'),
    242: (656, 'Both identify Stinky Pete as the villainous prospector in Toy Story 2. The mentor framing supplies context but asks no separate fact.'),
    244: (2179, 'The retained question explicitly tests Ernesto poisoning Hector and stealing his songs. That answer already establishes the original songwriter; retire the simpler overlapping authorship question.'),
    248: (1252, 'The organization and its self-named anthem both have the answer Rescue Aid Society. Memorizing that name solves both among their options; retain the anthem question, which adds musical context.'),
}
bank = {q['id']: q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
out = ROOT/'audit/runs/next-shard-0005-retirements'
out.mkdir(exist_ok=True)
for old, (replacement, reason) in PAIRS.items():
    ref = out/f'{old}-{replacement}.json'
    ref.write_text(json.dumps({'reviewer':'Codex','at':'2026-11-06','retired':bank[old],'retained':bank[replacement],'rationale':reason,'scope':'Only the planned ID is retired. Replacement is duplicate context; no factual approval is inferred for it.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result = subprocess.run([sys.executable,'scripts/question_audit.py','retire',str(old),'--replaced-by',str(replacement),'--reviewer','Codex','--reason',reason,'--reference',str(ref.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if result.returncode:
        raise SystemExit(result.stdout+result.stderr)
    print(f'Retired {old}; retained {replacement}')
