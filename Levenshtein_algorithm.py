def get_levenshtein_distance(first_word: str, second_word: str) -> int:
    first_word = first_word.lower()
    second_word = second_word.lower()

    deletion_cost = 1
    insertion_cost = 1

    len_s1 = len(first_word)
    len_s2 = len(second_word)

    matrix = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        matrix[i][0] = i * deletion_cost
    for j in range(len_s2 + 1):
        matrix[0][j] = j * insertion_cost

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if first_word[i - 1] != second_word[j - 1]:
                substitution_cost = 1
            else:
                substitution_cost = 0

            del_cost = matrix[i - 1][j] + deletion_cost
            ins_cost = matrix[i][j - 1] + insertion_cost
            sub_cost = matrix[i - 1][j - 1] + substitution_cost

            matrix[i][j] = min(del_cost, ins_cost, sub_cost)

    max_len = max(len_s1, len_s2)
    result = 1 - matrix[-1][-1] / max_len
    return result
