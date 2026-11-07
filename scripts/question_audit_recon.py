"""Advisory duplicate ordering and full topic packets; no automatic decisions."""
import re
from collections import defaultdict

from _common import jaccard, normalize_answer, tokenize
from question_audit_topics import FILM_PATTERNS


def inverse_pairs(corpus):
    """Find reciprocal answer/stem mentions, even when neither answer is shared."""
    stems = {q['id']: normalize_answer(q['question']) for q in corpus}
    answers = {q['id']: normalize_answer(q['answers'][0]) for q in corpus}
    index = defaultdict(set)
    for qid, text in stems.items():
        for word in text.split():
            index[word].add(qid)
    pairs = set()
    for qid, answer in answers.items():
        words = answer.split()
        if not words:
            continue
        candidates = set.intersection(*(index[word] for word in words))
        for other in candidates:
            if other <= qid:
                continue
            if (' '+answer+' ') in (' '+stems[other]+' ') \
                    and (' '+answers[other]+' ') in (' '+stems[qid]+' '):
                pairs.add((qid, other))
    return pairs


def duplicate_priority(a, b):
    pair = (min(a['id'], b['id']), max(a['id'], b['id']))
    if pair in inverse_pairs([a, b]):
        return {'priority': 1, 'signals': ['inverse-answer-and-stem']}
    stem_similarity = jaccard(tokenize(a['question']), tokenize(b['question']))
    answer_similarity = jaccard(tokenize(a['answers'][0]), tokenize(b['answers'][0]))
    if stem_similarity >= .45 and answer_similarity >= .5:
        return {'priority': 1, 'signals': ['similar-fact-wording']}
    if stem_similarity >= .5:
        return {'priority': 2, 'signals': ['similar-stems']}
    return {'priority': 3, 'signals': ['shared-answer']}


def topic_digests(selected, corpus):
    """Complete selector matches, with all four answers and no top-N truncation."""
    selectors = {}
    for q in selected:
        haystack = q['question']+' '+q['answers'][0]
        matched = [(name, pattern) for name, pattern in FILM_PATTERNS.items()
                   if re.search(pattern, haystack, re.I)]
        if q.get('film'):
            name = q['film']
            if name not in dict(matched):
                matched.append((name, re.escape(name)))
        if matched:
            for name, pattern in matched:
                selectors[('topic', name)] = pattern
        else:
            # A whole-category fallback makes missing topic coverage visible.
            selectors[('category', q['category'])] = None
    result = []
    for (kind, topic), pattern in sorted(selectors.items()):
        matches = [q for q in corpus if (q['category'] == topic if kind == 'category'
                   else re.search(pattern, q['question']+' '+q['answers'][0], re.I))]
        result.append({'topic': topic, 'selectorKind': kind, 'selector': pattern,
                       'questions': matches, 'count': len(matches),
                       'scopeNote': 'Context for distinctness only; these questions do not expand the saved plan.'})
    return result


def comparison_questions(findings, corpus):
    by_id = {q['id']: q for q in corpus}
    result = []
    for f in findings:
        if f['kind'] != 'duplicate':
            continue
        qs = [by_id[i] for i in f['questionIds'] if i in by_id]
        priority = duplicate_priority(*qs) if len(qs) == 2 else {'priority': 2, 'signals': []}
        result.append({'findingId': f['id'], 'questions': qs, **priority})
    return sorted(result, key=lambda item: (item['priority'], item['findingId']))
