import main


def to_matrix(string):
    """
    This function transform a string input into a matrix of characters of dimension 2*(N - N%2)/2
    :param string: even sized string. else, last char is dropped
    """
    n = len(string)
    return [[string[i + j] for i in range(0, n - 1, 2)] for j in range(2)]


def to_digit(matrix, table):
    """

    :param matrix: each element is a char. if not in the table, error is thrown
    :param table: table of conversion for chars to number in the matrix to the alphabet.
    :return: matrix of the same dimension but with each char converted according to the table
    """
    return [[table[elem] for elem in row] for row in matrix]


def load_cipher(filename):
    """
    read the file and return it as a string
    """
    with open(filename, 'r') as f:
        return f.read()


def cipher_frequencies_graph(cipher):
    """
    plot count of recurring 2-uple and 4-uple for manual association with probable plain text
    :param cipher: string of the cipher
    """
    d = main.count_digrams(cipher, False)
    q = main.count_quadgrams(cipher, False)
    main.plot_frequencies(d, "Digram Graph", "green")
    main.plot_frequencies(q, "Quadgram Graph", "red")


def invertible_mod(matrix, mod):
    pass


def invert_matrix_mod(matrix, mod):
    if not invertible_mod(matrix, mod):
        raise ValueError(f"{matrix} not invertible mod {mod}")
    pass


def mult_matrix_mod(a, b, mod):
    pass



def key_from_known_plaintext(pair, table):
    """
    :param table: table to retrieve numeric values from key strings
    :param pair: Pair (plaintext, cipher) used to retrieve the key, as string. both must be of length 4
    :return: key matrix if the pair was correctly formatted and the plaintext matrix invertible. ELse, raise error
    """
    if len(pair[0] != 4 or len(pair[1] != 4)):
        raise ValueError(f"Found lengths {(len(pair[0]), len(pair[1]))}. Expected (4,4).")

    p = pair[0]
    c = pair[1]
    p_matrix = to_digit(to_matrix(p), table)
    c_matrix = to_digit(to_matrix(c), table)
    mod = len(table)

    return mult_matrix_mod(c_matrix, invert_matrix_mod(p_matrix, mod), mod)









print(to_digit(to_matrix("aabbaabb"), {'a': 0, 'b': 9}))
