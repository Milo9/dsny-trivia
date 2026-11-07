"""Resumable, manifest-ordered editorial batches for 'audit the next shard'."""
from pathlib import Path

from question_audit import completion_report, current_review, digest, read_json, review_template, write_json
from question_audit_recon import comparison_questions, topic_digests


def workspace_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('audit queue paths must stay inside the project')
    return path


def read_shards(root):
    manifest = read_json(root / 'questions/manifest.json')
    return [(name, read_json(workspace_path(root, name))) for name in manifest['shards']]


def queue_state(root, corpus, report, as_of, size=None):
    root = Path(root)
    config = read_json(root / 'audit/queue.json')
    if config.get('schema') != 1:
        raise ValueError('unsupported audit queue schema')
    batch_size = config['batchSize'] if size is None else size
    if type(batch_size) is not int or not 1 <= batch_size <= 250:
        raise ValueError('audit batch size must be between 1 and 250')
    runs = workspace_path(root, config['runsDirectory'])
    packet_path = workspace_path(root, config['workPacket'])
    blocked = {i for finding in report['openFindings'] for i in finding['questionIds']}
    done = {q['id'] for q in report['questions'] if q['mechanical'] and q['manual']
            and q['sourceVerified'] and q['id'] not in blocked}
    shards = read_shards(root)
    retired = {q['id']: q for q in read_json(root / 'questions/retired.json')}
    progress = [{'shard': name, 'total': len(qs), 'complete': sum(q['id'] in done for q in qs),
                 'remaining': sum(q['id'] not in done for q in qs)} for name, qs in shards]
    state = {'schema': 1, 'asOf': as_of, 'batchSize': batch_size,
             'progress': {'total': len(corpus), 'complete': len(done), 'remaining': len(corpus)-len(done)},
             'shards': progress, 'workPacketPath': str(packet_path.relative_to(root.resolve()))}
    state['recordedEvidence'] = report['coverage']['evidenceRecorded'] if 'coverage' in report and 'evidenceRecorded' in report['coverage'] \
        else sum(q['sourceVerified'] for q in report['questions'])
    saved = []
    for path in runs.glob('next-shard-*-plan.json'):
        plan = read_json(path)
        if plan.get('workflow') != 'next-shard' or type(plan.get('sequence')) is not int or plan['sequence'] < 1:
            raise ValueError(f'invalid sequential audit plan: {path.name}')
        if path.name != f"next-shard-{plan['sequence']:04d}-plan.json":
            raise ValueError(f'audit plan sequence/filename mismatch: {path.name}')
        saved.append((plan['sequence'], path, plan))
    if len({sequence for sequence, _, _ in saved}) != len(saved):
        raise ValueError('duplicate sequential audit plan numbers')
    for _, path, plan in sorted(saved):
        result_path = path.with_name(path.name.replace('-plan.json', '-result.json'))
        live = completion_report(plan, report, corpus, retired, as_of, 'Queue status', partial=True)
        result = read_json(result_path) if result_path.exists() else None
        closed = (result is not None and result.get('status') == 'complete-for-scope'
                  and result.get('plan') == plan and live['status'] == 'complete-for-scope'
                  and result.get('scopeHashes') == live['scopeHashes']
                  and result.get('removedIds') == live['removedIds'])
        if not closed:
            remaining = [i for i in plan['questionIds'] if i not in done and i not in retired]
            return dict(state, status='awaiting-close' if live['status'] == 'complete-for-scope' else 'resume',
                        plan=plan, planPath=str(path.relative_to(root.resolve())),
                        resultPath=str(result_path.relative_to(root.resolve())), remainingQuestionIds=remaining,
                        unpreservedRemovedIds=live['unpreservedRemovedIds'],
                        undocumentedRetirementIds=live['undocumentedRetirementIds'],
                        unclassifiedChangeIds=live['changeSummary']['unclassifiedIds'])
    for name, qs in shards:
        selected = [q for q in qs if q['id'] not in done][:batch_size]
        if not selected:
            continue
        sequence = max((s for s, _, _ in saved), default=0)+1
        path = runs / f'next-shard-{sequence:04d}-plan.json'
        plan = {'schema': 1, 'workflow': 'next-shard', 'sequence': sequence, 'createdAt': as_of,
                'sourceShard': name, 'batchSize': batch_size, 'corpusHash': digest(corpus),
                'population': len(corpus), 'questionIds': [q['id'] for q in selected],
                'startingHashes': {str(q['id']): digest(q) for q in selected}}
        return dict(state, status='ready', plan=plan, planPath=str(path.relative_to(root.resolve())),
                    resultPath=str(path.with_name(path.name.replace('-plan.json', '-result.json')).relative_to(root.resolve())),
                    remainingQuestionIds=plan['questionIds'], unpreservedRemovedIds=[])
    return dict(state, status='complete', remainingQuestionIds=[], unpreservedRemovedIds=[])


