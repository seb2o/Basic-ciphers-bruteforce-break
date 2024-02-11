from itertools import zip_longest

import matplotlib.pyplot as plt


def plot_frequencies(d, t="Graph", c=None):
    plt.figure(figsize=(30, 10))
    plt.bar(list(d.keys()), list(d.values()), color=c)
    plt.title(t)
    plt.show()


def count_digrams(text, sliding=True):
    digram_count = {}
    n = len(text)
    if sliding:
        for i in range(n - 1):
            digram = text[i:i + 2]
            if digram in digram_count:
                digram_count[digram] += 1
            else:
                digram_count[digram] = 1
        return {k: v for k, v in digram_count.items() if v > 10}
    else:
        for i in range(0, n, 2):
            digram = text[i:i + 2]
            if digram in digram_count:
                digram_count[digram] += 1
            else:
                digram_count[digram] = 1
        return {k: v for k, v in digram_count.items() if v > 4}


def count_trigrams(text):
    trigram_count = {}
    for i in range(len(text) - 2):
        trigram = text[i:i + 3]
        if trigram in trigram_count:
            trigram_count[trigram] += 1
        else:
            trigram_count[trigram] = 1
    return {k: v for k, v in trigram_count.items() if v > 2}


def count_quadgrams(text, sliding=True):
    quadgram_count = {}
    n = len(text)
    if sliding:
        for i in range(n - 3):
            quadgram = text[i:i + 4]
            if quadgram in quadgram_count:
                quadgram_count[quadgram] += 1
            else:
                quadgram_count[quadgram] = 1
        return {k: v for k, v in quadgram_count.items() if v > 2}
    else:
        for i in range(0, n, 4):
            quadgram = text[i:i + 4]
            if quadgram in quadgram_count:
                quadgram_count[quadgram] += 1
            else:
                quadgram_count[quadgram] = 1
        return {k: v for k, v in quadgram_count.items() if v > 1}


def letter_count(s):
    occurences = {}
    for c in s:
        # if c in "AZERTYUIOPQSDFGHJKLMWXCVBN":
        if c in occurences:
            occurences[c] = occurences[c] + 1
        else:
            occurences[c] = 1
    return occurences


def to_frequencies_sorted_alphabetically(d, n=1):
    return {k: d[k] / n for k in sorted(d)}


def to_frequencies_sorted(d, n):
    return {k: v / n for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}


def visualize_substitution(table, c_freq, s_freq):
    characters = list(table.items())

    plot_frequencies(c_freq, "Cipher frequencies")
    plot_frequencies(s_freq, "Sample english text frequencies")

    table_ordered_c_freq, table_ordered_s_freq = zip(*[(c_freq.get(c, 0), s_freq.get(s, 0)) for c, s in table.items()])

    # Setting up bar positions
    x = range(len(characters))
    bar_width = 0.35

    # Plotting
    plt.figure(figsize=(20, 10))
    plt.bar(x, table_ordered_c_freq, width=bar_width, label='Ciphertext')
    plt.bar([p + bar_width for p in x], table_ordered_s_freq, width=bar_width, label='Sample English Text')

    # Adding labels and title
    plt.xlabel('Characters')
    plt.ylabel('Frequency of Appearance')
    plt.title('Frequency of Appearance of Characters in Ciphertext and Sample English Text')
    plt.xticks([p + bar_width / 2 for p in x], characters)
    plt.legend()

    # Show plot
    plt.tight_layout()
    plt.show()


def decode_substitution(c, s, manual_pairs):
    c_freq = to_frequencies_sorted(letter_count(c), len(c))
    s_freq = to_frequencies_sorted(letter_count(s), len(s))

    # Find keys present in s_freq but not in c_freq
    missing_keys_c_freq = set(s_freq.keys()) - set(c_freq.keys())
    # Find keys present in c_freq but not in s_freq
    missing_keys_s_freq = set(c_freq.keys()) - set(s_freq.keys())
    # Update c_freq with missing keys
    for key in missing_keys_c_freq:
        c_freq[key] = 0
    # Update s_freq with missing keys
    for key in missing_keys_s_freq:
        s_freq[key] = 0

    table = {e: (lambda l, f: l if f[l] > .001 else '_')(d, s_freq) for (e, d) in zip(c_freq, s_freq)}

    for (encoded, decoded) in manual_pairs.items():
        inverse_table = {v: k for (k, v) in table.items()}
        previous_association_value = table[encoded]
        table[encoded] = decoded
        table[inverse_table[decoded]] = previous_association_value

    visualize_substitution(table, c_freq, s_freq)
    return [table[letter] if letter in table else letter for letter in c]


