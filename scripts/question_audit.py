"""Version-bound question audit ledger, triage, sampling, decisions and release gate.

No command searches the web or claims facts have been verified automatically.
Record commands never infer factual correctness. Only the explicit retire command
changes shards, with a recoverable transaction preserving historical snapshots.
See QUESTION_AUDIT.md for the editorial procedure and command examples.
"""
import argparse
import copy
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import random
import re
import sys
from urllib.parse import urlparse

from _common import BASE, find_answer_leaks, load_corpus, normalize_answer, tokenize
from find_category_bugs import check_category
from find_near_dupes import find_similar_pairs

ROOT = Path(BASE)
CHECKS = ('singleAnswer', 'context', 'wording', 'noGiveaway', 'distinctFact',
          'category', 'difficulty', 'scope')
EVIDENCE_BASES = ('direct', 'contradiction', 'exclusive-inference', 'exhaustive-list')
# QUESTION_AUDIT.md rule 7: longest recheck interval, in days from the evidence date.
# 'historical' (date-anchored or past-event) facts take no recheck at all.
RECHECK_TIERS = {'changeable': 92, 'stable': 366}
CHANGE_TYPES = ('factual', 'clarification', 'distractors', 'explanation',
                'difficulty', 'category', 'scope', 'metadata')
RISK_PATTERNS = {
    'changing-fact': r'\b(current|currently|newest|latest|most recent|today|now|upcoming|scheduled)\b',
    'record-or-superlative': r'\b(first|only|largest|biggest|smallest|longest|record|most|least)\b',
    'specific-attribution': r'\b(voic\w*|compos\w*|songwrit\w*|lyric\w*|direct\w*|cast|portray\w*|considered)\b',
    'exact-number-or-date': r'\b(how many|what year|which year|how old|how long|preceded|years? before|years? after)\b|\b\d{4}\b',
    'inverted-logic': r'\b(not|never|except|incorrect|false)\b',
    'ship-or-venue': r'\b(ship|restaurant|venue|attraction|ride|cruise|renamed|replaced)\b',
    'plot-or-attribute': r'\b(why|happens|cause\w*|belong\w*|owns?|whose|wear\w*|color|colour|species|animal)\b',
    'tv-scope': r'\b(television|tv show|disney channel|series|episode|season|mandalorian|wandavision|ducktales)\b',
}


def today():
    return datetime.now(timezone.utc).date().isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def valid_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def https(value):
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username


def validate_review(review, as_of):
    """Validate evidence records; this cannot judge whether a source supports a claim."""
    errors = []
    if not isinstance(review, dict):
        return ['review must be an object']
    if review.get('schema', 1) not in (1, 2):
        errors.append('unsupported review schema')
    if not nonblank(review.get('reviewer')):
        errors.append('reviewer is required')
    if not valid_date(review.get('at')) or review['at'] > as_of:
        errors.append('review date must be a real date, not in the future')
    manual = review.get('manual')
    if not isinstance(manual, dict) or any(manual.get(k) is not True for k in CHECKS):
        errors.append('all eight manual checklist items must be explicitly true')
    if not nonblank(review.get('notes')):
        errors.append('manual review notes are required')
    verified = review.get('verification')
    if verified is not None:
        if not isinstance(verified, dict):
            return errors + ['verification must be an object or null']
        if not nonblank(verified.get('context')):
            errors.append('verification needs the version/location/time context')
        if type(verified.get('timeSensitive')) is not bool:
            errors.append('timeSensitive must be explicitly true or false')
        due = verified.get('nextReviewAt')
        if due is not None and (not valid_date(due) or due <= review.get('at', '')):
            errors.append('nextReviewAt must be a real date after the review date')
        if verified.get('timeSensitive') and due is None:
            errors.append('changing facts require nextReviewAt')
        if valid_date(due) and valid_date(review.get('at')) and \
                (date.fromisoformat(due)-date.fromisoformat(review['at'])).days > RECHECK_TIERS['stable']:
            errors.append('nextReviewAt must fall within 12 months of the review (rule 7)')
        if review.get('schema') == 2:
            premise = verified.get('premise', {})
            if not isinstance(premise, dict) or not nonblank(premise.get('reason')) \
                    or not valid_sources(premise.get('sources')):
                errors.append('premise needs a source-backed check of the question\'s assumptions')
            challenge = verified.get('challenge', {})
            if not isinstance(challenge, dict) or not nonblank(challenge.get('reviewer')) \
                    or not valid_date(challenge.get('at')) or challenge['at'] > as_of \
                    or not valid_date(review.get('at')) or challenge['at'] < review['at'] \
                    or challenge.get('premiseChecked') is not True \
                    or challenge.get('alternativesExcluded') is not True \
                    or not nonblank(challenge.get('notes')):
                errors.append('final evidence challenge needs reviewer/date, premise and competing-answer checks, and notes')
        options = verified.get('options')
        if not isinstance(options, list) or len(options) != 4:
            errors.append('verification requires evidence for all four options')
        else:
            for i, option in enumerate(options):
                if not isinstance(option, dict):
                    errors.append(f'option {i} must be an object')
                    continue
                if option.get('verdict') != ('correct' if i == 0 else 'incorrect'):
                    errors.append(f'option {i} needs the appropriate explicit verdict')
                if not nonblank(option.get('reason')):
                    errors.append(f'option {i} needs a factual rationale')
                if review.get('schema') == 2 and option.get('basis') not in EVIDENCE_BASES:
                    errors.append(f'option {i} needs an evidence basis: '+', '.join(EVIDENCE_BASES))
                sources = option.get('sources')
                if not isinstance(sources, list) or not sources:
                    errors.append(f'option {i} needs supporting sources')
                elif any(not isinstance(s, dict) or not https(s.get('url'))
                         or not nonblank(s.get('locator')) for s in sources):
                    errors.append(f'option {i} sources need HTTPS URLs and specific evidence locators')
    return errors


