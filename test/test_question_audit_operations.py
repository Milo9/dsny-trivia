"""Evidence challenge, honest counts, bulk imports and recoverable retirements."""
import copy
from contextlib import redirect_stdout, redirect_stderr
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import question_audit as audit
import question_audit_operations as operations
import question_audit_queue as queue
from question_audit_recon import comparison_questions, topic_digests
from test_question_audit import AS_OF, ledger_for, question, reviewed


class EvidenceChallengeTests(unittest.TestCase):
    def test_new_templates_do_not_attest_to_unperformed_work(self):
        r = audit.review_template(question())
        self.assertEqual(r['schema'], 2)
        self.assertFalse(r['verification']['challenge']['premiseChecked'])
        self.assertFalse(r['verification']['challenge']['alternativesExcluded'])
        self.assertTrue(audit.validate_review(r, audit.today()))

    def test_premise_challenge_and_each_option_basis_are_required(self):
        q = question()
        mutations = [lambda r: r['verification'].pop('premise'),
                     lambda r: r['verification']['premise'].update(sources=[]),
                     lambda r: r['verification'].pop('challenge'),
                     lambda r: r['verification']['challenge'].update(alternativesExcluded=False),
                     lambda r: r['verification']['challenge'].update(notes=''),
                     lambda r: r['verification']['challenge'].update(at='2026-11-02'),
                     lambda r: r['verification']['options'][3].pop('basis')]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                r = reviewed(q); mutate(r)
                self.assertTrue(audit.validate_review(r, AS_OF))

    def test_malformed_challenge_dates_produce_errors_instead_of_crashing(self):
        r = reviewed(question()); r['at'] = None
        self.assertTrue(audit.validate_review(r, AS_OF))

    def test_one_source_can_support_exhaustive_or_exclusive_reasoning(self):
        r = reviewed(question())
        for option in r['verification']['options']:
            option['basis'] = 'exhaustive-list'
        self.assertEqual(audit.validate_review(r, AS_OF), [])

    def test_legacy_records_are_disclosed_without_fabricating_a_challenge(self):
        q = question(); r = reviewed(q)
        r.pop('schema'); r['verification'].pop('challenge'); r['verification'].pop('premise')
        for option in r['verification']['options']:
            option.pop('basis')
        ledger = ledger_for([q]); ledger['questions'][str(q['id'])]['review'] = r
        report = audit.audit_report([q], ledger, {'questions': {}}, AS_OF, [])
        self.assertEqual(report['coverage']['legacyEvidenceReviews'], 1)
        self.assertEqual(report['coverage']['challengedEvidence'], 0)
        self.assertEqual(report['questions'][0]['evidenceStandard'], 'legacy-v1')
        with self.assertRaisesRegex(ValueError, 'schema 2'):
            audit.record_reviews([q], ledger, [r], AS_OF)

    def test_manual_concern_preserves_record_but_prevents_verified_and_approved_counts(self):
        q = question(); ledger = ledger_for([q])
        ledger['questions'][str(q['id'])]['review'] = reviewed(q)
        findings = [{'id': 'manual-evidence', 'kind': 'manual', 'questionIds': [q['id']], 'signature': 'v1'}]
        report = audit.audit_report([q], ledger, {'questions': {}}, AS_OF, findings)
        self.assertEqual(report['coverage']['evidenceRecorded'], 1)
        self.assertEqual(report['coverage']['sourceVerified'], 0)
        self.assertEqual(report['coverage']['approved'], 0)
        self.assertEqual(report['remainingSourceVerification'], 1)
        self.assertFalse(report['wholeCorpusVerified'])

    def test_non_evidence_warning_blocks_approval_without_erasing_source_record(self):
        q = question(); ledger = ledger_for([q]); ledger['questions'][str(q['id'])]['review'] = reviewed(q)
        f = [{'id': 'candidate', 'kind': 'duplicate', 'questionIds': [q['id']], 'signature': 'v1'}]
        report = audit.audit_report([q], ledger, {'questions': {}}, AS_OF, f)
        self.assertEqual(report['coverage']['sourceVerified'], 1)
        self.assertEqual(report['coverage']['approved'], 0)
        self.assertEqual(report['remainingApproval'], 1)
        self.assertFalse(report['wholeCorpusVerified'])


