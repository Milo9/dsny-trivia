import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
packet = json.loads((root / 'artifacts/question-audit/current.json').read_text(encoding='utf-8'))
review = packet['questions'][0]['existingReview']
review['at'] = '2026-11-08'
review['notes'] = ('Rechecked the reopened shared-answer finding against #1621 and read the complete parks topic digest. '
                   '#98 asks coaster identity/story, #357 its opening year, and #922 its named land: different facts. '
                   '#1621 asks a cruise deployment continent; knowing that answer supplies no attraction-location association.')
verification = review['verification']
verification['context'] = "Disney's Animal Kingdom, Florida; current park land assignment checked 2026-11-08."
source = {
    'url': 'https://disneyworld.disney.go.com/destinations/animal-kingdom/',
    'locator': 'Asia section, Expedition Everest listing (lines 79-85); separate Africa and Discovery Island sections (lines 65-76 and 88-94)',
}
verification['premise'] = {'reason': 'The official park directory explicitly lists Expedition Everest beneath Asia, identifying its park land rather than merely its Himalayan theme.', 'sources': [source]}
reasons = [
    'The park directory lists Expedition Everest under Asia.',
    'Africa is a separate park land in the directory; the explicit Asia assignment excludes Africa as the land containing this attraction.',
    'DinoLand U.S.A. is a different named land, not another name for Asia; the explicit Asia assignment excludes this option regardless of DinoLand closure status.',
    'Discovery Island is separately headed in the directory; the attraction is assigned to Asia, not Discovery Island.',
]
for index, option in enumerate(verification['options']):
    option['sources'] = [source]
    option['reason'] = reasons[index]
    option['basis'] = 'direct' if index == 0 else 'exclusive-inference'
verification['challenge'] = {
    'reviewer': 'Codex', 'at': '2026-11-08', 'premiseChecked': True, 'alternativesExcluded': True,
    'notes': 'Tested whether the Himalayas theme alone was being mistaken for a land assignment, or whether another listed land could contain the attraction. The directory explicitly places it under Asia, with Africa and Discovery Island separate; DinoLand is not a synonym for Asia. The question asks a named park land, not a physical continent or cruise deployment. All four choices are land names; the answer is not supplied by the stem. Medium recall difficulty and parks scope remain appropriate. Compared all parks digest questions and cross-bank Everest/Asia matches: coaster identity, opening year, and cruise deployment remain separate facts.'
}
out = root / 'audit/runs/next-shard-0017-resume-reviews.json'
out.write_text(json.dumps([review], indent=2) + '\n', encoding='utf-8')
comparison = {
    'reviewer': 'Codex', 'at': '2026-11-08',
    'findingId': 'duplicate-c39f2966f10464a8f75a',
    'questions': [],
    'decision': 'accepted',
    'reason': 'Shared answer only: #922 asks the named Animal Kingdom land containing Expedition Everest; #1621 asks the continent associated with Disney Adventure deployment. Memorizing either answer does not establish the other relationship. Neither stem supplies the other fact.',
    'source': source,
}
compact = json.loads((root / 'artifacts/question-audit/current-compact.json').read_text(encoding='utf-8'))
comparison['questions'] = [compact['catalog'][str(qid)] for qid in [922, 1621]]
(root / 'audit/runs/next-shard-0017-resume-comparison-922-1621.json').write_text(json.dumps(comparison, indent=2) + '\n', encoding='utf-8')

for shard in (root / 'questions').glob('q-*.json'):
    for question in json.loads(shard.read_text(encoding='utf-8')):
        if 'everest' in json.dumps(question).lower() or 'Asia' in question.get('answers', []):
            print(json.dumps(question))