def valid_sources(sources):
    return (isinstance(sources, list) and bool(sources)
            and all(isinstance(s, dict) and https(s.get('url')) and nonblank(s.get('locator')) for s in sources))


def record_reviews(corpus, ledger, reviews, as_of):
    """Validate the entire batch before producing a changed ledger; no partial imports."""
    if not isinstance(reviews, list) or not reviews:
        raise ValueError('provide a nonempty array of reviews')
    by_id = {q['id']: q for q in corpus}
    seen = set()
    for review in reviews:
        if not isinstance(review, dict) or type(review.get('questionId')) is not int:
            raise ValueError('every review needs an integer questionId')
        qid = review['questionId']
        if qid in seen:
            raise ValueError(f'#{qid}: duplicate review in bulk import')
        seen.add(qid)
        if qid not in by_id:
            raise ValueError(f'#{qid}: not an active question')
        if review.get('schema') != 2:
            raise ValueError(f'#{qid}: new records require schema 2; re-review the premise and competing answers')
        q = by_id[qid]
        if review.get('hash') != digest(q) or review.get('questionSnapshot') != q:
            raise ValueError(f'#{qid}: question changed since template creation; re-review its current version')
        errors = validate_review(review, as_of)
        if not errors and review.get('verification') and [o.get('answer') for o in review['verification']['options']] != q['answers']:
            errors.append('option evidence must match current answers in their stored order')
        if errors:
            raise ValueError(f'#{qid}: '+'; '.join(errors))
    updated = sync_ledger(corpus, copy.deepcopy(ledger), as_of)
    for review in reviews:
        entry = updated['questions'][str(review['questionId'])]
        if entry.get('review'):
            entry['history'].append({'hash': entry['hash'], 'review': entry['review']})
        entry['review'] = copy.deepcopy(review)
    return updated


def evidence_date(review):
    """Earliest recorded source inspection behind a review, else the review date."""
    verified = review.get('verification') or {}
    parts = [verified.get('premise') or {}] + [o for o in verified.get('options') or [] if isinstance(o, dict)]
    dates = [s['checkedAt'] for part in parts if isinstance(part, dict) for s in part.get('sources') or []
             if isinstance(s, dict) and valid_date(s.get('checkedAt'))]
    return min(dates + [review['at']])


def recheck_calendar(report, as_of, months=12):
    """Scheduled factual rechecks per month, so a due wave is visible before the gate fails."""
    dues = [q['nextReviewAt'] for q in report['questions'] if q.get('nextReviewAt')]
    horizon = (date.fromisoformat(as_of)+timedelta(days=31*months)).isoformat()
    upcoming = Counter(d[:7] for d in dues if as_of < d <= horizon)
    return {'overdue': sum(d <= as_of for d in dues), 'byMonth': dict(sorted(upcoming.items())),
            'later': sum(d > horizon for d in dues)}


def current_review(entry, q, as_of):
    review = entry.get('review')
    if entry.get('hash') != digest(q) or not isinstance(review, dict) or validate_review(review, as_of):
        return None
    if review.get('hash') != digest(q) or review.get('questionSnapshot') != q:
        return None
    if review.get('verification') and [o.get('answer') for o in review['verification']['options']] != q['answers']:
        return None
    return review


def sync_ledger(corpus, ledger, as_of):
    ledger.setdefault('issues', {})
    for q in corpus:
        key, fingerprint = str(q['id']), digest(q)
        entry = ledger['questions'].setdefault(key, {'history': []})
        if entry.get('hash') and entry['hash'] != fingerprint:
            entry['history'].append({k: entry[k] for k in ('hash', 'mechanicalAt', 'review') if k in entry})
            entry.pop('review', None)
        entry.update(hash=fingerprint, mechanicalAt=as_of)
        # Imported metadata is evidence to investigate, never an automatic review.
        entry['legacyEvidence'] = {k: q[k] for k in ('source', 'verifiedAt') if k in q}
    return ledger


def findings_for(corpus):
    """Stable content-bound findings; noisy checks never decide correctness."""
    by_id = {q['id']: q for q in corpus}
    findings = {}

    def add(kind, ids, detail):
        ids = sorted(ids)
        signature = digest({'kind': kind, 'ids': ids, 'detail': detail,
                            'hashes': [digest(by_id[i]) for i in ids]})
        key = kind + '-' + signature[:20]
        findings[key] = {'id': key, 'kind': kind, 'questionIds': ids,
                         'detail': detail, 'signature': signature}

    for q in corpus:
        for leak in find_answer_leaks(q):
            add('leak', [q['id']], leak)
        for category in check_category(q):
            add('category', [q['id']], list(category))
        if re.search(RISK_PATTERNS['tv-scope'], q['question'], re.I):
            add('scope', [q['id']], 'Check the no-TV-shows boundary; incidental mentions may be valid.')
        lengths = [len(a.split()) for a in q['answers']]
        if lengths[0] >= max(6, max(lengths[1:]) * 2):
            add('answer-style', [q['id']], 'Correct answer is unusually verbose relative to distractors.')
    pairs = {(a['id'], b['id']) for _, a, b in find_similar_pairs(corpus, corpus, .5, True)}
    # Include every shared-answer group, including common names and short answers.
    groups = defaultdict(list)
    for q in corpus:
        groups[normalize_answer(q['answers'][0])].append(q)
    for members in groups.values():
        for i, a in enumerate(members):
            for b in members[i+1:]:
                pairs.add((min(a['id'], b['id']), max(a['id'], b['id'])))
    from question_audit_recon import duplicate_priority, inverse_pairs
    pairs.update(inverse_pairs(corpus))
    for a, b in sorted(pairs):
        add('duplicate', [a, b], 'Could memorizing one answer solve the other without learning a new fact?')
    for finding in findings.values():
        if finding['kind'] == 'duplicate':
            a, b = finding['questionIds']
            finding.update(duplicate_priority(by_id[a], by_id[b]))
    return sorted(findings.values(), key=lambda f: (f.get('priority', 0), f['id']))


