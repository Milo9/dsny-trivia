"""Explicit editorial mutations, with preserved evidence and retirement recovery."""
import copy
import json
from pathlib import Path


def inside(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    if not path.is_relative_to(root):
        raise ValueError('editorial transaction paths must stay inside the project')
    return path


def transaction_path(root):
    return inside(root, Path(root)/'artifacts/question-audit/retirement-pending.json')


def _replace_text(path, contents):
    path = Path(path)
    temp = path.with_suffix(path.suffix+'.transaction-tmp')
    temp.write_text(contents, encoding='utf-8', newline='')
    temp.replace(path)


def recover_retirement(root):
    """Rollback a process-interrupted transaction before any further audit work."""
    from question_audit import read_json
    journal = transaction_path(root)
    value = read_json(journal)
    if value.get('schema') != 1 or not isinstance(value.get('files'), list) or not value['files']:
        raise ValueError('invalid retirement recovery journal')
    entries = []
    for item in value['files']:
        if not isinstance(item, dict) or not isinstance(item.get('original'), str) \
                or not isinstance(item.get('path'), str):
            raise ValueError('invalid retirement recovery entry')
        path = inside(root, Path(root)/item['path'])
        if path == journal.resolve():
            raise ValueError('recovery journal cannot overwrite itself')
        entries.append((path, item['original']))
    if len({p for p, _ in entries}) != len(entries):
        raise ValueError('duplicate recovery destinations')
    for path, contents in entries:
        _replace_text(path, contents)
    journal.unlink()


def commit_retirement(root, changes):
    """Write-ahead journal plus rollback; filesystem multi-file writes aren't atomic."""
    from question_audit import write_json
    journal = transaction_path(root)
    if journal.exists():
        raise ValueError('pending retirement; run recover-retirement first')
    entries = []
    for path, contents in changes.items():
        path = inside(root, path)
        with path.open(encoding='utf-8', newline='') as stream:
            original = stream.read()
        entries.append({'path': str(path.relative_to(Path(root).resolve())),
                        'original': original,
                        'updated': contents})
    write_json(journal, {'schema': 1, 'files': entries})
    try:
        for item in entries:
            _replace_text(Path(root)/item['path'], item['updated'])
        journal.unlink()
    except OSError:
        # A hard process stop leaves the journal for explicit recovery instead.
        recover_retirement(root)
        raise


def retirement_record(original, replacement, reviewer, reason, reference, as_of):
    """replacement is the active question keeping the fact, or None (no replacement)."""
    from question_audit import digest, nonblank
    if not all(nonblank(v) for v in (reviewer, reason, reference)):
        raise ValueError('retirement needs reviewer, rationale and evidence reference')
    if replacement is not None and original['id'] == replacement['id']:
        raise ValueError('a retired question cannot replace itself')
    return {'retiredId': original['id'], 'retiredHash': digest(original),
            'replacedBy': replacement['id'] if replacement else None,
            'replacementHash': digest(replacement) if replacement else None,
            'replacementSnapshot': copy.deepcopy(replacement), 'reviewer': reviewer.strip(),
            'reason': reason.strip(), 'reference': reference.strip(), 'at': as_of}


def retire_question(root, ledger_path, qid, replacement_id, reviewer, reason, reference, as_of, preserved=False):
    """Retire one active question, or document an already preserved retirement."""
    import question_audit as audit
    root = Path(root).resolve()
    ledger_path = inside(root, ledger_path)
    manifest = audit.read_json(root/'questions/manifest.json')
    shards = [(inside(root, root/name), audit.read_json(inside(root, root/name))) for name in manifest['shards']]
    retired_path = inside(root, root/manifest.get('retired', 'questions/retired.json'))
    retired = audit.read_json(retired_path)
    ledger = audit.read_json(ledger_path)
    corpus = [q for _, qs in shards for q in qs]
    by_id = {q['id']: q for q in corpus}
    if replacement_id is not None and replacement_id not in by_id:
        raise ValueError('replacement must be an active question')
    if preserved:
        if qid in by_id:
            raise ValueError('record-retirement requires an already retired question; use retire')
        snapshot = next((q for q in retired if q['id'] == qid), None)
        if snapshot is None or snapshot.get('replacedBy') != replacement_id:  # both None without replacement
            raise ValueError('preserved snapshot/replacedBy does not match')
        original = {k: v for k, v in snapshot.items() if k != 'replacedBy'}
    else:
        if qid not in by_id or any(q['id'] == qid for q in retired):
            raise ValueError('retire requires an active ID absent from retired snapshots')
        original = by_id[qid]
    replacement = by_id[replacement_id] if replacement_id is not None else None
    record = retirement_record(original, replacement, reviewer, reason, reference, as_of)
    entry = ledger.get('questions', {}).get(str(qid), {})
    expected = entry.get('hash') or audit.read_json(root/'audit/baseline.json').get('questions', {}).get(str(qid))
    if expected and expected != audit.digest(original):
        raise ValueError('retirement snapshot differs from the ledger; run sync and recheck before retiring')
    records = ledger.setdefault('retirements', {})
    previous = records.get(str(qid))
    record['history'] = ([{k: v for k, v in previous.items() if k != 'history'}]+previous.get('history', [])) if previous else []
    records[str(qid)] = record
    audit.sync_ledger(corpus, ledger, as_of)
    serialize = lambda value: json.dumps(value, ensure_ascii=False, indent=2)+'\n'
    changes = {ledger_path: serialize(ledger)}
    if not preserved:
        retired.append(dict(copy.deepcopy(original), **({'replacedBy': replacement_id} if replacement_id is not None else {})))
        changes[retired_path] = serialize(retired)
        path, qs = next((path, qs) for path, qs in shards if any(q['id'] == qid for q in qs))
        remaining = [q for q in qs if q['id'] != qid]
        changes[path] = '[\n'+',\n'.join(json.dumps(q, ensure_ascii=False) for q in remaining)+'\n]\n'
    commit_retirement(root, changes)
    return record


def classify_change(corpus, ledger, qid, kinds, reviewer, reason, reference, as_of):
    from question_audit import CHANGE_TYPES, digest, nonblank
    if not kinds or any(kind not in CHANGE_TYPES for kind in kinds) \
            or not all(nonblank(v) for v in (reviewer, reason, reference)):
        raise ValueError('classification requires supported types, reviewer, reason and reference')
    q = next((q for q in corpus if q['id'] == qid), None)
    if q is None:
        raise ValueError('classify requires an active question')
    updated = copy.deepcopy(ledger)
    records = updated.setdefault('changeClassifications', {})
    previous = records.get(str(qid))
    records[str(qid)] = {'hash': digest(q), 'types': sorted(set(kinds)), 'reason': reason.strip(),
        'reviewer': reviewer.strip(), 'reference': reference.strip(), 'at': as_of,
        'history': ([{k: v for k, v in previous.items() if k != 'history'}]+previous.get('history', [])) if previous else []}
    return updated


def save_completion(path, result):
    from question_audit import digest, read_json, write_json
    path = Path(path)
    if path.exists():
        previous = read_json(path)
        if previous != result:
            archive = path.parent/(path.stem+'-history')/(digest(previous)+'.json')
            if not archive.exists():
                write_json(archive, previous)
    write_json(path, result)


SCHEDULE_TIERS = ('historical', 'stable', 'changeable')


def reschedule_reviews(corpus, ledger, request, as_of):
    """Re-tier recheck dates of current reviews under rule 7, without touching evidence.

    Only timeSensitive/nextReviewAt change. The prior review moves to history and the
    new one carries a 'schedule' record stating the tier, reason, actor and that no
    source was re-inspected. Due rechecks must be performed, not rescheduled; the new
    date is bounded by the tier interval from the recorded evidence date. Validates
    every item before returning a changed copy (no partial writes).
    """
    from datetime import date, timedelta
    from question_audit import (RECHECK_TIERS, current_review, evidence_date, nonblank,
                                valid_date, validate_review)
    if not isinstance(request, dict) or request.get('schema') != 1 or not nonblank(request.get('reviewer')) \
            or not isinstance(request.get('items'), list) or not request['items']:
        raise ValueError('reschedule file needs schema 1, a reviewer and a nonempty items array')
    by_id = {q['id']: q for q in corpus}
    updated = copy.deepcopy(ledger)
    seen = set()
    for item in request['items']:
        qid = item.get('questionId') if isinstance(item, dict) else None
        if type(qid) is not int or qid not in by_id:
            raise ValueError(f'#{qid}: not an active question')
        if qid in seen:
            raise ValueError(f'#{qid}: listed twice')
        seen.add(qid)
        tier, due = item.get('tier'), item.get('nextReviewAt')
        if tier not in SCHEDULE_TIERS:
            raise ValueError(f'#{qid}: tier must be one of {", ".join(SCHEDULE_TIERS)}')
        if not nonblank(item.get('reason')):
            raise ValueError(f'#{qid}: a volatility reason is required')
        entry = updated['questions'].get(str(qid), {})
        review = current_review(entry, by_id[qid], as_of)
        if not review or not review.get('verification'):
            raise ValueError(f'#{qid}: needs a current source-verified review to reschedule')
        previous = {k: review['verification'].get(k) for k in ('timeSensitive', 'nextReviewAt')}
        if previous['nextReviewAt'] and previous['nextReviewAt'] <= as_of:
            raise ValueError(f'#{qid}: recheck is already due; perform it instead of rescheduling')
        if tier == 'historical':
            if due is not None:
                raise ValueError(f'#{qid}: historical facts take no recheck date')
        else:
            if not valid_date(due) or due <= as_of:
                raise ValueError(f'#{qid}: {tier} needs a future nextReviewAt')
            limit = date.fromisoformat(evidence_date(review)) + timedelta(days=RECHECK_TIERS[tier])
            if date.fromisoformat(due) > limit:
                raise ValueError(f'#{qid}: {tier} recheck must fall by {limit.isoformat()} '
                                 f'({RECHECK_TIERS[tier]} days after the evidence date)')
        new = copy.deepcopy(review)
        new['verification'].update(timeSensitive=tier != 'historical', nextReviewAt=due)
        new['schedule'] = {'tier': tier, 'reason': item['reason'].strip(), 'reviewer': request['reviewer'].strip(),
                           'at': as_of, 'evidenceDate': evidence_date(review), 'sourcesReinspected': False,
                           'previous': previous}
        errors = validate_review(new, as_of)
        if errors:
            raise ValueError(f'#{qid}: ' + '; '.join(errors))
        entry['history'].append({'hash': entry['hash'], 'review': entry['review']})
        entry['review'] = new
    return updated
