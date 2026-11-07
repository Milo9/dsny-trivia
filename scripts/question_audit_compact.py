"""Compact reading and evidence authoring; never infers editorial approval."""
import copy
from pathlib import Path

from question_audit import (CHECKS, digest, https, nonblank, read_json,
                            record_reviews, review_template, valid_date)


def compact_packet(packet):
    """Normalize repeated question objects without dropping options or findings."""
    catalog = {}

    def remember(q):
        if q is not None:
            key = str(q['id'])
            if key in catalog and catalog[key] != q:
                raise ValueError(f'conflicting snapshots for question {key}')
            catalog[key] = q
            return q['id']

    questions = []
    for entry in packet['questions']:
        questions.append({'id': remember(entry['question']), 'hash': digest(entry['question']),
                          'coverage': entry['coverage'], 'openFindingIds': entry['openFindingIds'],
                          'existingReviewAvailable': entry['existingReview'] is not None})
    for q in packet['relatedQuestions']:
        remember(q)
    comparisons = []
    for item in packet['comparisons']:
        comparisons.append({**{k: v for k, v in item.items() if k != 'questions'},
                            'questionIds': [remember(q) for q in item['questions']]})
    retirements = []
    for item in packet['retirementComparisons']:
        retirements.append({'retiredId': remember(item['retiredQuestion']),
                            'replacementId': remember(item['replacementQuestion']),
                            'decision': item['decision']})
    return {**{k: packet[k] for k in ('schema', 'asOf', 'status', 'planPath', 'resultPath',
                                     'remainingQuestionIds', 'progress') if k in packet},
            'questions': questions, 'catalog': catalog, 'openFindings': packet['openFindings'],
            'comparisons': comparisons, 'retirementComparisons': retirements,
            'topicDigests': packet['topicDigests'],
            'instructions': 'Read the saved plan and QUESTION_AUDIT.md. Catalog contains complete question objects once. '
                            'Read each complete topic digest once per unchanged packet; use view --topic to deduplicate overlapping topics. '
                            'Full packet retains templates, existing reviews and legacy evidence. No evidence or approval is inferred.'}


def reading_view(packet, root, topics=(), ids=()):
    if not topics and not ids:
        return compact_packet(packet)
    catalog = {}
    matches = []
    for topic in packet['topicDigests']:
        if topic['topic'] not in topics:
            continue
        path = (Path(root) / topic['path']).resolve()
        if not path.is_relative_to(Path(root).resolve()):
            raise ValueError('topic path must stay inside the project')
        full = read_json(path)
        matches.append(topic['topic'])
        for q in full['questions']:
            catalog[str(q['id'])] = q
    if set(topics) - set(matches):
        raise ValueError('unknown topic: '+', '.join(sorted(set(topics)-set(matches))))
    if ids:
        available = compact_packet(packet)['catalog']
        available.update(catalog)
        missing = set(ids) - {int(key) for key in available}
        if missing:
            raise ValueError(f'IDs absent from selected context: {sorted(missing)}')
        catalog = {str(qid): available[str(qid)] for qid in ids}
    return {'topics': matches, 'catalog': catalog,
            'scopeNote': 'Topic context does not expand the fixed plan. All four options are preserved.'}


def notes_template(corpus, plan, reviewer, as_of, ids=None):
    by_id = {q['id']: q for q in corpus}
    selected = plan['questionIds'] if ids is None else ids
    if len(set(selected)) != len(selected) or set(selected) - set(plan['questionIds']):
        raise ValueError('notes IDs must be unique and inside the saved plan')
    return {'schema': 1, 'reviewer': reviewer, 'at': as_of,
            'sourcesChecked': [], 'reviews': [
                {'questionId': qid, 'hash': digest(by_id[qid]), 'checks': [], 'notes': '',
                 'context': '', 'timeSensitive': None, 'nextReviewAt': None,
                 'premise': {'reason': '', 'sources': []},
                 'options': [{'basis': '', 'reason': '', 'sources': []} for _ in range(4)],
                 'challenge': {'reviewer': '', 'at': as_of, 'premiseChecked': False,
                               'alternativesExcluded': False, 'notes': ''}}
                for qid in selected if qid in by_id]}