def show_cipher_letter_frequencies(c, name):
    occurences = letter_count(c)
    n = len(occurences)
    sorted_alphabetically = to_frequencies_sorted_alphabetically(occurences, n)
    sorted_by_frequencies = to_frequencies_sorted(occurences, n)
    plot_frequencies(sorted_alphabetically, f"{name} : Sorted alphabetically")
    plot_frequencies(sorted_by_frequencies, f"{name} : Sorted by frequencies")


def ciphers_1gram_frequency_plot(filenames):
    for i in filenames:
        with open(i, 'r') as f:
            show_cipher_letter_frequencies(f.read(), i)


def find_partial_3_gram(string, match, wild_card_index):
    found = ""
    for i in range(len(string) - 3):
        box = string[i, i + 3]
        if wild_card_index == 3:
            if box[:-1] == match:
                found += f"{match}*  "
        if wild_card_index == 0:
            if box[1:] == match:
                found += f"*{match}  "
        if box[:wild_card_index] == match[:wild_card_index] and box[wild_card_index + 1:] == match[
                                                                                             wild_card_index + 1:]:
            found += f"{match[:wild_card_index]}*{match[wild_card_index + 1:]}"


def stream_separate(cipher, key_length):
    n_blocks = len(cipher) // key_length
    return [''.join([cipher[i + j] for j in range(0, n_blocks * key_length, key_length)]) for i in range(key_length)]


def text_stream_frequencies(stream_list, filename):
    for s in stream_list:
        plot_frequencies(to_frequencies_sorted(letter_count(s), len(s)), filename)


def caesar_shift(cipher, letter_key):
    letter_to_digit = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
        'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
        'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17,
        'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
        'Y': 24, 'Z': 25, ',': 26, '.': 27, '-': 28
    }
    digit_to_letter = {v: k for k, v in letter_to_digit.items()}
    shift_value = letter_to_digit[letter_key] - 4  # 4 is the value for E, the most frequent letter
    return [digit_to_letter[(letter_to_digit[c] - shift_value) % 29] for c in cipher]


def reorder_viginere(stream):
    block_length = len(stream[0])
    return [block[i] for i in range(block_length) for block in stream]


def decode_viginere(stream_list, english_freq):
    decoded = []
    plot_frequencies(english_freq)
    for c in stream_list:
        count = letter_count(c)
        plot_frequencies(to_frequencies_sorted(count, len(c)))
    #     plot_frequencies(to_frequencies_sorted_alphabetically(count, len(c)))
    #     cipher_freq = to_frequencies_sorted(count, len(c))
    #     decoded.append(caesar_shift(c, next(iter(cipher_freq))))
    # print(reorder_viginere(decoded))


def main():
    english_freq = {'E': .1193, 'T': .088, 'A': .079, 'O': .0752, 'I': .0682, 'H': .0642, 'N': .0623, 'S': .0599,
                    'R': .0554,
                    'D': .0436, 'L': .0400, 'U': .0283, 'M': .0264, 'W': .0237, 'Y': .0224, 'F': .0211, 'C': .021,
                    'G': .0189,
                    ',': .017, '.': .015, 'P': .0147, 'B': .0137, 'V': .0092, 'K': .0075, '-': .0021, 'X': .0014,
                    'Q': .0011,
                    'J': .0009, 'Z': .0004}
    files = ["0.txt", "2.txt"]
    with open("test.txt", 'r') as f:
        plot_frequencies(to_frequencies_sorted(letter_count(f.read()), 1000))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
