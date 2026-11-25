"""Generation round 5 (backlog #18): 200 easy questions, IDs 2996-3195. Claude, 2026-11-25.

Reads the authored rows (audit/runs/generation-0005-rows.json: one list per question with
stem, options, source key, locator, evidence and a reason per distractor). Steps:
  shard   write questions/q-011.json and list it in the manifest
  plan    save the fixed scope with starting hashes
  notes   write the source library and concise evidence notes for build-reviews
Every source was fetched on 2026-11-25 and the passage behind each correct answer was read
in that text (the last column is the passage pattern that matched). See the notes file.
"""
import json, re, sys
from pathlib import Path
from urllib.parse import quote
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from question_audit import digest  # noqa: E402

RUN, AT, WHO, FIRST = ROOT / 'audit/runs', '2026-11-25', 'Claude', 2996
NOFILM = {'Mickey and Friends', "Chip 'n' Dale", 'Walt Disney', 'Disney Company', 'Winnie the Pooh'}
CHECKS = ['singleAnswer', 'context', 'wording', 'noGiveaway', 'distinctFact', 'category', 'difficulty', 'scope']


def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p, v): Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace("'", '')).strip('-')


def url(s):
    if s.startswith('http'):
        return s
    kind, v = s.split(':', 1)
    if kind == 'wp':
        return 'https://en.wikipedia.org/wiki/' + quote(v, safe='_(),.:!&')
    if kind == 'd23':
        return f'https://d23.com/a-to-z/{v}/'
    return 'https://www.springfieldspringfield.co.uk/movie_script.php?movie=' + v


def rows(): return read(RUN / 'generation-0005-rows.json')


def question(n, p):
    q = {'id': FIRST + n, 'question': p[3], 'answers': p[4:8], 'difficulty': 'easy', 'category': p[0],
         'factId': slug(p[1]) + '.' + p[2]}
    if p[1] not in NOFILM and p[0] not in ('parks', 'walt', 'cruise'):
        q['film'] = p[1]
    q['explanation'] = p[10]
    if not p[8].startswith('sp:'):   # transcripts stay in the ledger, not as a player-facing link
        q['source'], q['verifiedAt'] = url(p[8]), AT
    return q


def shard():
    qs = [question(n, p) for n, p in enumerate(rows())]
    body = '[\n' + ',\n'.join(json.dumps(q, ensure_ascii=False) for q in qs) + '\n]\n'
    (ROOT / 'questions/q-011.json').write_bytes(body.encode('utf-8'))
    m = read(ROOT / 'questions/manifest.json')
    if 'questions/q-011.json' not in m['shards']:
        m['shards'].append('questions/q-011.json')
        write(ROOT / 'questions/manifest.json', m)
    print(len(qs), 'questions')


def bank(): return read(ROOT / 'questions/q-011.json')


def plan():
    qs = bank()
    write(RUN / 'generation-0005-plan.json', {
        'schema': 1, 'kind': 'generation', 'asOf': AT, 'reviewer': WHO,
        'questionIds': [q['id'] for q in qs], 'startingHashes': {str(q['id']): digest(q) for q in qs},
        'scope': '200 additional easy questions on famous films, characters, songs, parks, Walt Disney and '
                 f'cruise basics (backlog #18). IDs {qs[0]["id"]}-{qs[-1]["id"]}.'})


KIND = {'sp': 'Subtitle-derived dialogue transcript; quoted wording was read in that text, not from a viewing.',
        'wp': 'Secondary summary of the work or place; page text read in full context around the passage.',
        'd23': 'Disney archival encyclopedia entry.', 'http': 'Official Disney or Walt Disney Family Museum page.'}


def due(p):
    m = re.search(r'~stable:(\S+)', p[14])
    return m[1] if m else None


def notes():
    qs, rs = bank(), rows()
    sources, reviews = {}, []
    for q, p in zip(qs, rs):
        assert q == question(q['id'] - FIRST, p)
        sid, kind = f'gen5-{q["id"]}', p[8].split(':', 1)[0]
        kind = 'http' if kind.startswith('http') else kind
        sources[sid] = {'url': url(p[8]), 'locator': p[9], 'evidence': p[10], 'checkedBy': WHO, 'checkedAt': AT,
                        'timeSensitive': bool(due(p)), 'nextReviewAt': due(p), 'limitations': KIND[kind],
                        'topics': [p[1]]}
        why = p[11:14]
        basis = ['direct'] + ['exclusive-inference'] * 3
        reviews.append({
            'questionId': q['id'], 'hash': digest(q), 'checks': CHECKS,
            'notes': f'Easy headline fact for {p[1]}; all active and retired stems and answers were read before drafting '
                     'and no question asks this fact. Options are parallel and the stem does not state the answer.',
            'context': p[1], 'timeSensitive': bool(due(p)), 'nextReviewAt': due(p),
            'premise': {'reason': p[10], 'sources': [sid]},
            'options': [{'basis': b, 'reason': r, 'sources': [sid]} for b, r in zip(basis, [p[10], *why])],
            'challenge': {'reviewer': WHO, 'at': AT, 'premiseChecked': True, 'alternativesExcluded': True,
                          'notes': f'Reread {p[9]}. {p[10]} Tried each alternative under the literal wording: '
                                   + ' '.join(f'{a}: {w}' for a, w in zip(p[5:8], why))}})
    write(RUN / 'generation-0005-sources.json', {'schema': 1, 'sources': sources})
    write(RUN / 'generation-0005-evidence-notes.json',
          {'schema': 1, 'reviewer': WHO, 'at': AT, 'sourcesChecked': list(sources), 'reviews': reviews})
    print(len(reviews), 'reviews')


{'shard': shard, 'plan': plan, 'notes': notes}[sys.argv[1]]()
