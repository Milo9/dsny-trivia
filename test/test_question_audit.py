"""Regression checks for evidence loss, false audit completion and missed triage."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import question_audit as audit

AS_OF = '2026-11-01'


def question(qid=9001, **values):
    return {**dict(id=qid, question='Name the companion of the red panda?',
                   answers=['Mei', 'Abby', 'Priya', 'Miriam'], category='characters',
                   difficulty='medium'), **values}


def ledger_for(qs):
    return audit.sync_ledger(qs, {'schema': 1, 'questions': {}, 'decisions': {}}, AS_OF)


def reviewed(q, time_sensitive=False, due=None):
    value = audit.review_template(q)
    value.update(reviewer='Test reviewer', at=AS_OF, manual=dict.fromkeys(audit.CHECKS, True),
                 notes='Read full topic coverage; parallel, distinct and unambiguous options.')
    value['verification'].update(context='The original theatrical film, English credits.',
                                 timeSensitive=time_sensitive, nextReviewAt=due,
                                 premise={'reason': 'The credited characters establish the premise in this test fixture.',
                                          'sources': [{'url': 'https://example.org/film/credits', 'locator': 'Cast list'}]},
                                 challenge={'reviewer': 'Test reviewer', 'at': AS_OF, 'premiseChecked': True,
                                            'alternativesExcluded': True,
                                            'notes': 'Compared all four roles and checked that no competing answer fits the stated context.'})
    for i, option in enumerate(value['verification']['options']):
        option.update(basis='direct' if i == 0 else 'contradiction',
                      reason='Specific supporting or excluding evidence for option '+str(i),
                      sources=[{'url': 'https://example.org/film/credits', 'locator': 'End credits, cast section'}])
    return value


class QuestionAuditTests(unittest.TestCase):
    def test_imported_sources_are_not_inferred_to_verify_all_four_options(self):
        q = question(source='https://example.org/film', verifiedAt='2026-10-29')
        ledger = ledger_for([q])
        self.assertIn('source', ledger['questions']['9001']['legacyEvidence'])
        self.assertFalse(audit.source_verified(ledger['questions']['9001'], q, AS_OF))

    def test_edited_question_loses_approval_but_preserves_review_evidence(self):
        q = question()
        ledger = ledger_for([q])
        ledger['questions']['9001']['review'] = reviewed(q)
        self.assertTrue(audit.source_verified(ledger['questions']['9001'], q, AS_OF))
        changed = {**q, 'question': 'What is the name of the panda companion?'}
        audit.sync_ledger([changed], ledger, AS_OF)
        entry = ledger['questions']['9001']
        self.assertFalse(audit.source_verified(entry, changed, AS_OF))
        self.assertEqual(entry['history'][0]['review']['questionSnapshot'], q)

    def test_baseline_backlog_allowed_but_new_content_needs_evidence(self):
        q = question()
        ledger = ledger_for([q])
        baseline = {'questions': {'9001': audit.digest(q)}}
        self.assertEqual(audit.gate_errors([q], ledger, baseline, AS_OF, []), [])
        self.assertTrue(audit.gate_errors([q], ledger, {'questions': {}}, AS_OF, []))
        ledger['questions']['9001']['review'] = reviewed(q)
        self.assertEqual(audit.gate_errors([q], ledger, {'questions': {}}, AS_OF, []), [])

    def test_missing_distractor_evidence_prevents_source_verification(self):
        q = question()
        value = reviewed(q)
        value['verification']['options'][3]['sources'] = []
        self.assertTrue(audit.validate_review(value, AS_OF))
        value = reviewed(q)
        value['verification']['options'][2]['verdict'] = 'correct'
        self.assertTrue(audit.validate_review(value, AS_OF))

    def test_manual_only_review_is_distinct_from_source_verification(self):
        q = question()
        ledger = ledger_for([q])
        value = reviewed(q)
        value['verification'] = None
        ledger['questions']['9001']['review'] = value
        report = audit.audit_report([q], ledger, {'questions': {}}, AS_OF, [])
        self.assertEqual(report['coverage']['manual'], 1)
        self.assertEqual(report['coverage']['sourceVerified'], 0)

    def test_changing_fact_requires_real_future_recheck_and_due_review_blocks_release(self):
        q = question()
        self.assertTrue(audit.validate_review(reviewed(q, True), AS_OF))
        self.assertTrue(audit.validate_review(reviewed(q, True, '2026-02-30'), AS_OF))
        ledger = ledger_for([q])
        ledger['questions']['9001']['review'] = reviewed(q, True, '2026-11-02')
        self.assertTrue(audit.source_verified(ledger['questions']['9001'], q, AS_OF))
        self.assertTrue(audit.gate_errors([q], ledger, {'questions': {'9001': audit.digest(q)}}, '2026-11-02', []))

    def test_snapshot_or_option_mismatch_cannot_reuse_review(self):
        q = question()
        ledger = ledger_for([q])
        ledger['questions']['9001']['review'] = reviewed(q)
        ledger['questions']['9001']['review']['verification']['options'][3]['answer'] = 'Another answer'
        self.assertFalse(audit.source_verified(ledger['questions']['9001'], q, AS_OF))

    def test_warning_disposition_is_invalidated_by_content_change(self):
        q = question(question='What is the name of Miriam?', answers=['Miriam', 'Mei', 'Abby', 'Priya'])
        ledger = ledger_for([q])
        findings = audit.findings_for([q])
        finding = findings[0]
        ledger['decisions'][finding['id']] = dict(signature=finding['signature'], status='accepted',
            reason='Necessary title context.', reviewer='Tester', at=AS_OF)
        self.assertNotIn(finding, audit.open_findings(findings, ledger, AS_OF))
        changed = {**q, 'question': 'Please name Miriam?'}
        self.assertTrue(audit.open_findings(audit.findings_for([changed]), ledger, AS_OF))

    def test_whole_corpus_shared_answer_checks_include_large_and_short_answer_groups(self):
        qs = [question(9000+i, question=f'Identify topic {i}?', answers=['Up', 'A', 'B', 'C']) for i in range(8)]
        pairs = [f for f in audit.findings_for(qs) if f['kind'] == 'duplicate']
        self.assertEqual(len(pairs), 28)

    def test_cross_answer_collision_prioritizes_possible_multiple_correct_answers(self):
        qs = [question(9001, question='Identify the red panda companion?', answers=['Mei', 'Abby', 'P', 'M']),
              question(9002, question='Identify a companion of the red panda?', answers=['Abby', 'Mei', 'X', 'Y'])]
        self.assertIn('cross-answer-collision', audit.risk_map(qs)[9001])

    def test_plan_reproducibly_samples_outside_risk_patterns_in_each_category(self):
        qs = [question(9000+i, question=f'Identify companion {i}?', category='movies' if i<10 else 'characters') for i in range(20)]
        qs.append(question(9021, question='Who composed the score?'))
        ledger = ledger_for(qs)
        a = audit.make_plan(qs, ledger, AS_OF, 'seed', 1, 2)
        self.assertEqual(a, audit.make_plan(qs, ledger, AS_OF, 'seed', 1, 2))
        self.assertEqual(len(a['randomSampleIds']), 4)
        self.assertIn(9021, a['questionIds'])
        self.assertNotIn(9021, a['randomSampleIds'])

    def test_open_warning_blocks_new_verified_question_until_reviewed(self):
        q = question(question='What is the name of Miriam?', answers=['Miriam', 'Mei', 'Abby', 'Priya'])
        ledger = ledger_for([q]); ledger['questions']['9001']['review'] = reviewed(q)
        findings = audit.findings_for([q])
        self.assertTrue(audit.gate_errors([q], ledger, {'questions': {}}, AS_OF, findings))
        for f in findings:
            ledger['decisions'][f['id']] = dict(signature=f['signature'], status='accepted',
                reason='Example adjudication.', reviewer='Tester', at=AS_OF)
        self.assertEqual(audit.gate_errors([q], ledger, {'questions': {}}, AS_OF, findings), [])

    def test_removed_question_must_retain_historical_snapshot(self):
        q = question()
        ledger = ledger_for([q])
        self.assertTrue(audit.gate_errors([], ledger, {'questions': {}}, AS_OF, []))

    def test_completion_rejects_incomplete_scope_and_partial_report_discloses_it(self):
        q = question(); ledger = ledger_for([q])
        plan = audit.make_plan([q], ledger, AS_OF, 'seed', 1, 1)
        report = audit.audit_report([q], ledger, {'questions': {}}, AS_OF, [])
        with self.assertRaises(ValueError):
            audit.completion_report(plan, report, [q], set(), AS_OF, 'Tester')
        result = audit.completion_report(plan, report, [q], set(), AS_OF, 'Tester', True)
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['incompleteIds'], [9001])

    def test_complete_scope_does_not_claim_whole_corpus_is_verified(self):
        qs = [question(9001), question(9002)]
        ledger = ledger_for(qs); ledger['questions']['9001']['review'] = reviewed(qs[0])
        plan = {'schema': 1, 'questionIds': [9001], 'startingHashes': {'9001': audit.digest(qs[0])}}
        report = audit.audit_report(qs, ledger, {'questions': {}}, AS_OF, [])
        result = audit.completion_report(plan, report, qs, set(), AS_OF, 'Tester')
        self.assertEqual(result['status'], 'complete-for-scope')
        self.assertFalse(result['report']['wholeCorpusVerified'])
        self.assertEqual(result['report']['remainingSourceVerification'], 1)

    def test_empty_scope_and_missing_retired_snapshot_cannot_be_completed(self):
        report = {'questions': [], 'openFindings': []}
        with self.assertRaises(ValueError):
            audit.completion_report({'schema': 1, 'questionIds': []}, report, [], set(), AS_OF, 'Tester')
        plan = {'schema': 1, 'questionIds': [9001], 'startingHashes': {'9001': 'old'}}
        with self.assertRaises(ValueError):
            audit.completion_report(plan, report, [], set(), AS_OF, 'Tester')

    def test_claimed_fixed_warning_still_reproducing_fails_gate(self):
        q = question(question='What is the name of Miriam?', answers=['Miriam', 'A', 'B', 'C'])
        ledger = ledger_for([q]); finding = audit.findings_for([q])[0]
        ledger['decisions'][finding['id']] = dict(signature=finding['signature'], status='fixed',
            reason='Claimed fixed.', reviewer='Tester', at=AS_OF)
        errors = audit.gate_errors([q], ledger, {'questions': {'9001': audit.digest(q)}}, AS_OF)
        self.assertTrue(any('still reproduces' in e for e in errors))

    def test_manually_found_concern_survives_edits_and_blocks_audit_completion(self):
        q = question(); ledger = ledger_for([q])
        ledger['issues']['manual-example'] = {'questionIds': [9001], 'reason': 'Plot detail may support two answers.'}
        ledger['questions']['9001']['review'] = reviewed(q)
        report = audit.audit_report([q], ledger, {'questions': {}}, AS_OF)
        self.assertTrue(any(f['kind'] == 'manual' for f in report['openFindings']))
        changed = {**q, 'question': 'Identify the panda companion?'}
        self.assertTrue(any(f['kind'] == 'manual' for f in audit.audit_findings([changed], ledger)))
        self.assertTrue(audit.gate_errors([q], ledger, {'questions': {}}, AS_OF))


if __name__ == '__main__':
    unittest.main()
