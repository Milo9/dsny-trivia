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
    from question_audit import digest, nonblank
    if not all(nonblank(v) for v in (reviewer, reason, reference)):
        raise ValueError('retirement needs reviewer, duplicate rationale and evidence reference')
    if original['id'] == replacement['id']:
        raise ValueError('a retired question cannot replace itself')
    return {'retiredId': original['id'], 'retiredHash': digest(original),
            'replacedBy': replacement['id'], 'replacementHash': digest(replacement),
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
    if replacement_id not in by_id:
        raise ValueError('replacement must be an active question')
    if preserved:
        if qid in by_id:
            raise ValueError('record-retirement requires an already retired question; use retire')
        snapshot = next((q for q in retired if q['id'] == qid), None)
        if snapshot is None or snapshot.get('replacedBy') != replacement_id:
            raise ValueError('preserved snapshot/replacedBy does not match')
        original = {k: v for k, v in snapshot.items() if k != 'replacedBy'}
    else:
        if qid not in by_id or any(q['id'] == qid for q in retired):
            raise ValueError('retire requires an active ID absent from retired snapshots')
        original = by_id[qid]
    record = retirement_record(original, by_id[replacement_id], reviewer, reason, reference, as_of)
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
        retired.append(dict(copy.deepcopy(original), replacedBy=replacement_id))
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
