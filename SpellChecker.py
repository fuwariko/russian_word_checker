import string
from words_check_by_levenshtein import LevenshteinWordCheck
import re
from WordWithDistance import WordWithDistance


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

        splitted_text = re.split(r'[ ,.!?]', text)

        for word in splitted_text:
            word_without_punctuation = word.rstrip(string.punctuation)
            tested_word = word_without_punctuation.lower()

            if not all(ord('а') <= ord(char) <= ord('я') or char == 'ё' or char == '-' for char in tested_word):
                print(f"Слово '{word}' не на русском или содержит цифры.")
                continue

            corrections = self.checker.get_suggested_words(tested_word)

            self.write_correct_words(word, [correction for correction in corrections])

    @staticmethod
    def write_correct_words(input_word, words_correction):
        """Входные данные: исходное слово, список вариантов коррекции этого слова.
           Выводит в консоль варианты коррекции."""

        suggestions = []

        for word in words_correction:
            if isinstance(word, WordWithDistance):
                suggestions.append(word.word)
            elif word != input_word.lower():
                suggestions.append(word)

        suggestions_list = ' / '.join(suggestions)
        print("Введённый текст: {0:<50}".format(input_word), "Варианты коррекции:", suggestions_list)