import unittest
from Levenshtein_algorithm import get_levenshtein_distance


class TestLevenshteinDistanceNormalized(unittest.TestCase):

    def test_same_strings(self):
        self.assertEqual(get_levenshtein_distance("слово", "слово"), 1.0)

    def test_one_empty_string(self):
        self.assertEqual(get_levenshtein_distance("кот", ""), 0.0)
        self.assertEqual(get_levenshtein_distance("", "кот"), 0.0)

    def test_insertion(self):
        self.assertEqual(get_levenshtein_distance("кот", "коть"), 0.75)

    def test_case_insensitive(self):
        self.assertEqual(get_levenshtein_distance("кОт", "кот"), 1.0)

    def test_deletion(self):
        self.assertEqual(get_levenshtein_distance("коть", "кот"), 0.75)

    def test_substitution(self):
        self.assertEqual(get_levenshtein_distance("кот", "кат"),  0.6666666666666667)


if __name__ == '__main__':
    unittest.main()