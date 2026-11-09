"""Record explicit change classifications and repair UTF-8 comparison metadata."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
changes = {
 1436: ('clarification distractors', 'Shortened modernization premise and made all causal alternatives parallel.'),
 1437: ('clarification', 'Bound the instrument question to Joe’s jazz audition.'),
 1440: ('factual distractors', 'Replaced Vespa racing with cycling; retained pasta and parallel three-event lists.'),
 1441: ('factual clarification distractors', 'Replaced unsupported lighthouse with the source-described abandoned Roman tower.'),
 1446: ('clarification', 'Ask what Jim rides without crediting him with inventing the device type.'),
 1447: ('clarification', 'Replaced subjective most-dangerous ranking with Scroop’s concrete lifeline-cutting action.'),
 1448: ('factual clarification', 'Corrected Denahi’s immediate revenge premise to his belief that a bear killed Kenai.'),
 1449: ('factual clarification distractors difficulty', 'Acknowledge temporary human restoration, parallel the final-life choices, and use medium recall difficulty.'),
 1458: ('clarification distractors', 'Avoid internally contradictory python/boa terminology in Disney’s profile; ask snake versus three other reptiles.'),
 1459: ('factual clarification', 'Removed the false only-fear assertion; Khan also fears guns. Bound the answer to the burning-branch climax.'),
 1464: ('factual clarification distractors', 'Replace throughout-his-life belief with the initial belief and remove the also-defensible Penny-danger choice.'),
 1466: ('clarification', 'Ask the spirits’ proper name so descriptive mist/stone labels cannot count as alternatives.'),
 1467: ('factual clarification', 'Correct the captured vessel to guests’ transport and date the operating attraction.'),
 1468: ('clarification', 'Remove the film-title echo and date the current attraction.'),
 1474: ('clarification', 'Date the water-park offering while preserving its specific theme and features.'),
 1475: ('clarification', 'Isolate the historical technology debut and remove birds clue shared with the separate musical-attraction question.'),
 1479: ('clarification', 'Use the sourced Hunny Pot experience, remove subjective fan-favorite wording and unnecessary replacement claim, and date the offering.'),
 1482: ('clarification', 'Identify the predecessor area without implying the entire physical redesign occurred in 2021.'),
 1485: ('clarification', 'Remove castle-name giveaway and date the current princess dining experience.'),
 1486: ('clarification distractors', 'Ask the ride that opened after Maelstrom; replace the ambiguous predecessor option with other actual rides.'),
 1487: ('factual clarification distractors', 'State post-armistice service in France and remove poster drawing, which Walt also did.'),
 1490: ('factual clarification', 'Ask about leading resort completion rather than implying Roy only became a company leader after Walt died.'),
 1494: ('factual clarification', 'Remove unsupported Walt-coined attribution; ask Disney’s established professional title.'),
 1495: ('clarification distractors difficulty', 'Ask the depth effect directly; use parallel alternatives and medium difficulty.'),
 1496: ('clarification distractors', 'Test the corroborated statuette configuration with equally formed count/size alternatives.'),
 1497: ('factual clarification', 'Remove the false universal claim that Mirabel is the only ungifted Madrigal; ask the private lament.'),
 1499: ('factual clarification distractors', 'Correct song context from Casita’s collapse to Alma/Pedro’s flashback; use actual song alternatives.'),
 1511: ('clarification difficulty', 'Remove Dr. Facilier clue, which made the villain-name question solve this without knowing the song; use medium attribution difficulty.'),
 1512: ('factual clarification distractors', 'Use Disney Lookout Cay’s proper destination name and avoid calling Eleuthera a wholly private island.'),
 1517: ('clarification', 'Describe enchanted-art clues rather than a generic special device and date the current game offering.'),
 1530: ('clarification', 'Remove teddy-bear answer echo; use Lotso’s specific command role.'),
 1535: ('clarification distractors', 'Specify the 1961 animated film and replace estate aliases with distinct named places.'),
}

def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))

plan = read('audit/runs/next-shard-0027-plan.json')
notes = read('audit/runs/next-shard-0027-reviewed-notes.json')
edited = {r['questionId'] for r in notes['reviews'] if r['hash'] != plan['startingHashes'][str(r['questionId'])]}
assert edited == set(changes), (edited, set(changes))
for i, (types, reason) in changes.items():
    existing = read('audit/ledger.json')['changeClassifications'].get(str(i), {})
    expected_hash = next(r['hash'] for r in notes['reviews'] if r['questionId'] == i)
    if existing.get('hash') == expected_hash and set(existing.get('types', [])) == set(types.split()):
        continue
    args = [sys.executable, 'scripts/question_audit.py', 'classify', str(i)]
    for kind in types.split():
        args += ['--type', kind]
    args += ['--reviewer', 'Codex', '--reason', reason, '--reference', 'audit/runs/next-shard-0027-reviewed-notes.json']
    for attempt in range(3):
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if not result.returncode or '[WinError 5]' not in result.stdout + result.stderr:
            break
        time.sleep(0.5)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)

# The original catalog is UTF-8. Correct comparison metadata written through a
# Windows-default-decoded read; retirement snapshots themselves were untouched.
catalog = read('artifacts/question-audit/current-compact.json')['catalog']
for i, replacement in [(1477,345),(1481,104),(1484,890)]:
    path = ROOT / f'audit/runs/next-shard-0027-comparison-{i}-{replacement}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    data['retiredOriginal'] = catalog[str(i)]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Classified {len(changes)} retained edits; comparison metadata uses original UTF-8 text.')
