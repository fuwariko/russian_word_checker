import unittest
from ViterbiAlgorithm import viterbi_segment
from words_check_by_levenshtein import LevenshteinWordCheck


class MyTestCase(unittest.TestCase):
    def test_string_without_delimiters(self):
        text = "яидупополю"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['я', 'иду', 'по', 'полю'])

    def test_string_with_single_delimiter(self):
        text = "молоко"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['молоко'])

    def test_string_with_repeating_delimiters(self):
        text = "вполе"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['в', 'поле'])

    def test_string_with_delimiters_of_single_letter(self):
        text = "яяиду"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['я', 'я', 'иду'])

    def test_string_with_delimiters_of_multiple_letters(self):
        text = "котсобака"
        checker = LevenshteinWordCheck(key=lambda item: item.distance)
        self.assertEqual(viterbi_segment(text, checker), ['кот', 'собака'])


if __name__ == '__main__':
    unittest.main()
