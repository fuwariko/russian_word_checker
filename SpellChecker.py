import string
from words_check_by_levenshtein import LevenshteinWordCheck
import re
from WordWithDistance import WordWithDistance
from ViterbiAlgorithm import viterbi_segment


class SpellChecker:
    def __init__(self):
        self.checker = LevenshteinWordCheck(key=lambda item: item.distance)

    @staticmethod
    def read_file(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    @staticmethod
    def add_word_to_dictionary(word, filename):
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(word + '\n')

    @staticmethod
    def save_rules(rules, filename):
        with open(filename, 'a', encoding='utf-8') as file:
            for incorrect_word, correct_word in rules.items():
                file.write(f"{incorrect_word}:{correct_word}\n")

    @staticmethod
    def load_rules(filename):
        rules = {}

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    incorrect_word, correct_word = line.split(':')
                    rules[incorrect_word] = correct_word

        return rules

    def read_input(self):
        user_choice = input("Выберите способ ввода текста (1 - консоль, 2 - файл): ")
        if user_choice == '1':
            text = input("Введите текст (введите 'cтоп' для выхода, "
                         "\n'добавить слово' - добавить слово в словарь, "
                         "\n'добавить правило' - добавить правило в словарь): ")
        elif user_choice == '2':
            filename = input("Введите имя файла: ")
            text = self.read_file(filename)
        else:
            print("Некорректный выбор.")
            return None
        return text

    def run_console(self):
        while True:
            text_input = self.read_input()
            if text_input is None:
                continue
            if text_input.lower() == 'добавить слово':
                new_word = input("Введите слово для добавления: ")
                filename = input("Введите имя файла, в который нужно добавить: ")
                self.add_word_to_dictionary(new_word, filename)
                continue
            if text_input.lower() == 'добавить правило':
                new_rule = input("Введите новое правило (формат: 'искажение:правильное'): ")
                rule_parts = new_rule.split(":")
                incorrect_word = rule_parts[0]
                correct_word = rule_parts[1]
                filename = input("Введите имя файла, в который нужно добавить правило: ")
                rule = {incorrect_word: correct_word}
                self.save_rules(rule, filename)
                continue
            if text_input.lower() == 'стоп':
                break

            self.check_text(text_input)

    def check_text(self, text):
        """Входные данные: текст, имя файла с правилами
        Разбивает текст на слова, удаляет пунктуацию, приводит все к нижнему регистру.
        Проверяет на каком языке слово.
        Проверяет слова и выводит список исправлений."""
        rules = self.load_rules('test_files\\rules.txt')

        splitted_text = [word for word in re.split(r'[ ,.!?]', text) if word.strip() != '']

        for word in splitted_text:
            word_without_punctuation = word.rstrip(string.punctuation)
            tested_word = word_without_punctuation.lower()

            if not all((ord('а') <= ord(char) <= ord('я') or char == 'ё' or char == '-') or char.isdigit() for char in
                       tested_word):
                print(f"Слово '{word}' не на русском")
                continue

            if self.check_consecutive_hyphens(tested_word):
                print(f"Слово '{word}' содержит два дефиса подряд.")
                continue

            corrected_word = rules.get(tested_word)
            if corrected_word is not None:
                print(f"Введённый текст: {word:<30} Исправление: {corrected_word}")
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
                if word.distance == 1.0 or input_word.isdigit():
                    break
                else:
                    suggestions.append(word.word)
            elif word != input_word.lower():
                suggestions.append(word)

        suggestions_list = ' / '.join(suggestions)
        if len(suggestions_list) > 0:
            print("Введённый текст: {0:<30}".format(input_word), "Варианты коррекции:", suggestions_list)

