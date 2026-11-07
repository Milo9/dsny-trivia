"""Sequential audit selection must never skip incomplete or stale work."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import question_audit as audit
import question_audit_queue as queue
from test_question_audit import AS_OF, ledger_for, question, reviewed


class AuditQueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.shards = [('questions/q-020.json', [question(i) for i in (10, 30, 90)]),
                       ('questions/q-003.json', [question(i) for i in (2, 8)])]
        self.corpus = [q for _, qs in self.shards for q in qs]
        for name, qs in self.shards:
            audit.write_json(self.root/name, qs)
        audit.write_json(self.root/'questions/manifest.json', {'shards': [n for n, _ in self.shards]})
        audit.write_json(self.root/'questions/retired.json', [])
        audit.write_json(self.root/'audit/queue.json', {'schema': 1, 'batchSize': 2,
            'runsDirectory': 'audit/runs', 'workPacket': 'artifacts/current.json'})
        self.ledger = ledger_for(self.corpus)
        self.baseline = {'questions': {str(q['id']): audit.digest(q) for q in self.corpus}}

    def report(self, findings=None, as_of=AS_OF):
        return audit.audit_report(self.corpus, self.ledger, self.baseline, as_of, findings or [])

    def next(self, preview=False, size=None, report=None):
        return queue.prepare_next(self.root, self.corpus, self.ledger, report or self.report(),
                                  AS_OF, size=size, preview=preview)

    def verify(self, ids):
        for q in self.corpus:
            if q['id'] in ids:
                self.ledger['questions'][str(q['id'])]['review'] = reviewed(q)

    def close(self, state):
        result = audit.completion_report(state['plan'], self.report(), self.corpus, set(), AS_OF, 'Tester')
        audit.write_json(self.root/state['resultPath'], result)

    def test_first_batch_uses_manifest_and_file_order_despite_id_gaps(self):
        state = self.next()
        self.assertEqual(state['plan']['sourceShard'], 'questions/q-020.json')
        self.assertEqual(state['remainingQuestionIds'], [10, 30])
        self.assertTrue((self.root/state['planPath']).exists())
        full = audit.read_json(self.root/state['workPacketPath'])
        compact_path = (self.root/state['workPacketPath']).with_name('current-compact.json')
        compact = audit.read_json(compact_path)
        self.assertEqual(set(compact['catalog']), {'10', '30'})
        self.assertEqual(compact['catalog']['10']['answers'], self.corpus[0]['answers'])
        for topic in full['topicDigests']:
            self.assertTrue(set(topic['remainingQuestionIds']).issubset({10, 30}))

    def test_preview_creates_no_plan_or_packet_and_does_not_change_ledger(self):
        before = copy.deepcopy(self.ledger)
        state = self.next(preview=True)
        self.assertEqual(state['status'], 'ready')
        self.assertFalse((self.root/'audit/runs').exists())
        self.assertFalse((self.root/state['workPacketPath']).exists())
        self.assertEqual(self.ledger, before)

    def test_resume_keeps_scope_and_does_not_overwrite_plan_or_repeat_verified_items(self):
        first = self.next()
        original = (self.root/first['planPath']).read_bytes()
        self.verify([10])
        resumed = self.next(size=1)
        self.assertEqual(resumed['status'], 'resume')
        self.assertEqual(resumed['plan']['questionIds'], [10, 30])
        self.assertEqual(resumed['remainingQuestionIds'], [30])
        self.assertEqual((self.root/first['planPath']).read_bytes(), original)
        packet = audit.read_json(self.root/resumed['workPacketPath'])
        self.assertEqual([q['question']['id'] for q in packet['questions']], [30])

    def test_next_requires_completion_report_before_advancing(self):
        first = self.next()
        self.verify([10, 30])
        awaiting = self.next()
        self.assertEqual(awaiting['status'], 'awaiting-close')
        self.assertEqual(awaiting['planPath'], first['planPath'])
        self.close(first)
        second = self.next()
        self.assertEqual(second['plan']['sequence'], 2)
        self.assertEqual(second['remainingQuestionIds'], [90])
        self.assertEqual(second['plan']['sourceShard'], 'questions/q-020.json')
        self.verify([90]); self.close(second)
        third = self.next()
        self.assertEqual(third['plan']['sourceShard'], 'questions/q-003.json')
        self.assertEqual(third['remainingQuestionIds'], [2, 8])

    def test_partial_report_cannot_advance_queue(self):
        first = self.next()
        result = audit.completion_report(first['plan'], self.report(), self.corpus, set(), AS_OF, 'Tester', True)
        audit.write_json(self.root/first['resultPath'], result)
        self.assertEqual(self.next()['planPath'], first['planPath'])

    def test_new_warning_reopens_a_previously_closed_batch_and_includes_related_question(self):
        first = self.next(); self.verify([10, 30]); self.close(first)
        report = self.report()
        report['openFindings'] = [{'id': 'new-duplicate', 'kind': 'duplicate', 'questionIds': [10, 2]}]
        resumed = self.next(report=report)
        self.assertEqual(resumed['status'], 'resume')
        self.assertEqual(resumed['remainingQuestionIds'], [10])
        packet = audit.read_json(self.root/resumed['workPacketPath'])
        self.assertEqual([q['id'] for q in packet['relatedQuestions']], [2])
        self.assertEqual(resumed['plan']['questionIds'], [10, 30])

    def test_reverified_content_edit_still_requires_a_fresh_completion_report(self):
        first = self.next(); self.verify([10, 30]); self.close(first)
        self.corpus[0] = {**self.corpus[0], 'question': 'Updated wording?'}
        audit.write_json(self.root/self.shards[0][0], self.corpus[:3])
        audit.sync_ledger(self.corpus, self.ledger, AS_OF)
        self.assertEqual(self.next()['status'], 'resume')
        self.verify([10])
        from question_audit_operations import classify_change
        self.ledger = classify_change(self.corpus, self.ledger, 10, ['clarification'],
            'Tester', 'Clarified the question.', 'test review', AS_OF)
        self.assertEqual(self.next()['status'], 'awaiting-close')

    def test_overdue_review_reopens_earlier_closed_batch(self):
        first = self.next(); self.verify([10, 30]); self.close(first)
        self.ledger['questions']['10']['review']['verification'].update(timeSensitive=True, nextReviewAt='2026-11-02')
        later = audit.audit_report(self.corpus, self.ledger, self.baseline, '2026-11-02', [])
        state = queue.queue_state(self.root, self.corpus, later, '2026-11-02')
        self.assertEqual(state['planPath'], first['planPath'])
        self.assertEqual(state['remainingQuestionIds'], [10])

    def test_verified_questions_from_other_workflows_are_skipped(self):
        self.verify([10])
        self.assertEqual(self.next()['remainingQuestionIds'], [30, 90])

    def test_completed_bank_returns_complete_without_creating_empty_plan(self):
        self.verify([q['id'] for q in self.corpus])
        state = self.next()
        self.assertEqual(state['status'], 'complete')
        self.assertNotIn('planPath', state)
        self.assertFalse((self.root/'audit/runs').exists())

    def test_removed_snapshot_is_required_before_a_batch_can_finish(self):
        first = self.next()
        self.corpus = self.corpus[1:]
        audit.write_json(self.root/self.shards[0][0], self.corpus[:2])
        state = self.next()
        self.assertEqual(state['status'], 'resume')
        self.assertEqual(state['unpreservedRemovedIds'], [10])

    def test_invalid_sizes_and_external_output_paths_are_rejected(self):
        for size in (0, -1, 251, True):
            with self.assertRaises(ValueError):
                self.next(size=size)
        config = audit.read_json(self.root/'audit/queue.json')
        config['workPacket'] = '../outside.json'
        audit.write_json(self.root/'audit/queue.json', config)
        with self.assertRaises(ValueError):
            self.next()


if __name__ == '__main__':
    unittest.main()