def source_library(value, as_of):
    if not isinstance(value, dict) or value.get('schema') != 1 or not isinstance(value.get('sources'), dict):
        raise ValueError('source library needs schema 1 and a sources object')
    for key, source in value['sources'].items():
        if not nonblank(key) or not isinstance(source, dict) or not https(source.get('url')) \
                or not nonblank(source.get('locator')) or not nonblank(source.get('evidence')) \
                or not nonblank(source.get('checkedBy')) or not valid_date(source.get('checkedAt')) \
                or source['checkedAt'] > as_of or type(source.get('timeSensitive')) is not bool:
            raise ValueError(f'invalid source note: {key}')
        due = source.get('nextReviewAt')
        if (source['timeSensitive'] and due is None) or (due is not None and
                (not valid_date(due) or due <= source['checkedAt'])):
            raise ValueError(f'invalid source recheck date: {key}')
    return value['sources']


def build_reviews(notes, library, corpus, ledger, as_of):
    """Expand only explicit attestations, then use the existing atomic validator."""
    if not isinstance(notes, dict) or notes.get('schema') != 1 or not isinstance(notes.get('reviews'), list):
        raise ValueError('notes need schema 1 and a reviews array')
    if not valid_date(notes.get('at')) or notes['at'] > as_of:
        raise ValueError('notes need a real review date, not in the future')
    sources = source_library(library, as_of)
    checked = notes.get('sourcesChecked')
    if not isinstance(checked, list) or any(key not in sources for key in checked):
        raise ValueError('sourcesChecked must list source IDs actually re-evaluated for this review')
    by_id = {q['id']: q for q in corpus}

    def evidence(item):
        if not isinstance(item, dict):
            raise ValueError('evidence must be an object')
        refs = item.get('sources')
        if not isinstance(refs, list) or not refs:
            raise ValueError('each premise and option needs source IDs')
        expanded = []
        for key in refs:
            if key not in checked:
                raise ValueError(f'source not explicitly checked for this review: {key}')
            source = sources[key]
            if source['checkedAt'] > notes['at']:
                raise ValueError(f'source note postdates the review: {key}')
            if source.get('nextReviewAt') and source['nextReviewAt'] <= as_of:
                raise ValueError(f'source note is due for recheck: {key}')
            expanded.append({'sourceNoteId': key, **copy.deepcopy(source)})
        return {**item, 'sources': expanded}

    reviews = []
    for note in notes['reviews']:
        q = by_id[note['questionId']]
        if note.get('hash') != digest(q):
            raise ValueError(f'stale notes for question {q["id"]}; review the final wording')
        checks = note.get('checks')
        if not isinstance(checks, list) or len(checks) != len(CHECKS) or set(checks) != set(CHECKS):
            raise ValueError('explicitly attest to all eight named checks')
        if not isinstance(note.get('options'), list) or len(note['options']) != 4:
            raise ValueError('provide four option assessments in answer order')
        review = review_template(q)
        review.update(reviewer=notes.get('reviewer'), at=notes.get('at'),
                      manual=dict.fromkeys(checks, True), notes=note.get('notes'))
        review['verification'] = {
            'context': note.get('context'), 'timeSensitive': note.get('timeSensitive'),
            'nextReviewAt': note.get('nextReviewAt'), 'premise': evidence(note['premise']),
            'challenge': copy.deepcopy(note.get('challenge')),
            'options': [{**evidence(item), 'answer': q['answers'][i],
                         'verdict': 'correct' if i == 0 else 'incorrect'}
                        for i, item in enumerate(note['options'])]}
        reviews.append(review)
    # No ledger mutation here. Includes duplicate-ID, snapshot and schema checks.
    record_reviews(corpus, ledger, reviews, as_of)
    return reviews


def finding_changes(previous, current):
    old = {f['id']: f for f in previous['openFindings']}
    new = {f['id']: f for f in current['openFindings']}
    return {'added': sorted(new.keys()-old.keys()), 'resolved': sorted(old.keys()-new.keys()),
            'changed': sorted(k for k in new.keys() & old.keys() if new[k] != old[k])}