def decision_valid(decision, finding, as_of):
    return (isinstance(decision, dict) and decision.get('signature') == finding['signature']
            and decision.get('status') in ('accepted', 'unresolved', 'fixed')
            and nonblank(decision.get('reason')) and nonblank(decision.get('reviewer'))
            and valid_date(decision.get('at')) and decision['at'] <= as_of)


def open_findings(findings, ledger, as_of):
    return [f for f in findings if not (decision_valid(ledger['decisions'].get(f['id']), f, as_of)
                                      and (ledger['decisions'][f['id']]['status'] == 'accepted'
                                           or (f['kind'] == 'manual' and ledger['decisions'][f['id']]['status'] == 'fixed')))]


def audit_findings(corpus, ledger):
    findings = findings_for(corpus)
    by_id = {q['id']: q for q in corpus}
    for key, issue in ledger.get('issues', {}).items():
        ids = [i for i in issue['questionIds'] if i in by_id]
        if ids:
            findings.append({'id': key, 'kind': 'manual', 'questionIds': ids, 'detail': issue['reason'],
                             'signature': digest({'issue': key, 'hashes': [digest(by_id[i]) for i in ids]})})
    return sorted(findings, key=lambda f: f['id'])


def risk_map(corpus):
    risks = {}
    correct_index = defaultdict(list)
    tokens = {q['id']: tokenize(q['question']) for q in corpus}
    for q in corpus:
        risks[q['id']] = [label for label, pattern in RISK_PATTERNS.items()
                          if re.search(pattern, q['question'], re.I)]
        correct_index[normalize_answer(q['answers'][0])].append(q)
    for q in corpus:
        for answer in q['answers'][1:]:
            for other in correct_index[normalize_answer(answer)]:
                if other['id'] != q['id'] and len(tokens[q['id']] & tokens[other['id']]) >= 3:
                    risks[q['id']].append('cross-answer-collision')
        risks[q['id']] = sorted(set(risks[q['id']]))
    return risks


def make_plan(corpus, ledger, as_of, seed, limit, sample_per_category):
    risks = risk_map(corpus)
    pending = [q for q in corpus if not source_verified(ledger['questions'].get(str(q['id']), {}), q, as_of)]
    ranked = sorted((q for q in pending if risks[q['id']]),
                    key=lambda q: (-len(risks[q['id']]), q['id']))[:limit]
    sampled = []
    rng = random.Random(seed)
    categories = sorted({q['category'] for q in corpus})
    for category in categories:
        pool = sorted((q['id'] for q in pending if q['category'] == category and not risks[q['id']]))
        sampled.extend(rng.sample(pool, min(sample_per_category, len(pool))))
    return {'schema': 1, 'createdAt': as_of, 'seed': seed, 'riskLimit': limit,
            'samplePerCategory': sample_per_category, 'corpusHash': digest(corpus),
            'questionIds': sorted({q['id'] for q in ranked} | set(sampled)),
            'riskSelected': {str(q['id']): risks[q['id']] for q in ranked},
            'randomSampleIds': sorted(sampled), 'population': len(corpus),
            'notCurrentlyVerified': len(pending), 'startingHashes': {str(q['id']): digest(q) for q in ranked +
                [q for q in corpus if q['id'] in sampled]}}


def source_verified(entry, q, as_of):
    review = current_review(entry, q, as_of)
    if not review or review.get('verification') is None:
        return False
    due = review['verification'].get('nextReviewAt')
    return not due or due > as_of


