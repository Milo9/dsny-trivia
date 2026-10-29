import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from _common import find_answer_leaks
from find_category_bugs import check_category


class ContentToolTests(unittest.TestCase):
    def test_answer_inside_another_word_is_not_a_verbatim_leak(self):
        q = {'question': 'What is the name of the grasshopper?', 'answers': ['Hopper', 'Flik', 'Molt', 'Atta']}
        self.assertFalse(any(h['tier'] == 1 for h in find_answer_leaks(q)))

    def test_actual_whole_word_answer_is_a_leak(self):
        q = {'question': 'What is the name of Hopper?', 'answers': ['Hopper', 'Flik', 'Molt', 'Atta']}
        self.assertTrue(any(h['tier'] == 1 for h in find_answer_leaks(q)))

    def test_explicit_film_topic_prevents_incidental_title_false_positive(self):
        q = {'question': 'Which actor from Toy Story voiced Mama Gunda?', 'answers': ['Estelle Harris'], 'film': 'Tarzan II', 'category': 'movies'}
        self.assertEqual(check_category(q), [])

    def test_frozen_foods_is_not_the_film(self):
        self.assertEqual(check_category({'question': 'A line of frozen foods', 'answers': ['Food'], 'category': 'pixar'}), [])

    def test_explicit_up_topic_finds_a_real_category_bug(self):
        self.assertTrue(check_category({'film': 'Up', 'category': 'movies'}))


if __name__ == '__main__':
    unittest.main()
