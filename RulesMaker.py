
def save_rules(rules, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        for incorrect_word, correct_word in rules.items():
            file.write(f"{incorrect_word}:{correct_word}\n")


def load_rules(filename):
    rules = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                incorrect_word, correct_word = line.split(':')
                rules[incorrect_word] = correct_word

    return rules