def work_packet(state, corpus, ledger, report, retired=None):
    by_id = {q['id']: q for q in corpus}
    scope = set(state.get('plan', {}).get('questionIds', []))
    findings = [f for f in report['openFindings'] if scope.intersection(f['questionIds'])]
    related = {i for f in findings for i in f['questionIds']} - scope
    questions = []
    coverage = {q['id']: q for q in report['questions']}
    for qid in state['remainingQuestionIds']:
        if qid not in by_id:
            continue
        template = review_template(by_id[qid])
        template['at'] = state['asOf']
        template['verification']['challenge']['at'] = state['asOf']
        entry = ledger['questions'].get(str(qid), {})
        questions.append({'question': by_id[qid], 'reviewTemplate': template,
                          'existingReview': current_review(entry, by_id[qid], state['asOf']),
                          'coverage': coverage[qid], 'legacyEvidence': entry.get('legacyEvidence', {}),
                          'openFindingIds': [f['id'] for f in findings if qid in f['questionIds']]})
    retirements = [{'retiredQuestion': q, 'replacementQuestion': by_id.get(q.get('replacedBy')),
                    'decision': ledger.get('retirements', {}).get(str(q['id']))}
                   for q in (retired or []) if q['id'] in scope]
    topics = topic_digests([by_id[i] for i in state['remainingQuestionIds'] if i in by_id], corpus)
    remaining = set(state['remainingQuestionIds'])
    for topic in topics:
        topic['remainingQuestionIds'] = [q['id'] for q in topic['questions'] if q['id'] in remaining]
    return {**state, 'questions': questions, 'openFindings': findings,
            'relatedQuestions': [by_id[i] for i in sorted(related) if i in by_id],
            'comparisons': comparison_questions(findings, corpus), 'retirementComparisons': retirements,
            'topicDigests': topics,
            'instructions': 'Read QUESTION_AUDIT.md; research the premise and all four options, then challenge competing answers. Read the complete topic digests and full comparison objects. Related material does not expand scope. Save filled review templates separately; this packet is regenerated on resume. Existing evidence and ranking signals are not proof.'}


def prepare_next(root, corpus, ledger, report, as_of, size=None, preview=False):
    root = Path(root)
    state = queue_state(root, corpus, report, as_of, size)
    if not preview:
        if state['status'] == 'ready':
            path = workspace_path(root, state['planPath'])
            if path.exists():
                raise ValueError('refusing to overwrite an existing audit plan')
            write_json(path, state['plan'])
        packet = work_packet(state, corpus, ledger, report, read_json(root/'questions/retired.json'))
        # Separate full digests keep the main packet readable without hiding or
        # truncating any topic matches; filenames do not incorporate topic text.
        packet_path = workspace_path(root, state['workPacketPath'])
        for index, topic in enumerate(packet['topicDigests'], 1):
            path = workspace_path(root, packet_path.parent/'topics'/f'{index:03d}-{digest(topic["topic"])[:10]}.json')
            write_json(path, topic)
            topic.pop('questions')
            topic['path'] = str(path.relative_to(root.resolve()))
        write_json(packet_path, packet)
        from question_audit_compact import compact_packet
        compact_path = packet_path.with_name(packet_path.stem+'-compact.json')
        write_json(compact_path, compact_packet(packet))
    return state


def print_status(state, preview=False):
    progress = state['progress']
    print(f"Audit progress: {progress['complete']}/{progress['total']} complete; {progress['remaining']} remaining.")
    print(f"Evidence records: {state['recordedEvidence']}; completed approval excludes open concerns.")
    for shard in state['shards']:
        print(f"  {shard['shard']}: {shard['complete']}/{shard['total']} complete")
    if state['status'] == 'complete':
        print('All active questions have current verification and reviewed findings.')
        return
    plan = state['plan']
    print(f"{'Preview' if preview else state['status'].capitalize()}: batch {plan['sequence']} in {plan['sourceShard']}; "
          f"{len(state['remainingQuestionIds'])}/{len(plan['questionIds'])} questions remaining.")
    print('Plan: ' + state['planPath'])
    print('Result: ' + state['resultPath'])
    if not preview:
        print('Work packet: ' + state['workPacketPath'])
        path = Path(state['workPacketPath'])
        print('Compact reading view: ' + str(path.with_name(path.stem+'-compact.json')))
    if state['status'] == 'awaiting-close':
        print('Verification is finished; close this batch before advancing.')
    if state['unpreservedRemovedIds']:
        print('Restore missing retired snapshots: ' + str(state['unpreservedRemovedIds']))
    if state.get('undocumentedRetirementIds'):
        print('Document retirement decisions: '+str(state['undocumentedRetirementIds']))
    if state.get('unclassifiedChangeIds'):
        print('Classify edits before closing: '+str(state['unclassifiedChangeIds']))
