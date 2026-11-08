"""Save inspected duplicate comparisons; does not modify shards."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[2]
catalog = {}
for path in (root / 'questions').glob('q-*.json'):
    for q in json.loads(path.read_text(encoding='utf-8-sig')):
        catalog[q['id']] = q
pairs = {
    1154: (2253, 'The retained opening-year question explicitly names Mystic Manor as the trackless ride in Hong Kong Disneyland Mystic Point. Its premise directly supplies the identity asked here; retain the additional date fact.'),
    1155: (2257, 'The retained princess-dedication question explicitly names Shanghai Disneyland Enchanted Storybook Castle. This simpler identity is supplied verbatim in its premise.'),
    1161: (1365, 'The retained host-pair question explicitly identifies the American Adventure as a US-history show. That premise supplies the country asked here; retain the additional host fact.'),
    1162: (1475, 'The retained Tiki Room identity question gives the 1963 Disneyland opening and the animatronics milestone. This is the same opening event in reverse, with the year already supplied.'),
    1177: (682, 'The retained D23-name question answers that 23 commemorates the studio founding in Hollywood in 1923. This standalone founding-year question repeats that fact.'),
    1180: (1372, 'The retained wife-name question explicitly supplies the 1925 marriage date. Memorizing that premise answers this inverse date question.'),
    1186: (129, 'Both test Carolwood as the identifying name of Walt backyard railway. Of the street options only Carolwood matches the retained railroad identity; retain the complete railway-name question.'),
    1196: (1197, 'Both concern the same first cartoon Oscar awarded to Flowers and Trees. The category question offers only one cartoon category for the same short-film award event; retain the direct first-competitive-award identity question.'),
}
out = {'reviewer': 'Codex', 'at': '2026-11-08', 'scope': 'Batch 22 only; replacement questions read as context', 'comparisons': []}
for old, (new, reason) in pairs.items():
    out['comparisons'].append({'retire': old, 'replacedBy': new, 'reason': reason, 'removedSnapshot': catalog[old], 'retainedSnapshot': catalog[new], 'challenge': 'Read all four options on both questions. The retained question supplies the tested fact; no independent fact is needed to answer the retired question.'})
(root / 'audit/runs/next-shard-0022-comparisons.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
