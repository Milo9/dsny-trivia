"""Efficiency helpers must preserve scope, options and explicit evidence checks."""
import copy
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import question_audit as audit
import question_audit_compact as compact
from test_question_audit import AS_OF, ledger_for, question, reviewed


class CompactAuditTests(unittest.TestCase):
    def setUp(self):
        self.q = question()
        self.ledger = ledger_for([self.q])
        full = reviewed(self.q)
        self.library = {'schema': 1, 'sources': {'scene': {
            'url': 'https://example.org/film', 'locator': 'Scene 3',
            'evidence': 'Fixture passage establishes distinct roles.',
            'checkedBy': 'Tester', 'checkedAt': AS_OF, 'timeSensitive': False,
            'nextReviewAt': None}}}
        self.notes = compact.notes_template([self.q], {'questionIds': [self.q['id']]}, 'Tester', AS_OF)
        self.notes['sourcesChecked'] = ['scene']
        note = self.notes['reviews'][0]
        note.update(checks=list(audit.CHECKS), notes=full['notes'], context='Original film',
                    timeSensitive=False, challenge=full['verification']['challenge'])
        note['premise'] = {'reason': 'Fixture premise support', 'sources': ['scene']}
        note['options'] = [{'basis': 'direct' if i == 0 else 'contradiction',
                            'reason': f'Fixture role excludes or establishes option {i}',
                            'sources': ['scene']} for i in range(4)]

    def build(self):
        return compact.build_reviews(self.notes, self.library, [self.q], self.ledger, AS_OF)

    def test_expansion_is_valid_and_embeds_immutable_evidence_without_recording(self):
        before = copy.deepcopy(self.ledger)
        reviews = self.build()
        self.assertEqual(audit.validate_review(reviews[0], AS_OF), [])
        self.assertEqual(reviews[0]['questionSnapshot'], self.q)
        self.assertEqual([o['answer'] for o in reviews[0]['verification']['options']], self.q['answers'])
        self.library['sources']['scene']['evidence'] = 'Later change'
        self.assertNotEqual(reviews[0]['verification']['premise']['sources'][0]['evidence'], 'Later change')
        self.assertEqual(self.ledger, before)

    def test_template_never_attests_to_checks_or_challenge(self):
        notes = compact.notes_template([self.q], {'questionIds': [self.q['id']]}, 'Tester', AS_OF)
        with self.assertRaises(ValueError):
            compact.build_reviews(notes, self.library, [self.q], self.ledger, AS_OF)

    def test_notes_selection_cannot_expand_scope(self):
        plan = {'questionIds': [self.q['id']]}
        with self.assertRaises(ValueError):
            compact.notes_template([self.q, question(2)], plan, 'Tester', AS_OF, [2])
        self.assertEqual(len(compact.notes_template([self.q], plan, 'Tester', AS_OF, [self.q['id']])['reviews']), 1)

    def test_cli_build_failure_preserves_output_and_ledger(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name, value in [('ledger', self.ledger), ('baseline', {'schema': 1}),
                                ('notes', self.notes), ('sources', self.library)]:
                audit.write_json(root/f'{name}.json', value)
            argv = ['--ledger', str(root/'ledger.json'), '--baseline', str(root/'baseline.json'),
                    'build-reviews', str(root/'notes.json'), '--sources', str(root/'sources.json'),
                    '--out', str(root/'reviews.json')]
            before = (root/'ledger.json').read_bytes()
            with patch.object(audit, 'ROOT', root), patch.object(audit, 'load_corpus', return_value=[self.q]), \
                    patch.object(audit, 'today', return_value=AS_OF), patch('validate_corpus.main', return_value=0), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(audit.main(argv), 0)
                output = (root/'reviews.json').read_bytes()
                self.notes['reviews'][0]['options'][3]['sources'] = []
                audit.write_json(root/'notes.json', self.notes)
                self.assertEqual(audit.main(argv), 1)
            self.assertEqual((root/'reviews.json').read_bytes(), output)
            self.assertEqual((root/'ledger.json').read_bytes(), before)

    def test_stale_wording_missing_checks_or_option_evidence_rejects(self):
        mutations = [lambda n: n.update(hash='old'), lambda n: n.update(checks=[]),
                     lambda n: n['options'][3].update(sources=[]),
                     lambda n: n['challenge'].update(alternativesExcluded=False),
                     lambda n: n['options'][1].update(reason='')]
        original = copy.deepcopy(self.notes)
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.notes = copy.deepcopy(original)
                mutate(self.notes['reviews'][0])
                with self.assertRaises(ValueError):
                    self.build()

    def test_unacknowledged_unknown_and_due_sources_reject(self):
        self.notes['sourcesChecked'] = []
        with self.assertRaises(ValueError):
            self.build()
        self.notes['sourcesChecked'] = ['missing']
        with self.assertRaises(ValueError):
            self.build()
        self.notes['sourcesChecked'] = ['scene']
        self.library['sources']['scene'].update(checkedAt='2026-10-01', timeSensitive=True, nextReviewAt=AS_OF)
        with self.assertRaisesRegex(ValueError, 'due for recheck'):
            self.build()

    def test_bad_second_review_and_duplicate_ids_reject_without_ledger_write(self):
        before = copy.deepcopy(self.ledger)
        self.notes['reviews'].append(copy.deepcopy(self.notes['reviews'][0]))
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(self.ledger, before)

    def packet(self):
        return {'schema': 1, 'questions': [{'question': self.q, 'coverage': {},
                'openFindingIds': ['f'], 'existingReview': None}],
                'relatedQuestions': [self.q], 'openFindings': [{'id': 'f'}],
                'comparisons': [{'findingId': 'f', 'questions': [self.q, self.q], 'priority': 1}],
                'retirementComparisons': [], 'topicDigests': []}

    def test_compact_catalog_deduplicates_without_dropping_answers_or_findings(self):
        packet = self.packet()
        view = compact.compact_packet(packet)
        self.assertEqual(list(view['catalog']), [str(self.q['id'])])
        self.assertEqual(view['catalog'][str(self.q['id'])], self.q)
        self.assertEqual(view['openFindings'], packet['openFindings'])
        self.assertEqual(view['comparisons'][0]['questionIds'], [self.q['id']]*2)
        self.assertNotIn('reviewTemplate', view['questions'][0])

    def test_full_overlapping_topics_merge_all_questions_and_reject_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            packet = self.packet()
            extra = question(2)
            for name in ('a', 'b'):
                audit.write_json(root/f'{name}.json', {'questions': [self.q, extra]})
            packet['topicDigests'] = [{'topic': name, 'path': f'{name}.json'} for name in ('a', 'b')]
            view = compact.reading_view(packet, root, ['a', 'b'])
            self.assertEqual(set(view['catalog']), {str(self.q['id']), '2'})
            with self.assertRaises(ValueError):
                compact.reading_view(packet, root, ['missing'])
            packet['topicDigests'][0]['path'] = '../escape.json'
            with self.assertRaises(ValueError):
                compact.reading_view(packet, root, ['a'])

    def test_finding_delta_includes_changed_existing_findings(self):
        old = {'openFindings': [{'id': 'a', 'signature': 'old'}, {'id': 'b'}]}
        new = {'openFindings': [{'id': 'a', 'signature': 'new'}, {'id': 'c'}]}
        self.assertEqual(compact.finding_changes(old, new), {'added': ['c'], 'resolved': ['b'], 'changed': ['a']})


if __name__ == '__main__':
    unittest.main()
