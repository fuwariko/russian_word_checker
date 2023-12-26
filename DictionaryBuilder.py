import string


def build_vocab(corpus):
    text = ""
    with open(corpus, 'r', encoding='utf-8') as file:
        for line in file:
            text += line

    tokens = text.lower().split()
    tokens = [token.strip(string.punctuation) for token in tokens if token.strip(string.punctuation)]
    unique_words = set(tokens)
    with open('test_files/new_dictionary.txt', 'a', encoding='utf-8') as file:
        for word in unique_words:
            file.write(f"{word}\n")


build_vocab('test_files/text.txt')