def audit_report(corpus, ledger, baseline, as_of, findings=None):
    findings = findings if findings is not None else audit_findings(corpus, ledger)
    findings = [dict(f, decision=ledger['decisions'].get(f['id'])) for f in findings]
    outstanding = open_findings(findings, ledger, as_of)
    blocked = {i for f in outstanding for i in f['questionIds']}
    evidence_concerns = {i for f in outstanding if f['kind'] == 'manual' for i in f['questionIds']}
    risks = risk_map(corpus)
    counts = Counter()
    questions = []
    for q in corpus:
        key = str(q['id'])
        entry = ledger['questions'].get(key, {})
        review = current_review(entry, q, as_of)
        mechanical = entry.get('hash') == digest(q) and valid_date(entry.get('mechanicalAt')) and entry['mechanicalAt'] <= as_of
        recorded = source_verified(entry, q, as_of)
        verified = recorded and q['id'] not in evidence_concerns
        approved = bool(mechanical and review and recorded and q['id'] not in blocked)
        overdue = bool(review and review.get('verification') and review['verification'].get('nextReviewAt')
                       and review['verification']['nextReviewAt'] <= as_of)
        required = baseline['questions'].get(key) != digest(q)
        counts.update(mechanical=int(mechanical), manual=int(bool(review)), evidenceRecorded=int(recorded),
                      sourceVerified=int(verified), approved=int(approved),
                      challengedEvidence=int(recorded and review.get('schema') == 2),
                      legacyEvidenceReviews=int(recorded and review.get('schema', 1) == 1),
                      overdue=int(overdue), releaseReviewRequired=int(required))
        questions.append({'id': q['id'], 'category': q['category'], 'mechanical': bool(mechanical),
                          'manual': bool(review), 'evidenceRecorded': bool(recorded),
                          'evidenceStandard': ('challenged-v2' if review.get('schema') == 2 else 'legacy-v1') if recorded else None,
                          'sourceVerified': bool(verified), 'approved': approved,
                          'openFindingIds': [f['id'] for f in outstanding if q['id'] in f['questionIds']], 'overdue': overdue,
                          'nextReviewAt': review['verification'].get('nextReviewAt') if review and review.get('verification') else None,
                          'releaseReviewRequired': required, 'riskReasons': risks[q['id']]})
    active_ids = {q['id'] for q in corpus}
    fixed = [dict(value, id=key) for key, value in ledger['decisions'].items()
             if value.get('status') == 'fixed' and (key in ledger.get('issues', {}) or key not in {f['id'] for f in findings})]
    return {'schema': 1, 'asOf': as_of, 'corpusHash': digest(corpus), 'active': len(corpus),
            'coverage': dict(counts), 'remainingSourceVerification': len(corpus)-counts['sourceVerified'],
            'remainingApproval': len(corpus)-counts['approved'],
            'wholeCorpusVerified': counts['approved'] == len(corpus),
            'retirementRecords': ledger.get('retirements', {}),
            'changeClassifications': ledger.get('changeClassifications', {}),
            'retiredOrRemovedLedgerIds': sorted(int(k) for k in ledger['questions'] if int(k) not in active_ids),
            'openFindings': outstanding, 'fixedFindings': fixed, 'findings': findings, 'questions': questions}


def gate_errors(corpus, ledger, baseline, as_of, findings=None):
    errors = []
    findings = findings if findings is not None else audit_findings(corpus, ledger)
    outstanding = open_findings(findings, ledger, as_of)
    required = set()
    retired = {q['id']: q for q in read_json(ROOT/'questions/retired.json')}
    active = {q['id'] for q in corpus}
    for key in set(ledger['questions']) | set(baseline['questions']):
        if int(key) not in active and int(key) not in retired:
            errors.append(f'#{key}: removed question must be preserved in questions/retired.json')
        elif int(key) not in active:
            original = {k: v for k, v in retired[int(key)].items() if k != 'replacedBy'}
            expected = ledger['questions'].get(key, {}).get('hash', baseline['questions'].get(key))
            if digest(original) != expected:
                errors.append(f'#{key}: retired snapshot differs from its last recorded active version')
    for q in corpus:
        key, fingerprint = str(q['id']), digest(q)
        entry = ledger['questions'].get(key, {})
        if entry.get('hash') != fingerprint or not valid_date(entry.get('mechanicalAt')) or entry['mechanicalAt'] > as_of:
            errors.append(f"#{key}: missing or stale mechanical record; run sync")
        if baseline['questions'].get(key) != fingerprint:
            required.add(q['id'])
            if not source_verified(entry, q, as_of):
                errors.append(f"#{key}: new/changed question needs current manual review and four-option source verification")
        review = current_review(entry, q, as_of)
        if entry.get('review') and review is None:
            errors.append(f'#{key}: invalid or stale review evidence; re-review the current question')
        if review and review.get('verification') and review['verification'].get('nextReviewAt') \
                and review['verification']['nextReviewAt'] <= as_of:
            errors.append(f"#{key}: scheduled factual recheck is due")
    for finding in outstanding:
        if required.intersection(finding['questionIds']) or finding['kind'] == 'manual':
            errors.append(f"{finding['id']}: undecided/unresolved concern requires a review decision")
    current_ids = {f['id'] for f in findings}
    for key, decision in ledger['decisions'].items():
        if decision.get('status') not in ('accepted', 'unresolved', 'fixed') or not nonblank(decision.get('reason')) \
                or not nonblank(decision.get('reviewer')) or not valid_date(decision.get('at')) \
                or decision['at'] > as_of:
            errors.append(f'{key}: invalid finding decision')
        if decision.get('status') == 'fixed' and not nonblank(decision.get('reference')):
            errors.append(f'{key}: fixed finding needs a fix reference')
        if decision.get('status') == 'fixed' and key in ledger.get('issues', {}):
            for q in corpus:
                if q['id'] in ledger['issues'][key]['questionIds'] and not source_verified(ledger['questions'].get(str(q['id']), {}), q, as_of):
                    errors.append(f'{key}: fixed manual concern needs current four-option verification')
        if decision.get('status') == 'fixed' and key in current_ids and key not in ledger.get('issues', {}):
            errors.append(f'{key}: marked fixed but detector still reproduces it')
    for key, record in ledger.get('retirements', {}).items():
        snapshot = retired.get(int(key))
        if snapshot is None or not valid_retirement(record, snapshot, as_of):
            errors.append(f'#{key}: invalid retirement evidence record')
    return errors


