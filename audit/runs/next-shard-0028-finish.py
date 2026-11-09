"""Record final hash-bound classifications using supported audit commands."""
import json
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[2]
prefix = 'audit/runs/next-shard-0028'
plan = json.loads((root / (prefix + '-plan.json')).read_text(encoding='utf-8'))
reviews = json.loads((root / (prefix + '-reviews.json')).read_text(encoding='utf-8'))
types = {
    1538: ['clarification', 'metadata'], 1540: ['clarification'],
    1541: ['clarification', 'distractors'],
    1545: ['factual', 'clarification', 'distractors', 'difficulty'],
    1546: ['factual', 'clarification', 'distractors', 'difficulty'],
    1550: ['clarification'], 1554: ['clarification'],
    1558: ['clarification', 'difficulty'], 1561: ['clarification'],
    1562: ['clarification', 'category'],
    1565: ['clarification', 'distractors'],
    1566: ['factual', 'clarification', 'distractors'],
    1567: ['clarification', 'distractors'], 1569: ['clarification'],
    1573: ['factual', 'clarification', 'distractors', 'difficulty'],
    1574: ['factual', 'clarification', 'distractors'],
    1576: ['factual', 'clarification'],
    1578: ['factual', 'clarification', 'distractors'],
    1579: ['factual', 'clarification'],
    1581: ['clarification'], 1582: ['clarification'],
    1585: ['clarification', 'distractors'],
    1586: ['clarification', 'distractors'], 1588: ['clarification'],
    1589: ['clarification', 'distractors'], 1592: ['clarification'],
    1593: ['clarification'], 1595: ['clarification', 'distractors'],
}
changed = {r['questionId'] for r in reviews if r['hash'] != plan['startingHashes'][str(r['questionId'])]}
assert changed == set(types)
notes = json.loads((root / (prefix + '-reviewed-notes.json')).read_text(encoding='utf-8'))
by_id = {r['questionId']: r for r in notes['reviews']}
ledger = json.loads((root / 'audit/ledger.json').read_text(encoding='utf-8'))
for qid, kinds in types.items():
    existing = ledger.get('changeClassifications', {}).get(str(qid), {})
    if existing.get('hash') == by_id[qid]['hash'] and set(existing.get('types', [])) == set(kinds):
        continue
    args = [sys.executable, 'scripts/question_audit.py', 'classify', str(qid)]
    for kind in kinds:
        args += ['--type', kind]
    args += ['--reviewer', 'Codex', '--reason', by_id[qid]['challenge']['notes'],
             '--reference', prefix + '-reviews.json']
    for attempt in range(4):
        result = subprocess.run(args, cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if not result.returncode or not any(e in result.stderr for e in ['WinError 5', 'WinError 32']):
            break
        time.sleep(0.2)
    if result.returncode:
        print(result.stdout, result.stderr)
        raise SystemExit(result.returncode)
print('Classified', len(types), 'retained edits.')
counts = {t: sum(t in ts for ts in types.values()) for t in sorted({t for ts in types.values() for t in ts})}
print('Change types (overlapping):', json.dumps(counts))
packet = json.loads((root / 'artifacts/question-audit/current-compact.json').read_text(encoding='utf-8'))
comparison = dict(reviewer='Codex', at='2026-11-08',
    questionSnapshots=[packet['catalog'][str(q)] for q in [1559, 1560]],
    decision='retain-both',
    reason='Different tested identities: mother Laurel versus partner Colt. Neither answer supplies the other name.',
    evidence='audit/source-notes.json#b28-onward',
    fullContext='All 351 character, 444 movie, 296 Pixar and 171 Walt category records plus additional named-topic records read with all four answers. Final edits compared against the unchanged context; no duplicate retirement warranted.')
(root / (prefix + '-comparisons.json')).write_text(json.dumps(comparison, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
