import unittest
from SpellChecker import SpellChecker
from words_check_by_levenshtein import LevenshteinWordCheck
from Levenshtein_algorithm import get_levenshtein_distance
from WordWithDistance import WordWithDistance
import hashlib


class MyTestCase(unittest.TestCase):

    def test_check_consecutive_hyphens(self):
        checker = SpellChecker()
        result1 = checker.check_consecutive_hyphens("пол--арбуза")
        result2 = checker.check_consecutive_hyphens("пол-арбуза")
        self.assertTrue(result1)
        self.assertFalse(result2)

    def setUp(self):
        self.word_check = LevenshteinWordCheck(key=lambda x: x.distance)

    def test_add_distance(self):
        word_with_distance = WordWithDistance('малоко')
        input_word = 'молоко'
        expected_distance = get_levenshtein_distance(word_with_distance.word, input_word)
        result = self.word_check.add_distance(word_with_distance, input_word)
        self.assertEqual(result.distance, expected_distance)

    def test_get_distance_cache_hit(self):
        word = 'молоко'
        distance = [1, 2, 3]
        self.word_check.cache[hashlib.md5(word.encode('utf-8')).hexdigest()] = distance
        result = self.word_check.get_distance(word)
        self.assertEqual(result, distance)

    def test_get_distance_cache_miss(self):
        word = 'молоко'
        expected_distance = [WordWithDistance('молоко'), WordWithDistance('молокот'), WordWithDistance('молок')]
        self.word_check.data = expected_distance
        result = self.word_check.get_distance(word)
        self.assertEqual(result, expected_distance)
        self.assertEqual(len(self.word_check.cache), 1)
        self.assertEqual(self.word_check.cache[hashlib.md5(word.encode('utf-8')).hexdigest()], expected_distance)

    def test_get_suggested_words(self):
        word = 'малоко'
        expected_distance = [WordWithDistance('молоко'), WordWithDistance('молокот'), WordWithDistance('молок')]
        for suggestion in expected_distance:
            suggestion.distance = get_levenshtein_distance(word, suggestion.word)
            suggestion.other = word
        self.word_check.get_distance = lambda x: expected_distance
        result = self.word_check.get_suggested_words(word)
        self.assertEqual(result, expected_distance[:3])


if __name__ == '__main__':
    unittest.main()