def valid_retirement(record, snapshot=None, as_of=None):
    if not isinstance(record, dict) or not all(nonblank(record.get(k)) for k in ('reviewer', 'reason', 'reference', 'retiredHash')) \
            or not valid_date(record.get('at')) or type(record.get('retiredId')) is not int \
            or (as_of is not None and record['at'] > as_of):
        return False
    if record.get('replacedBy') is None:
        # Retired without a replacement (e.g. not worth its recheck upkeep).
        if record.get('replacementSnapshot') is not None or record.get('replacementHash') is not None:
            return False
    else:
        replacement = record.get('replacementSnapshot')
        if type(record['replacedBy']) is not int or record['retiredId'] == record['replacedBy'] \
                or not isinstance(replacement, dict) \
                or record['replacedBy'] != replacement.get('id') or record.get('replacementHash') != digest(replacement) \
                or not nonblank(replacement.get('question')) or not isinstance(replacement.get('answers'), list) \
                or len(replacement['answers']) != 4 or not all(nonblank(a) for a in replacement['answers']):
            return False
    if snapshot is not None:
        original = {k: v for k, v in snapshot.items() if k != 'replacedBy'}
        if record['retiredId'] != snapshot.get('id') or record['retiredHash'] != digest(original) \
                or snapshot.get('replacedBy') != record['replacedBy']:
            return False
    return True


def change_summary(changed, corpus, classifications, as_of=None):
    by_id = {q['id']: q for q in corpus}
    counts = dict.fromkeys(CHANGE_TYPES, 0)
    unclassified = []
    for qid in changed:
        record = classifications.get(str(qid), {})
        types = record.get('types', [])
        if record.get('hash') != digest(by_id[qid]) or not isinstance(types, list) or not types \
                or any(t not in CHANGE_TYPES for t in types) \
                or not all(nonblank(record.get(k)) for k in ('reviewer', 'reason', 'reference')) \
                or not valid_date(record.get('at')) or (as_of is not None and record['at'] > as_of):
            unclassified.append(qid)
        else:
            for kind in set(types):
                counts[kind] += 1
    return {'edited': len(changed), 'byType': counts, 'unclassifiedIds': unclassified,
            'note': 'Types may overlap; edited is not a count of factual errors.'}


def completion_report(plan, report, corpus, retired, as_of, reviewer, partial=False):
    ids = plan.get('questionIds')
    if plan.get('schema') != 1 or not isinstance(ids, list) or not ids or len(set(ids)) != len(ids) \
            or any(type(i) is not int or str(i) not in plan.get('startingHashes', {}) for i in ids) \
            or not reviewer.strip():
        raise ValueError('invalid or empty audit plan/reviewer')
    by_id = {q['id']: q for q in corpus}
    removed = sorted(set(ids)-set(by_id))
    scope = [q for q in report['questions'] if q['id'] in ids]
    outstanding = [f for f in report['openFindings'] if set(ids).intersection(f['questionIds'])]
    incomplete = [q['id'] for q in scope if not (q['mechanical'] and q['manual'] and q['sourceVerified'])]
    unpreserved = sorted(set(removed)-set(retired))
    retirement_records = report.get('retirementRecords', {})
    undocumented = [i for i in removed if not valid_retirement(retirement_records.get(str(i)),
                    retired.get(i) if isinstance(retired, dict) else None, as_of)]
    changed = sorted(q['id'] for q in corpus if q['id'] in ids and plan['startingHashes'][str(q['id'])] != digest(q))
    changes = change_summary(changed, corpus, report.get('changeClassifications', {}), as_of)
    unresolved_ids = sorted(set(incomplete) | {i for f in outstanding for i in f['questionIds'] if i in ids}
                            | set(unpreserved) | set(undocumented))
    approved = [q for q in scope if q['mechanical'] and q['manual'] and q['sourceVerified']
                and not any(q['id'] in f['questionIds'] for f in outstanding)]
    complete = not (unresolved_ids or changes['unclassifiedIds'])
    result = {'schema': 1, 'at': as_of, 'reviewer': reviewer.strip(), 'plan': plan,
              'status': 'complete-for-scope' if complete else 'partial',
              'scopeCounts': {'planned': len(ids), 'active': len(scope),
                              'reviewed': sum(q['manual'] for q in scope)+len(removed)-len(undocumented),
                              'mechanical': sum(q['mechanical'] for q in scope),
                              'manual': sum(q['manual'] for q in scope),
                              'evidenceRecorded': sum(q.get('evidenceRecorded', q['sourceVerified']) for q in scope),
                              'sourceVerified': sum(q['sourceVerified'] for q in scope),
                              'approved': len(approved), 'edited': len(changed), 'retired': len(removed),
                              'unresolved': len(unresolved_ids)},
              'removedIds': removed, 'unpreservedRemovedIds': unpreserved, 'incompleteIds': incomplete,
              'undocumentedRetirementIds': undocumented, 'unresolvedQuestionIds': unresolved_ids,
              'changeSummary': changes,
              'scopeHashes': {str(i): digest(by_id[i]) for i in ids if i in by_id},
              'changedIds': changed,
              'unresolvedFindings': outstanding, 'report': report}
    if not complete and not partial:
        raise ValueError('scope is incomplete; finish reviews/decisions or use --partial to report remaining work honestly')
    return result


