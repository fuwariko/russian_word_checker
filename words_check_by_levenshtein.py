import hashlib
from Levenshtein_algorithm import get_levenshtein_distance
from WordWithDistance import WordWithDistance
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import os


class LevenshteinWordCheck:
    def __init__(self, key) -> None:
        """Загружает словарь.
        Создает список объектов класса WordWithDistance,
        где объект - слово из словаря и расстояние Левенштейна до введенного слова."""
        self.sorting = key
        self.cache = {}
        a = os.getcwd()
        a = os.path.dirname(a)
        with open('test_files\\dictionary.txt', 'r', encoding='utf-8') as data_file:
            words = data_file.read().split('\n')
            self.data = [WordWithDistance(word) for word in words]
            self.max_len = max(len(word_with_d.word) for word_with_d in self.data)
            self.counter = Counter(words.word for words in self.data)
            self.total = float(sum(self.counter.values()))

    def get_suggested_words(self, word) -> list[WordWithDistance]:
        """Сортирует результаты по ключу сортировки,
        заданному при инициализации объекта класса.
        Возвращает первые три слова с наименьшим расстоянием"""

        distance = self.get_distance(word)
        suggested_words = sorted(distance, key=self.sorting, reverse=True)
        suggested_words = suggested_words[:3]
        for suggestion in suggested_words:
            suggestion.other = word
        return suggested_words

    @staticmethod
    def add_distance(word, input_word):
        word.distance = get_levenshtein_distance(word.word, input_word)
        return word

    def get_distance(self, word) -> list[WordWithDistance]:
        """Вычисляет расстояние Левенштейна между введенным словом и каждым словом в словаре.
         Проверяет, есть ли результаты в кэше по хэш-ключу ведденого слова.
         есть - возвращает результаты из кэша.
         нет - создает пул потоков выполнения
         и для каждого слова в словаре отправляет задачу вычисления расстояния Левенштейна в потоки.
         В конце  результаты собираются в список.
         Сохраняются в кэш по хэш-ключу введенного слова."""

        key = hashlib.md5(word.encode('utf-8')).hexdigest()
        if key in self.cache:
            return self.cache[key]

        with ThreadPoolExecutor() as executor:
            futures = []
            for word_with_d in self.data:
                future = executor.submit(self.add_distance, word_with_d, word)
                futures.append(future)

        results = [future.result() for future in futures]
        self.cache[key] = results
        return results


