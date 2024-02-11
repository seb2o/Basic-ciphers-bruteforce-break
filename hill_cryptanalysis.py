import math

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


def plot_cipher_frequencies(cipher):
    """
    plot count of recurring 2-uple and 4-uple for manual association with probable plain text
    :param cipher: string of the cipher
    """
    d = main.count_digrams(cipher, False)
    q = main.count_quadgrams(cipher, False)
    main.plot_frequencies(d, "Digram Graph", "green")
    main.plot_frequencies(q, "Quadgram Graph", "red")


def det(matrix):
    """
    :param matrix: 2*2 matrix with digit as element
    :param mod: modulo for the operation
    :return: the determinant of the matrix, modulo mod. error if matrix ill formatted
    """
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def adjugate(matrix):
    """
    :param matrix: 2x2 matrix
    :return: adjugate of the matrix
    """
    return [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]


def invert_matrix_mod(matrix, mod):
    factor = pow(det(matrix), -1, mod)
    return [[(factor*elem) % mod for elem in row] for row in adjugate(matrix)]


def mult_matrix_mod(a, b, mod):
    result = []
    for i in range(2):
        row = []
        for j in range(2):
            # Compute the dot product of the ith row of a and the jth column of b
            dot_product = sum(a[i][k] * b[k][j] for k in range(2)) % mod
            row.append(dot_product)
        result.append(row)
    return result


def key_from_known_plaintext(plaintext, cipher, table):
    """
    :param plaintext: plaintext supposed coresponding to cipher. length must be 4
    :param cipher : cipher corresponding to aforementionned plaintext, length must be 4
    :param table: table to retrieve numeric values from key strings
    :return: key matrix if the pair was correctly formatted and the plaintext matrix invertible. ELse, raise error
    """
    if len(plaintext) != 4 or len(cipher) != 4:
        raise ValueError(f"Found lengths {(len(plaintext), len(cipher))}. Expected (4,4).")

    p = plaintext
    c = cipher
    p_matrix = to_digit(to_matrix(p), table)
    c_matrix = to_digit(to_matrix(c), table)
    mod = len(table)

    return mult_matrix_mod(c_matrix, invert_matrix_mod(p_matrix, mod), mod)


# plot_cipher_frequencies(load_cipher("2-Hill-NoPunctuation.txt"))
table = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
        'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
        'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17,
        'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
        'Y': 24, 'Z': 25, '1': 26, '2': 27, '3': 28
    }

print(key_from_known_plaintext("THAT", "O2XZ", table))







