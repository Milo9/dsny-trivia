"""Version-bound question audit ledger, triage, sampling, decisions and release gate.

No command searches the web or claims facts have been verified automatically.
Only sync, record and decide change the ledger; shards are always read-only.
See QUESTION_AUDIT.md for the editorial procedure and command examples.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
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
    """Reject incomplete review evidence, including an unsupported distractor."""
    errors = []
    if not isinstance(review, dict):
        return ['review must be an object']
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
                sources = option.get('sources')
                if not isinstance(sources, list) or not sources:
                    errors.append(f'option {i} needs supporting sources')
                elif any(not isinstance(s, dict) or not https(s.get('url'))
                         or not nonblank(s.get('locator')) for s in sources):
                    errors.append(f'option {i} sources need HTTPS URLs and specific evidence locators')
    return errors


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
    for a, b in sorted(pairs):
        add('duplicate', [a, b], 'Could memorizing one answer solve the other without learning a new fact?')
    return sorted(findings.values(), key=lambda f: f['id'])


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
    risks = risk_map(corpus)
    counts = Counter()
    questions = []
    for q in corpus:
        key = str(q['id'])
        entry = ledger['questions'].get(key, {})
        review = current_review(entry, q, as_of)
        mechanical = entry.get('hash') == digest(q) and valid_date(entry.get('mechanicalAt')) and entry['mechanicalAt'] <= as_of
        verified = source_verified(entry, q, as_of)
        overdue = bool(review and review.get('verification') and review['verification'].get('nextReviewAt')
                       and review['verification']['nextReviewAt'] <= as_of)
        required = baseline['questions'].get(key) != digest(q)
        counts.update(mechanical=int(mechanical), manual=int(bool(review)), sourceVerified=int(verified),
                      overdue=int(overdue), releaseReviewRequired=int(required))
        questions.append({'id': q['id'], 'category': q['category'], 'mechanical': bool(mechanical),
                          'manual': bool(review), 'sourceVerified': bool(verified), 'overdue': overdue,
                          'nextReviewAt': review['verification'].get('nextReviewAt') if review and review.get('verification') else None,
                          'releaseReviewRequired': required, 'riskReasons': risks[q['id']]})
    active_ids = {q['id'] for q in corpus}
    fixed = [dict(value, id=key) for key, value in ledger['decisions'].items()
             if value.get('status') == 'fixed' and (key in ledger.get('issues', {}) or key not in {f['id'] for f in findings})]
    return {'schema': 1, 'asOf': as_of, 'corpusHash': digest(corpus), 'active': len(corpus),
            'coverage': dict(counts), 'remainingSourceVerification': len(corpus)-counts['sourceVerified'],
            'wholeCorpusVerified': counts['sourceVerified'] == len(corpus),
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
    return errors


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
    complete = not (incomplete or outstanding or unpreserved)
    result = {'schema': 1, 'at': as_of, 'reviewer': reviewer.strip(), 'plan': plan,
              'status': 'complete-for-scope' if complete else 'partial',
              'scopeCounts': {'planned': len(ids), 'mechanical': sum(q['mechanical'] for q in scope),
                              'manual': sum(q['manual'] for q in scope), 'sourceVerified': sum(q['sourceVerified'] for q in scope)},
              'removedIds': removed, 'unpreservedRemovedIds': unpreserved, 'incompleteIds': incomplete,
              'changedIds': sorted(q['id'] for q in corpus if q['id'] in ids and plan['startingHashes'][str(q['id'])] != digest(q)),
              'unresolvedFindings': outstanding, 'report': report}
    if not complete and not partial:
        raise ValueError('scope is incomplete; finish reviews/decisions or use --partial to report remaining work honestly')
    return result


def review_template(q):
    return {'questionId': q['id'], 'hash': digest(q), 'questionSnapshot': q,
            'reviewer': '', 'at': today(), 'manual': dict.fromkeys(CHECKS, False), 'notes': '',
            'verification': {'context': '', 'timeSensitive': None, 'nextReviewAt': None,
                             'options': [{'answer': a, 'verdict': 'correct' if i == 0 else 'incorrect',
                                          'reason': '', 'sources': [{'url': '', 'locator': ''}]}
                                         for i, a in enumerate(q['answers'])]}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--ledger', type=Path, default=ROOT/'audit/ledger.json')
    ap.add_argument('--baseline', type=Path, default=ROOT/'audit/baseline.json')
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('sync', help='Refresh structural coverage and invalidate changed-question reviews')
    sub.add_parser('check', help='Release gate; does not write files')
    report = sub.add_parser('report'); report.add_argument('--out', type=Path, required=True)
    plan = sub.add_parser('plan')
    plan.add_argument('--out', type=Path, required=True); plan.add_argument('--seed', required=True)
    plan.add_argument('--limit', type=int, default=30); plan.add_argument('--sample-per-category', type=int, default=3)
    template = sub.add_parser('template'); template.add_argument('id', type=int); template.add_argument('--out', type=Path, required=True)
    record = sub.add_parser('record'); record.add_argument('file', type=Path)
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
        # Every workflow entry point starts with the same structural check.
        from validate_corpus import main as validate_corpus
        if validate_corpus():
            return 1
        corpus, as_of = load_corpus(), today()
        ledger, baseline = read_json(args.ledger), read_json(args.baseline)
        if ledger.get('schema') != 1 or baseline.get('schema') != 1:
            raise ValueError('unsupported ledger/baseline schema')
        by_id = {q['id']: q for q in corpus}
        if args.command == 'sync':
            write_json(args.ledger, sync_ledger(corpus, ledger, as_of))
            print(f'Structural coverage refreshed for {len(corpus)} questions; no manual/source verification inferred.')
        elif args.command == 'template':
            write_json(args.out, review_template(by_id[args.id]))
        elif args.command == 'record':
            review = read_json(args.file)
            q = by_id[review['questionId']]
            if review.get('hash') != digest(q) or review.get('questionSnapshot') != q:
                raise ValueError('question changed since template creation; re-review its current version')
            errors = validate_review(review, as_of)
            if not errors and review.get('verification') and [o.get('answer') for o in review['verification']['options']] != q['answers']:
                errors.append('option evidence must match current answers in their stored order')
            if errors:
                raise ValueError('; '.join(errors))
            sync_ledger(corpus, ledger, as_of)
            entry = ledger['questions'][str(q['id'])]
            if entry.get('review'):
                entry['history'].append({'hash': entry['hash'], 'review': entry['review']})
            entry['review'] = review
            write_json(args.ledger, ledger)
            print(f"Recorded review for #{q['id']}.")
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
                           'at': as_of, 'questionSnapshot': q}
            finding = next(f for f in audit_findings(corpus, ledger) if f['id'] == key)
            ledger['decisions'][key] = {'signature': finding['signature'], 'questionIds': [q['id']], 'status': 'unresolved',
                                       'reason': args.reason.strip(), 'reviewer': args.reviewer.strip(), 'at': as_of, 'history': []}
            write_json(args.ledger, ledger)
            print(f'Tracked concern: {key}')
        elif args.command == 'decide':
            findings = {f['id']: f for f in audit_findings(corpus, ledger)}
            if not args.reason.strip() or not args.reviewer.strip():
                raise ValueError('reason and reviewer must be nonempty')
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
            if args.command == 'report':
                write_json(args.out, report)
                print(json.dumps({k: report[k] for k in ('active', 'coverage', 'remainingSourceVerification')}, indent=2))
                print(f"Open advisory findings: {len(report['openFindings'])}")
            elif args.command == 'check':
                errors = gate_errors(corpus, ledger, baseline, as_of, report['findings'])
                for error in errors:
                    print('ERROR ' + error)
                print(f"Audit gate: {len(errors)} errors; {report['remainingSourceVerification']} questions remain without current source verification.")
                return int(bool(errors))
            elif args.command == 'close':
                plan = read_json(args.plan)
                retired = {q['id'] for q in read_json(ROOT/'questions/retired.json')}
                result = completion_report(plan, report, corpus, retired, as_of, args.reviewer, args.partial)
                write_json(args.out, result)
                print(f"Audit {result['status']}; {len(result['incompleteIds'])} incomplete questions, {len(result['unresolvedFindings'])} unresolved warnings in scope.")
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
