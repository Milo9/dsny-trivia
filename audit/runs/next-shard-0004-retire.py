"""Apply the duplicate comparisons actually read during batch 4."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAIRS = {
    156: (705, 'Same Be Our Guest / Beauty and the Beast association in reverse; keep the question adding its household-object performance context.'),
    157: (706, 'Same Colors of the Wind / Pocahontas association in reverse; keep the version adding the nature-song context.'),
    161: (712, 'Same Reflection / Mulan association in reverse; keep the identity-conflict context.'),
    162: (1199, 'The retained question identifies Pinocchio and its competitive song-and-score wins together. It subsumes the score winner recall; keep the richer paired-award question rather than another Pinocchio award identification.'),
    163: (1509, 'Same I See the Light / Tangled association in reverse; keep the precise lantern-boat duet context.'),
    166: (699, 'Same How Far I Will Go / Moana association in reverse; keep the heroine longing to explore beyond the reef context.'),
    170: (456, 'Exactly the same Encanto / Lin-Manuel Miranda sole-songwriting attribution in reverse; retain the direct songwriter question.'),
    180: (1313, 'Exactly the same Joy / yellow color association in reverse. The lead-character clause does not add a separate tested fact.'),
    200: (645, 'Same Up villain explorer name. Both supply the explorer-villain role and ask for Muntz; retain the version with his middle initial.'),
    201: (751, 'Exactly the same Bambi / Thumper / rabbit identity in reverse; retain the character-name version.'),
}

bank = {q['id']: q for f in (ROOT / 'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
out = ROOT / 'audit/runs/next-shard-0004-retirements'
out.mkdir(exist_ok=True)
for old, (replacement, reason) in PAIRS.items():
    ref = out / f'{old}-{replacement}.json'
    ref.write_text(json.dumps({'reviewer': 'Codex', 'at': '2026-11-06', 'retired': bank[old], 'retained': bank[replacement], 'rationale': reason, 'scope': 'Retire only the planned ID. Retained questions are duplicate context and receive no new factual approval here.'}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    r = subprocess.run([sys.executable, 'scripts/question_audit.py', 'retire', str(old), '--replaced-by', str(replacement), '--reviewer', 'Codex', '--reason', reason, '--reference', str(ref.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stdout + r.stderr)
    print(f'Retired {old}; retained {replacement}')