class BulkReviewTests(unittest.TestCase):
    def test_invalid_last_review_does_not_mutate_any_ledger_entry(self):
        qs = [question(1), question(2)]; ledger = ledger_for(qs); before = copy.deepcopy(ledger)
        reviews = [reviewed(q) for q in qs]
        reviews[-1]['verification']['options'][-1]['sources'] = []
        with self.assertRaises(ValueError):
            audit.record_reviews(qs, ledger, reviews, AS_OF)
        self.assertEqual(ledger, before)

    def test_valid_bulk_import_preserves_old_review_in_history_and_does_not_alias_inputs(self):
        q = question(); ledger = ledger_for([q]); old = reviewed(q)
        ledger['questions'][str(q['id'])]['review'] = old
        new = reviewed(q); new['notes'] = 'Renewed review after checking the scene.'
        updated = audit.record_reviews([q], ledger, [new], AS_OF)
        self.assertEqual(updated['questions'][str(q['id'])]['history'][-1]['review'], old)
        new['notes'] = 'Modified caller data'
        self.assertNotEqual(updated['questions'][str(q['id'])]['review']['notes'], new['notes'])
        self.assertEqual(ledger['questions'][str(q['id'])]['review'], old)

    def test_stale_and_duplicate_reviews_fail_before_mutation(self):
        q = question(); ledger = ledger_for([q]); r = reviewed(q)
        for reviews in ([r, r], [{**r, 'hash': 'stale'}], []):
            with self.assertRaises(ValueError):
                audit.record_reviews([q], ledger, reviews, AS_OF)


class ReconstructionTests(unittest.TestCase):
    def test_inverse_candidates_are_detected_and_ranked_above_common_answers(self):
        qs = [question(1, question='Who is the villain in Sleeping Beauty?', answers=['Maleficent','A','B','C']),
              question(2, question='In which film does Maleficent appear?', answers=['Sleeping Beauty','A','B','C']),
              question(3, question='What color is the hat?', answers=['Blue','A','B','C']),
              question(4, question='What color is the ocean?', answers=['Blue','A','B','C'])]
        findings = [f for f in audit.findings_for(qs) if f['kind'] == 'duplicate']
        inverse = next(f for f in findings if f['questionIds'] == [1, 2])
        common = next(f for f in findings if f['questionIds'] == [3, 4])
        self.assertLess(inverse['priority'], common['priority'])
        self.assertEqual(inverse['signals'], ['inverse-answer-and-stem'])
        comparisons = comparison_questions(findings, qs)
        self.assertEqual(comparisons[0]['questions'], qs[:2])
        self.assertEqual(len(comparisons[0]['questions'][1]['answers']), 4)

    def test_shared_answer_pair_signatures_stay_stable_when_ranking_is_added(self):
        qs = [question(1), question(2)]
        f = next(f for f in audit.findings_for(qs) if f['kind'] == 'duplicate')
        signature = audit.digest({'kind': 'duplicate', 'ids': [1,2], 'detail': f['detail'],
                                  'hashes': [audit.digest(q) for q in qs]})
        self.assertEqual(signature, f['signature'])

    def test_topic_digest_has_every_match_and_all_options_without_distractor_only_matches(self):
        selected = question(1, question='In Dumbo, who is the friend?')
        qs = [selected]+[question(i, question=f'In Dumbo, identify scene {i}?') for i in range(2, 80)]
        qs.append(question(80, question='Who is the chef?', answers=['Remy','Dumbo','A','B']))
        digest = next(d for d in topic_digests([selected], qs) if d['topic'] == 'Dumbo')
        self.assertEqual(digest['count'], 79)
        self.assertEqual(len(digest['questions'][-1]['answers']), 4)
        self.assertNotIn(80, [q['id'] for q in digest['questions']])

    def test_topic_registry_does_not_treat_every_grew_up_phrase_as_the_film_up(self):
        q = question(1, question='Where did the heroine grow up?', answers=['A town','A','B','C'])
        self.assertFalse(any(d['topic']=='Up' for d in topic_digests([q],[q])))


class RetirementAndReportingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.qs = [question(1), question(2)]
        self.ledger = ledger_for(self.qs)
        self.ledger['questions']['1']['review'] = reviewed(self.qs[0])
        self.ledger_path = self.root/'audit/ledger.json'
        self.shard = self.root/'questions/q-001.json'
        audit.write_json(self.shard, self.qs)
        audit.write_json(self.root/'questions/manifest.json', {'shards':['questions/q-001.json'], 'retired':'questions/retired.json'})
        audit.write_json(self.root/'questions/retired.json', [])
        audit.write_json(self.root/'audit/baseline.json', {'schema':1,'questions':{str(q['id']):audit.digest(q) for q in self.qs}})
        audit.write_json(self.ledger_path, self.ledger)

    def retire(self, **kwargs):
        return operations.retire_question(self.root, self.ledger_path, 1, 2, 'Tester',
            'Same companion fact in different wording.', 'audit/review-1.json', AS_OF, **kwargs)

    def originals(self):
        return {p:p.read_bytes() for p in (self.shard, self.ledger_path, self.root/'questions/retired.json')}

    def test_retirement_preserves_exact_snapshot_old_review_and_replacement(self):
        record = self.retire()
        snapshot = audit.read_json(self.root/'questions/retired.json')[0]
        self.assertEqual({k:v for k,v in snapshot.items() if k!='replacedBy'}, self.qs[0])
        self.assertEqual(snapshot['replacedBy'], 2)
        ledger = audit.read_json(self.ledger_path)
        self.assertEqual(ledger['questions']['1'], self.ledger['questions']['1'])
        self.assertEqual(ledger['retirements']['1'], record)
        self.assertEqual(audit.read_json(self.shard), self.qs[1:])
        self.assertFalse(operations.transaction_path(self.root).exists())

    def test_retirement_validation_rejects_missing_self_and_stale_replacement_without_writes(self):
        before = self.originals()
        for replacement in (1, 99):
            with self.assertRaises(ValueError):
                operations.retire_question(self.root, self.ledger_path, 1, replacement, 'T','reason','ref',AS_OF)
        self.assertEqual(self.originals(), before)
        ledger = audit.read_json(self.ledger_path); ledger['questions']['1']['hash']='stale'
        audit.write_json(self.ledger_path, ledger); before = self.originals()
        with self.assertRaisesRegex(ValueError, 'snapshot differs'):
            self.retire()
        self.assertEqual(self.originals(), before)

    def test_normal_write_failure_rolls_back_all_files(self):
        before = self.originals(); real = operations._replace_text; calls = 0
        def fail_once(path, contents):
            nonlocal calls
            calls += 1
            if calls == 2: raise OSError('disk write failed')
            real(path, contents)
        with patch.object(operations, '_replace_text', side_effect=fail_once):
            with self.assertRaises(OSError): self.retire()
        self.assertEqual(self.originals(), before)
        self.assertFalse(operations.transaction_path(self.root).exists())

    def test_rollback_preserves_unicode_bom_and_windows_line_endings_byte_for_byte(self):
        self.qs[0]['question']='What instrument does Héctor play?'
        self.qs[0]['answers']=['Guitar','Violin','Flute','Trumpet']
        audit.write_json(self.shard,self.qs)
        text=self.shard.read_text(encoding='utf-8').replace('\n','\r\n')
        self.shard.write_bytes(b'\xef\xbb\xbf'+text.encode('utf-8'))
        audit.write_json(self.ledger_path,ledger_for(self.qs))
        before=self.originals(); real=operations._replace_text; calls=0
        def fail_once(path,contents):
            nonlocal calls
            calls+=1
            if calls==3: raise OSError('last destination unavailable')
            real(path,contents)
        with patch.object(operations,'_replace_text',side_effect=fail_once):
            with self.assertRaises(OSError): self.retire()
        self.assertEqual(self.originals(),before)

    def test_process_interruption_leaves_recoverable_journal_and_commands_refuse_to_continue(self):
        before = self.originals(); real = operations._replace_text; calls = 0
        def interrupt(path, contents):
            nonlocal calls
            calls += 1
            if calls == 2: raise KeyboardInterrupt()
            real(path, contents)
        with patch.object(operations, '_replace_text', side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt): self.retire()
        self.assertTrue(operations.transaction_path(self.root).exists())
        with patch.object(audit, 'ROOT', self.root), redirect_stderr(io.StringIO()):
            self.assertEqual(audit.main(['status']), 1)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(audit.main(['recover-retirement']), 0)
        self.assertEqual(self.originals(), before)

    def test_recovery_rejects_outside_paths_before_any_write(self):
        before = self.originals()
        audit.write_json(operations.transaction_path(self.root), {'schema':1,'files':[
            {'path':'audit/ledger.json','original':'destroyed'},
            {'path':'../outside.json','original':'bad'}]})
        with self.assertRaises(ValueError): operations.recover_retirement(self.root)
        self.assertEqual(self.originals(), before)

    def test_existing_snapshot_can_gain_a_decision_without_editing_the_snapshot(self):
        self.retire(); before = (self.root/'questions/retired.json').read_bytes()
        self.retire(preserved=True)
        self.assertEqual((self.root/'questions/retired.json').read_bytes(), before)
        self.assertEqual(len(audit.read_json(self.ledger_path)['retirements']['1']['history']), 1)

    def test_completion_requires_retirement_decision_not_only_a_snapshot(self):
        self.retire(); ledger = audit.read_json(self.ledger_path)
        ledger['questions']['2']['review'] = reviewed(self.qs[1])
        report = audit.audit_report(self.qs[1:], ledger, {'questions':{}}, AS_OF, [])
        plan = {'schema':1,'questionIds':[1,2],'startingHashes':{str(q['id']):audit.digest(q) for q in self.qs}}
        retired = {q['id']:q for q in audit.read_json(self.root/'questions/retired.json')}
        self.assertEqual(audit.completion_report(plan, report, self.qs[1:], retired, AS_OF, 'T')['scopeCounts']['retired'], 1)
        report['retirementRecords'] = {}
        partial = audit.completion_report(plan, report, self.qs[1:], retired, AS_OF, 'T', True)
        self.assertEqual(partial['undocumentedRetirementIds'], [1])
        self.assertEqual(partial['scopeCounts']['unresolved'], 1)
        with self.assertRaises(ValueError): audit.completion_report(plan, report, self.qs[1:], retired, AS_OF, 'T')

    def test_retirement_packet_contains_both_complete_question_objects(self):
        self.retire(); ledger=audit.read_json(self.ledger_path)
        report=audit.audit_report(self.qs[1:],ledger,{'questions':{}},AS_OF,[])
        state={'plan':{'questionIds':[1]},'remainingQuestionIds':[]}
        packet=queue.work_packet(state,self.qs[1:],ledger,report,audit.read_json(self.root/'questions/retired.json'))
        pair=packet['retirementComparisons'][0]
        self.assertEqual(pair['retiredQuestion']['answers'],self.qs[0]['answers'])
        self.assertEqual(pair['replacementQuestion'],self.qs[1])
        self.assertEqual(pair['decision']['retiredHash'],audit.digest(self.qs[0]))

    def test_changed_question_needs_classification_and_types_are_not_factual_error_counts(self):
        original = self.qs[0]; changed = {**original,'difficulty':'hard'}
        ledger = ledger_for([changed]); ledger['questions']['1']['review'] = reviewed(changed)
        plan = {'schema':1,'questionIds':[1],'startingHashes':{'1':audit.digest(original)}}
        report = audit.audit_report([changed], ledger, {'questions':{}}, AS_OF, [])
        partial = audit.completion_report(plan, report, [changed], set(), AS_OF, 'T', True)
        self.assertEqual(partial['changeSummary']['unclassifiedIds'], [1])
        ledger = operations.classify_change([changed],ledger,1,['difficulty','clarification'],'T','Calibrated wording and recall.','ref',AS_OF)
        report = audit.audit_report([changed], ledger, {'questions':{}}, AS_OF, [])
        result = audit.completion_report(plan, report, [changed], set(), AS_OF, 'T')
        self.assertEqual(result['changeSummary']['edited'], 1)
        self.assertEqual(result['changeSummary']['byType']['difficulty'], 1)
        self.assertEqual(result['changeSummary']['byType']['factual'], 0)
        self.assertEqual(result['scopeCounts']['approved'], 1)

    def test_completion_overwrite_archives_prior_result_once(self):
        path = self.root/'audit/runs/example-result.json'
        a={'status':'complete-for-scope'}; b={'status':'partial'}
        operations.save_completion(path,a); operations.save_completion(path,b); operations.save_completion(path,b)
        history = list((path.parent/'example-result-history').glob('*.json'))
        self.assertEqual(len(history), 1)
        self.assertEqual(audit.read_json(history[0]), a)
        self.assertEqual(audit.read_json(path), b)

    def main(self, args):
        def load(): return audit.read_json(self.shard)
        with patch.object(audit,'ROOT',self.root), patch.object(audit,'load_corpus',side_effect=load), \
                patch('validate_corpus.main',return_value=0), patch.object(audit,'today',return_value=AS_OF), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return audit.main(args)

    def test_record_many_cli_rejects_entire_array_without_changing_ledger(self):
        rs=[reviewed(q) for q in self.qs]
        rs[-1]['hash']='wrong'
        path=self.root/'reviews.json'; audit.write_json(path,rs)
        before=self.ledger_path.read_bytes()
        self.assertEqual(self.main(['record-many',str(path)]),1)
        self.assertEqual(self.ledger_path.read_bytes(),before)
        rs[-1]=reviewed(self.qs[-1]); audit.write_json(path,rs)
        self.assertEqual(self.main(['record-many',str(path)]),0)
        ledger=audit.read_json(self.ledger_path)
        self.assertTrue(all(ledger['questions'][str(q['id'])]['review']['schema']==2 for q in self.qs))

    def test_retire_cli_preserves_content_and_refreshes_report_without_source_approval(self):
        self.assertEqual(self.main(['retire','1','--replaced-by','2','--reviewer','T',
                                   '--reason','Equivalent companion fact.','--reference','comparison.json']),0)
        report=audit.read_json(self.root/'artifacts/question-audit.json')
        self.assertEqual(report['active'],1)
        self.assertEqual(report['coverage']['approved'],0)
        self.assertIn('1',report['retirementRecords'])

    def test_packet_writes_complete_topic_files_and_keeps_saved_plan_scope(self):
        self.qs=[question(1,question='In Dumbo, who is the friend?'),
                 question(2,question='In Dumbo, what is the train called?')]
        audit.write_json(self.shard,self.qs)
        ledger=ledger_for(self.qs)
        audit.write_json(self.root/'audit/queue.json',{'schema':1,'batchSize':1,
            'runsDirectory':'audit/runs','workPacket':'artifacts/current.json'})
        report=audit.audit_report(self.qs,ledger,{'questions':{}},AS_OF,[])
        state=queue.prepare_next(self.root,self.qs,ledger,report,AS_OF)
        packet=audit.read_json(self.root/state['workPacketPath'])
        self.assertEqual(packet['questions'][0]['reviewTemplate']['verification']['challenge']['at'],AS_OF)
        topic=next(d for d in packet['topicDigests'] if d['topic']=='Dumbo')
        full=audit.read_json(self.root/topic['path'])
        self.assertEqual([q['id'] for q in full['questions']],[1,2])
        self.assertEqual(state['plan']['questionIds'],[1])

    def test_missing_classification_keeps_reverified_batch_open(self):
        q=self.qs[0]; ledger=ledger_for([q]); ledger['questions']['1']['review']=reviewed(q)
        original={**q,'difficulty':'hard'}
        plan={'schema':1,'workflow':'next-shard','sequence':1,'sourceShard':'questions/q-001.json',
              'questionIds':[1],'batchSize':1,'startingHashes':{'1':audit.digest(original)}}
        audit.write_json(self.root/'audit/runs/next-shard-0001-plan.json',plan)
        audit.write_json(self.root/'audit/queue.json',{'schema':1,'batchSize':1,
            'runsDirectory':'audit/runs','workPacket':'artifacts/current.json'})
        # Only question 1 participates in this fixture's active bank.
        audit.write_json(self.shard,[q])
        report=audit.audit_report([q],ledger,{'questions':{}},AS_OF,[])
        state=queue.queue_state(self.root,[q],report,AS_OF)
        self.assertEqual(state['status'],'resume')
        self.assertEqual(state['unclassifiedChangeIds'],[1])
        self.assertEqual(state['plan']['questionIds'],[1])

    def test_manual_concern_cannot_be_closed_using_the_same_pre_concern_review(self):
        self.assertEqual(self.main(['issue','1','--reviewer','T','--reason','Evidence may permit another answer.']),0)
        ledger=audit.read_json(self.ledger_path); fid=next(iter(ledger['issues']))
        self.assertEqual(self.main(['decide',fid,'fixed','--reviewer','T','--reason','Claimed resolved.','--reference','ref']),1)
        renewed=reviewed(self.qs[0]); renewed['verification']['challenge']['notes']='Inspected the original scene in response to the concern; alternatives excluded.'
        path=self.root/'renewed.json'; audit.write_json(path,renewed)
        self.assertEqual(self.main(['record',str(path)]),0)
        self.assertEqual(self.main(['decide',fid,'fixed','--reviewer','T','--reason','Rechecked scene evidence.','--reference','ref']),0)

    def test_legacy_review_cannot_close_a_new_manual_concern_by_accepting_it(self):
        ledger=audit.read_json(self.ledger_path)
        ledger['questions']['1']['review'].pop('schema')
        audit.write_json(self.ledger_path,ledger)
        self.assertEqual(self.main(['issue','1','--reviewer','T','--reason','Distractor exclusion not established.']),0)
        ledger=audit.read_json(self.ledger_path); fid=next(iter(ledger['issues']))
        self.assertEqual(self.main(['decide',fid,'accepted','--reviewer','T','--reason','Claimed false alarm.','--reference','ref']),1)
        self.assertEqual(audit.read_json(self.ledger_path)['decisions'][fid]['status'],'unresolved')


if __name__ == '__main__':
    unittest.main()
