import string
from words_check_by_levenshtein import LevenshteinWordCheck
import re
from WordWithDistance import WordWithDistance
from ViterbiAlgorithm import viterbi_segment


class SpellChecker:
    def __init__(self):
        self.checker = LevenshteinWordCheck(key=lambda item: item.distance)

    def run_console(self):
        while True:
            text_input = input("Напишите что-нибудь (введите 'стоп' для выхода): ")
            if text_input.lower() == 'стоп':
                break
            self.check_text(text_input)

    def check_text(self, text):
        """Входные данные: текст
        Разбивает текст на слова, удаляет пунктуацию, приводит все к нижнему регистру.
        Проверяет на каком языке слово.
        Проверяет слова и выводит список исправлений."""

        splitted_text = [word for word in re.split(r'[ ,.!?]', text) if word.strip() != '']

        for word in splitted_text:
            word_without_punctuation = word.rstrip(string.punctuation)
            tested_word = word_without_punctuation.lower()

            if not all(ord('а') <= ord(char) <= ord('я') or char == 'ё' or char == '-' for char in tested_word):
                print(f"Слово '{word}' не на русском или содержит цифры.")
                continue

            if self.check_consecutive_hyphens(tested_word):
                print(f"Слово '{word}' содержит два дефиса подряд.")
                continue

            if "-" in tested_word:
                first_part = tested_word.split("-")[0]
                second_part = tested_word.split("-")[1]
                corrections1 = self.checker.get_suggested_words(first_part)
                corrections2 = self.checker.get_suggested_words(second_part)
                self.write_correct_words(tested_word, [correction for correction in corrections1])
                self.write_correct_words(tested_word, [correction for correction in corrections2])
            else:
                viterby_correction = viterbi_segment(tested_word, self.checker)
                corrections = self.checker.get_suggested_words(tested_word)
                self.write_correct_words(tested_word, [correction for correction in corrections]
                                         + [' '.join(viterby_correction)])


    @staticmethod
    def check_consecutive_hyphens(word):
        """Проверяет, содержит ли слово два дефиса подряд."""

        return '--' in word

    @staticmethod
    def write_correct_words(input_word, words_correction):
        """Входные данные: исходное слово, список вариантов коррекции этого слова.
           Выводит в консоль варианты коррекции."""

        suggestions = []

        for word in words_correction:
            if isinstance(word, WordWithDistance):
                if word.distance == 1.0:
                    break
                else:
                    suggestions.append(word.word)
            elif word != input_word.lower():
                suggestions.append(word)

        suggestions_list = ' / '.join(suggestions)
        if len(suggestions_list) > 0:
            print("Введённый текст: {0:<30}".format(input_word), "Варианты коррекции:", suggestions_list)

