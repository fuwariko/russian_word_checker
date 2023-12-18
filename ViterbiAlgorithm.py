def viterbi_segment(text, checker):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        max_probability = 0
        max_probability_index = 0

        for j in range(max(0, i - checker.max_len), i):
            current_probability = probs[j] * (checker.counter[text[j:i]] / checker.total)

            if current_probability > max_probability:
                max_probability = current_probability
                max_probability_index = j

        prob_k, k = max_probability, max_probability_index

        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words
