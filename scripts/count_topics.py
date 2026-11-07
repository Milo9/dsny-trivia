"""
Counts how many questions are about each Disney/Pixar film.
Counts against question text + correct answer (index 0) only — not distractors.
Run from the project root: python scripts/count_topics.py

Parent-film counts below EXCLUDE matches that belong to a tracked sequel/short
(see scripts/_common.py:SEQUELS_AND_SHORTS) so a "Saturated" label reflects the
base film, not the whole franchise. Sequels/shorts are reported separately.
"""
import json, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SEQUELS_AND_SHORTS

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from question_audit_topics import FILM_PATTERNS as film_keywords

all_questions = []
with open(os.path.join(BASE, 'questions', 'manifest.json'), encoding='utf-8') as f:
    manifest = json.load(f)
for shard_path in manifest['shards']:
    with open(os.path.join(BASE, shard_path), encoding='utf-8-sig') as f:
        all_questions.extend(json.load(f))

print(f'Total questions: {len(all_questions)}\n')

children_by_parent = {}
for entry in SEQUELS_AND_SHORTS:
    if entry['parent']:
        children_by_parent.setdefault(entry['parent'], []).append(entry['pattern'])

haystacks = [(q, q['question'] + ' ' + q['answers'][0]) for q in all_questions]

film_counts = []
for film, pattern in film_keywords.items():
    matched = [(q, h) for q, h in haystacks if re.search(pattern, h, re.IGNORECASE)]
    child_patterns = children_by_parent.get(film)
    if child_patterns:
        combined_child = '|'.join(f'(?:{p})' for p in child_patterns)
        matched = [(q, h) for q, h in matched if not re.search(combined_child, h, re.IGNORECASE)]
    film_counts.append((film, len(matched)))

film_counts.sort(key=lambda x: -x[1])
print(f'{"Film (base film, sequels/shorts excluded)":<42} {"Count":>5}  {"Status"}')
print('-' * 65)
for film, count in film_counts:
    status = 'SATURATED (>=20)' if count >= 20 else ('well-covered (10-19)' if count >= 10 else 'under-covered (<10)')
    print(f'{film:<42} {count:>5}  {status}')

print(f'\n{"Sequel / Short":<42} {"Count":>5}  {"Status"}')
print('-' * 65)
seq_counts = []
for entry in SEQUELS_AND_SHORTS:
    count = sum(1 for q, h in haystacks if re.search(entry['pattern'], h, re.IGNORECASE))
    seq_counts.append((entry['title'], count))
seq_counts.sort(key=lambda x: -x[1])
for title, count in seq_counts:
    status = 'ZERO COVERAGE' if count == 0 else ('covered' if count >= 3 else 'thin')
    print(f'{title:<42} {count:>5}  {status}')
print('\n(For opportunity-sorted sequel/short + distractor-only gaps, run scripts/find_gaps.py)')