def review_template(q):
    return {'schema': 2, 'questionId': q['id'], 'hash': digest(q), 'questionSnapshot': copy.deepcopy(q),
            'reviewer': '', 'at': today(), 'manual': dict.fromkeys(CHECKS, False), 'notes': '',
            'verification': {'context': '', 'timeSensitive': None, 'nextReviewAt': None,
                             'premise': {'reason': '', 'sources': [{'url': '', 'locator': ''}]},
                             'challenge': {'reviewer': '', 'at': today(), 'premiseChecked': False,
                                           'alternativesExcluded': False, 'notes': ''},
                             'options': [{'answer': a, 'verdict': 'correct' if i == 0 else 'incorrect',
                                          'basis': '', 'reason': '', 'sources': [{'url': '', 'locator': ''}]}
                                         for i, a in enumerate(q['answers'])]}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ledger', type=Path, default=ROOT/'audit/ledger.json')
    ap.add_argument('--baseline', type=Path, default=ROOT/'audit/baseline.json')
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('sync', help='Refresh structural coverage and invalidate changed-question reviews')
    sub.add_parser('check', help='Release gate; does not write files')
    sub.add_parser('status', help='Show sequential audit progress without writing files')
    next_batch = sub.add_parser('next', help='Prepare or resume the next sequential question audit batch')
    next_batch.add_argument('--size', type=int, help='Questions per new batch; the default is in audit/queue.json')
    next_batch.add_argument('--preview', action='store_true', help='Show the next batch without creating any files')
    report = sub.add_parser('report'); report.add_argument('--out', type=Path, required=True)
    report.add_argument('--brief', action='store_true', help='Print one summary line; full report stays on disk')
    report.add_argument('--since', type=Path, help='Print added/changed/resolved open finding IDs since this report')
    view = sub.add_parser('view', help='Read a compact packet or complete deduplicated topic context')
    view.add_argument('--packet', type=Path, default=ROOT/'artifacts/question-audit/current.json')
    view.add_argument('--topic', action='append', default=[], help='Exact topic name; repeat to combine full digests')
    view.add_argument('--ids', nargs='+', type=int, default=[])
    view.add_argument('--out', type=Path)
    notes = sub.add_parser('notes-template', help='Prepare concise evidence notes without approval defaults')
    notes.add_argument('plan', type=Path); notes.add_argument('--out', type=Path, required=True)
    notes.add_argument('--reviewer', required=True)
    notes.add_argument('--ids', nargs='+', type=int, help='Only these planned IDs, e.g. remaining questions in a topic group')
    build = sub.add_parser('build-reviews', help='Expand explicit evidence notes to validated reviews; does not record them')
    build.add_argument('notes', type=Path); build.add_argument('--sources', type=Path, required=True)
    build.add_argument('--out', type=Path, required=True)
    sources = sub.add_parser('sources', help='Validate and search reusable source notes; never grants approval')
    sources.add_argument('file', type=Path); sources.add_argument('--query', default='')
    sources.add_argument('--ids', nargs='+', default=[])
    plan = sub.add_parser('plan')
    plan.add_argument('--out', type=Path, required=True); plan.add_argument('--seed', required=True)
    plan.add_argument('--limit', type=int, default=30); plan.add_argument('--sample-per-category', type=int, default=3)
    template = sub.add_parser('template'); template.add_argument('id', type=int); template.add_argument('--out', type=Path, required=True)
    record = sub.add_parser('record'); record.add_argument('file', type=Path)
    many = sub.add_parser('record-many', help='Validate all supplied reviews before one ledger write')
    many.add_argument('files', nargs='+', type=Path)
    for command in ('retire', 'record-retirement'):
        retirement = sub.add_parser(command, help='Preserve a retired snapshot and evidence, or document an existing retirement')
        retirement.add_argument('id', type=int)
        replacement = retirement.add_mutually_exclusive_group(required=True)
        replacement.add_argument('--replaced-by', type=int, help='Active question that keeps the fact (duplicates)')
        replacement.add_argument('--no-replacement', action='store_true',
                                 help='Retire without a replacement, e.g. not worth its recheck upkeep')
        retirement.add_argument('--reviewer', required=True)
        retirement.add_argument('--reason', required=True)
        retirement.add_argument('--reference', required=True)
    reschedule = sub.add_parser('reschedule', help='Re-tier recheck dates of current reviews (rule 7); evidence unchanged')
    reschedule.add_argument('file', type=Path)
    sub.add_parser('recover-retirement', help='Roll back a process-interrupted retirement transaction')
    classify = sub.add_parser('classify', help='Classify an edit without implying source approval')
    classify.add_argument('id', type=int)
    classify.add_argument('--type', action='append', dest='types', choices=CHANGE_TYPES, required=True)
    classify.add_argument('--reason', required=True); classify.add_argument('--reviewer', required=True)
    classify.add_argument('--reference', required=True)
    issue = sub.add_parser('issue', help='Track a concern discovered outside detector patterns')
    issue.add_argument('id', type=int); issue.add_argument('--reason', required=True); issue.add_argument('--reviewer', required=True)
    decide = sub.add_parser('decide')
    decide.add_argument('finding'); decide.add_argument('status', choices=['accepted', 'unresolved', 'fixed'])
    decide.add_argument('--reason', required=True); decide.add_argument('--reviewer', required=True)
    decide.add_argument('--reference', default='')
    close = sub.add_parser('close')
    close.add_argument('plan', type=Path); close.add_argument('--out', type=Path, required=True)
    close.add_argument('--reviewer', required=True); close.add_argument('--partial', action='store_true')
    args = ap.parse_args(argv)
    try:
        from question_audit_operations import transaction_path, recover_retirement
        # A transaction can be interrupted between shard and snapshot writes.
        # Recovery must therefore run before structural validation of that state.
        if args.command == 'recover-retirement':
            recover_retirement(ROOT)
            print('Interrupted retirement rolled back; rerun sync/report/check.')
            return 0
        if transaction_path(ROOT).exists():
            raise ValueError('interrupted retirement: run recover-retirement before continuing')
        # Every workflow entry point starts with the same structural check.
        from validate_corpus import main as validate_corpus
        if validate_corpus():
            return 1
        corpus, as_of = load_corpus(), today()
        ledger, baseline = read_json(args.ledger), read_json(args.baseline)
        if ledger.get('schema') != 1 or baseline.get('schema') != 1:
            raise ValueError('unsupported ledger/baseline schema')
        by_id = {q['id']: q for q in corpus}
        if args.command in ('view', 'notes-template', 'build-reviews', 'sources'):
            from question_audit_compact import reading_view, notes_template, build_reviews, source_library
            if args.command == 'view':
                value = reading_view(read_json(args.packet), ROOT, args.topic, args.ids)
                if args.out:
                    write_json(args.out, value)
                else:
                    print(json.dumps(value, ensure_ascii=False, separators=(',', ':')))
            elif args.command == 'notes-template':
                if args.out.exists():
                    raise ValueError('refusing to overwrite saved evidence notes; choose a new output path')
                write_json(args.out, notes_template(corpus, read_json(args.plan), args.reviewer, as_of, args.ids))
                print(f'Notes template: {args.out}; no checks or evidence inferred.')
            elif args.command == 'build-reviews':
                value = build_reviews(read_json(args.notes), read_json(args.sources), corpus, ledger, as_of)
                write_json(args.out, value)
                print(f'Built {len(value)} validated reviews: {args.out}; use record-many to import.')
            else:
                library = source_library(read_json(args.file), as_of)
                if set(args.ids) - library.keys():
                    raise ValueError('unknown source IDs')
                for key, source in library.items():
                    if args.ids and key not in args.ids:
                        continue
                    if args.query.casefold() not in (key+' '+json.dumps(source, ensure_ascii=False)).casefold():
                        continue
                    due = bool(source.get('nextReviewAt') and source['nextReviewAt'] <= as_of)
                    print(json.dumps({'id': key, 'due': due, **source}, ensure_ascii=False, separators=(',', ':')))
        elif args.command == 'sync':
            write_json(args.ledger, sync_ledger(corpus, ledger, as_of))
            print(f'Structural coverage refreshed for {len(corpus)} questions; no manual/source verification inferred.')
        elif args.command == 'template':
            write_json(args.out, review_template(by_id[args.id]))
        elif args.command in ('record', 'record-many'):
            files = [args.file] if args.command == 'record' else args.files
            reviews = []
            for file in files:
                value = read_json(file)
                reviews.extend(value if isinstance(value, list) else [value])
            updated = record_reviews(corpus, ledger, reviews, as_of)
            write_json(args.ledger, updated)
            print(f'Recorded {len(reviews)} review(s); source support remains an editorial judgment.')
        elif args.command in ('retire', 'record-retirement'):
            from question_audit_operations import retire_question
            retire_question(ROOT, args.ledger, args.id, args.replaced_by, args.reviewer, args.reason,
                            args.reference, as_of, preserved=args.command == 'record-retirement')
            target = f'#{args.replaced_by}' if args.replaced_by is not None else 'no replacement'
            print(f'Retirement #{args.id} -> {target} recorded; original snapshot and history preserved.')
            # Structural checks and fresh warnings immediately follow the mutation.
            if validate_corpus():
                return 1
            refreshed = audit_report(load_corpus(), read_json(args.ledger), baseline, as_of)
            write_json(ROOT/'artifacts/question-audit.json', refreshed)
            print(f"Refreshed report: {len(refreshed['openFindings'])} advisory findings; review applicable decisions before closing.")
        elif args.command == 'reschedule':
            from question_audit_operations import reschedule_reviews
            request = read_json(args.file)
            updated = reschedule_reviews(corpus, ledger, request, as_of)
            write_json(args.ledger, updated)
            tiers = Counter(item['tier'] for item in request['items'])
            print(f"Rescheduled {len(request['items'])} recheck(s): "+', '.join(f'{k} {v}' for k, v in sorted(tiers.items()))
                  + '; recorded evidence unchanged, sources not re-inspected.')
        elif args.command == 'classify':
            from question_audit_operations import classify_change
            updated = classify_change(corpus, ledger, args.id, args.types, args.reviewer,
                                      args.reason, args.reference, as_of)
            write_json(args.ledger, updated)
            print(f'Classified #{args.id}: '+', '.join(sorted(set(args.types))))
        elif args.command == 'plan':
            if args.limit < 0 or args.sample_per_category < 0 or not args.seed.strip():
                raise ValueError('budgets must be nonnegative and seed must be nonempty')
            value = make_plan(corpus, ledger, as_of, args.seed, args.limit, args.sample_per_category)
            write_json(args.out, value)
            print(f"Selected {len(value['questionIds'])} questions, including {len(value['randomSampleIds'])} outside risk patterns.")
        elif args.command == 'issue':
            q = by_id[args.id]
            if not args.reason.strip() or not args.reviewer.strip():
                raise ValueError('reason and reviewer must be nonempty')
            key = 'manual-' + digest({'question': digest(q), 'reason': args.reason.strip()})[:20]
            issues = ledger.setdefault('issues', {})
            if key in issues:
                raise ValueError(f'concern already tracked: {key}')
            issues[key] = {'questionIds': [q['id']], 'reason': args.reason.strip(), 'reviewer': args.reviewer.strip(),
                           'at': as_of, 'questionSnapshot': q,
                           'reviewHashAtIssue': digest(ledger['questions'].get(str(q['id']), {}).get('review'))}
            finding = next(f for f in audit_findings(corpus, ledger) if f['id'] == key)
            ledger['decisions'][key] = {'signature': finding['signature'], 'questionIds': [q['id']], 'status': 'unresolved',
                                       'reason': args.reason.strip(), 'reviewer': args.reviewer.strip(), 'at': as_of, 'history': []}
            write_json(args.ledger, ledger)
            print(f'Tracked concern: {key}')
        elif args.command == 'decide':
            findings = {f['id']: f for f in audit_findings(corpus, ledger)}
            if not args.reason.strip() or not args.reviewer.strip():
                raise ValueError('reason and reviewer must be nonempty')
            if args.finding in ledger.get('issues', {}) and args.status in ('fixed', 'accepted'):
                issue = ledger['issues'][args.finding]
                if not args.reference.strip():
                    raise ValueError('closing a manual concern requires an evidence reference')
                for qid in issue['questionIds']:
                    if qid not in by_id:
                        continue
                    review = current_review(ledger['questions'].get(str(qid), {}), by_id[qid], as_of)
                    if not source_verified(ledger['questions'].get(str(qid), {}), by_id[qid], as_of) \
                            or review.get('schema') != 2:
                        raise ValueError('closing a manual concern requires a current schema-2 evidence challenge')
                    if issue.get('reviewHashAtIssue') == digest(review):
                        raise ValueError('renew the evidence review after the manual concern was raised')
            if args.status == 'fixed':
                manual = args.finding in ledger.get('issues', {})
                if (args.finding in findings and not manual) or args.finding not in ledger['decisions']:
                    raise ValueError('record the warning as unresolved first; fixed requires it to disappear on recheck')
                if not args.reference.strip():
                    raise ValueError('fixed decisions require a fix reference')
                finding = findings.get(args.finding, ledger['decisions'][args.finding])
                if manual and any(not source_verified(ledger['questions'].get(str(i), {}), by_id[i], as_of)
                                  for i in finding['questionIds'] if i in by_id):
                    raise ValueError('closing a manually found defect requires current four-option verification')
            else:
                finding = findings[args.finding]
            previous = ledger['decisions'].get(args.finding)
            ledger['decisions'][args.finding] = {'signature': finding['signature'], 'questionIds': finding['questionIds'],
                'status': args.status, 'at': as_of, 'reviewer': args.reviewer.strip(),
                'reason': args.reason.strip(), 'reference': args.reference.strip(),
                'history': ([{k: v for k, v in previous.items() if k != 'history'}] + previous.get('history', [])) if previous else []}
            write_json(args.ledger, ledger)
        else:
            report = audit_report(corpus, ledger, baseline, as_of)
            if args.command in ('next', 'status'):
                from question_audit_queue import prepare_next, print_status
                preview = args.command == 'status' or args.preview
                state = prepare_next(ROOT, corpus, ledger, report, as_of,
                                     getattr(args, 'size', None), preview=preview)
                print_status(state, preview=preview)
                calendar = recheck_calendar(report, as_of)
                print(f"Scheduled rechecks: {calendar['overdue']} overdue; next 12 months "
                      + (', '.join(f'{m}: {n}' for m, n in calendar['byMonth'].items()) or 'none')
                      + f"; {calendar['later']} later.")
            elif args.command == 'report':
                from question_audit_compact import finding_changes
                changes = finding_changes(read_json(args.since), report) if args.since else None
                write_json(args.out, report)
                if args.brief:
                    print(f"Audit: {report['active']} active; {report['remainingApproval']} awaiting approval; "
                          f"{report['remainingSourceVerification']} awaiting sources; {len(report['openFindings'])} open findings. Full report: {args.out}")
                else:
                    print(json.dumps({k: report[k] for k in ('active', 'coverage', 'remainingSourceVerification', 'remainingApproval')}, indent=2))
                    print(f"Open advisory findings: {len(report['openFindings'])}")
                if changes is not None:
                    print('Finding changes: '+json.dumps(changes, separators=(',', ':')))
            elif args.command == 'check':
                errors = gate_errors(corpus, ledger, baseline, as_of, report['findings'])
                for error in errors:
                    print('ERROR ' + error)
                print(f"Audit gate: {len(errors)} errors; {report['remainingSourceVerification']} questions remain without current source verification.")
                return int(bool(errors))
            elif args.command == 'close':
                from question_audit_operations import save_completion
                plan = read_json(args.plan)
                retired = {q['id']: q for q in read_json(ROOT/'questions/retired.json')}
                result = completion_report(plan, report, corpus, retired, as_of, args.reviewer, args.partial)
                save_completion(args.out, result)
                counts = result['scopeCounts']
                print(f"Audit {result['status']}; {counts['reviewed']} reviewed, {counts['approved']} approved, "
                      f"{counts['edited']} edited, {counts['retired']} retired, {counts['unresolved']} unresolved questions.")
                print('Edit types (may overlap): '+json.dumps(result['changeSummary']['byType']))
                if result['changeSummary']['unclassifiedIds']:
                    print('Unclassified edits: '+str(result['changeSummary']['unclassifiedIds']))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
