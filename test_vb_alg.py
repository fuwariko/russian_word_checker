import unittest
from ViterbiAlgorithm import viterbi_segment
from words_check_by_levenshtein import LevenshteinWordCheck


class MyTestCase(unittest.TestCase):
    def test_long_string(self):
        text = "яидупополю"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['я', 'иду', 'по', 'полю'])

    def test_one_word(self):
        text = "молоко"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['молоко'])

    def test_two_words1(self):
        text = "вполе"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['в', 'поле'])

    def test_string_with_repeating(self):
        text = "яяиду"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['я', 'я', 'иду'])

    def test_string_with_two_words2(self):
        text = "котсобака"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['кот', 'собака'])


if __name__ == '__main__':
    unittest.main()
