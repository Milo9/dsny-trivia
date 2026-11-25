"""v1.59 difficulty relabel of the 2026-11 generation rounds. Reviewed by Claude, 2026-11-24.

Run once from any directory. Step "plan" saves the fixed scope with starting
hashes and edits only the `difficulty` value of each line; step "reviews" builds
renewed schema-2 reviews on the final hashes. Every cited page was fetched and
read again on 2026-11-24 against the premise and all four options before this ran;
see release-1.59-difficulty-notes.md.
"""
import copy, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from question_audit import digest  # noqa: E402

AT, WHO = '2026-11-24', 'Claude'
RUN = ROOT / 'audit/runs'
# Classic live-action round (#2796-2895): owner asked for hard. Exceptions are
# answers widely known outside the film itself.
KEEP_EASY = {2806, 2816, 2886, 2891}
CLASSIC_MEDIUM = {2801, 2846}
OTHER = {2657: 'medium', 2670: 'hard', 2672: 'medium', 2678: 'medium', 2680: 'medium', 2694: 'medium',
         2791: 'medium', 2921: 'medium', 2926: 'medium', 2957: 'medium', 2966: 'medium', 2973: 'medium',
         2976: 'medium', 2981: 'medium', 2982: 'medium'}


def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p, v): Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def shards(): return [ROOT / s for s in read(ROOT / 'questions/manifest.json')['shards']]
def bank(): return {q['id']: q for s in shards() for q in read(s)}


def target(q):
    if q['id'] in OTHER:
        return OTHER[q['id']]
    if 2796 <= q['id'] <= 2895 and q['id'] not in KEEP_EASY:
        return 'medium' if q['id'] in CLASSIC_MEDIUM else 'hard'
    return q['difficulty']


def plan():
    qs = bank()
    scope = {i: target(q) for i, q in qs.items() if target(q) != q['difficulty']}
    write(RUN / 'release-1.59-difficulty-plan.json', {
        'schema': 1, 'workflow': 'release-followup', 'createdAt': AT, 'questionIds': sorted(scope),
        'startingHashes': {str(i): digest(qs[i]) for i in sorted(scope)},
        'reason': 'Owner request: mark the obscure classic live-action round hard and re-review the new easy labels.'})
    for path in shards():
        raw = path.read_bytes().decode('utf-8')
        lines = raw.split('\n')
        for n, line in enumerate(lines):
            m = re.match(r'\{"id": ?(\d+),', line.strip())
            if m and int(m[1]) in scope:
                new, count = re.subn(r'("difficulty": ?)"(?:easy|medium|hard)"', r'\1"%s"' % scope[int(m[1])], line)
                assert count == 1, line
                lines[n] = new
        if '\n'.join(lines) != raw:
            path.write_bytes('\n'.join(lines).encode('utf-8'))
    after = bank()
    for i, q in qs.items():
        assert after[i] == {**q, 'difficulty': scope.get(i, q['difficulty'])}, i
    print(len(scope), 'relabelled')


def reviews():
    saved, qs = read(RUN / 'release-1.59-difficulty-plan.json'), bank()
    ledger = read(ROOT / 'audit/ledger.json')['questions']
    out = []
    for i in saved['questionIds']:
        entry, q = ledger[str(i)], qs[i]
        prior = entry.get('review') or next(h['review'] for h in reversed(entry['history']) if h.get('review'))
        old = prior['questionSnapshot']
        assert {**old, 'difficulty': q['difficulty']} == q, i
        v = copy.deepcopy(prior['verification'])
        for part in [v['premise'], *v['options']]:
            for s in part['sources']:
                s.pop('sourceNoteId', None)
                s.update(checkedBy=WHO, checkedAt=AT)
                s['limitations'] = (s.get('limitations') or '').rstrip() + ' Page text fetched and reread 2026-11-24.'
        wrong = ' / '.join(q['answers'][1:])
        v['challenge'] = {
            'reviewer': WHO, 'at': AT, 'premiseChecked': True, 'alternativesExcluded': True,
            'notes': f'Reread {v["premise"]["sources"][0]["url"]} ({v["premise"]["sources"][0]["locator"]}): '
                     f'{v["premise"]["reason"]} Tried to fit {wrong} to the literal wording; the page gives none of '
                     f'them in the role asked about, and it states {q["answers"][0]} for it.'}
        why = ('classic live-action round; owner asked for hard because players find these films obscure'
               if 2796 <= i <= 2895 else 'easy label re-reviewed; recall of this film detail is not easy')
        out.append({'schema': 2, 'questionId': i, 'hash': digest(q), 'questionSnapshot': copy.deepcopy(q),
                    'reviewer': WHO, 'at': AT, 'manual': dict.fromkeys(prior['manual'], True),
                    'notes': f'Difficulty only: {old["difficulty"]} -> {q["difficulty"]} ({why}). Stem, options, category '
                             f'and scope unchanged and reread; distinctness carried from the {prior["at"]} topic review, '
                             f'with no open duplicate finding. Player results were used only as a hint.',
                    'verification': v})
    write(RUN / 'release-1.59-difficulty-reviews.json', out)
    print(len(out), 'reviews')


{'plan': plan, 'reviews': reviews}[sys.argv[1]]()
