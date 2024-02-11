import math

import main


def string_to_matrix(string):
    """
    This function transform a string input into a matrix of characters of dimension 2*(N - N%2)/2
    :param string: even sized string. else, last char is dropped
    """
    n = len(string)
    return [[string[i + j] for i in range(0, n - 1, 2)] for j in range(2)]


def text_matrix_to_digit(matrix, t):
    """
    Convert a char matrix to its number matrix
    :param matrix: each element is a char. if not in the table, error is thrown
    :param t: table of conversion for chars to number in the matrix to the alphabet.
    :return: matrix of the same dimension but with each char converted according to the table
    """
    return [[t[elem] for elem in row] for row in matrix]


def matrix_to_string(matrix, t):
    """
    from an encoded matrix to a string of character
    :param matrix: matrix 2*n, where the correspondance between elements and chars is given by table t
    :param t: the aforementionned t
    :return: text string corresponding to the matrix
    """
    i_inverse = {v: k for k, v in t.items()}
    return ''.join([i_inverse[elem] for col in zip(*matrix) for elem in col])


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
    return [[(factor * elem) % mod for elem in row] for row in adjugate(matrix)]


def mult_matrix_mod(a, b, mod):
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            # Compute the dot product of the ith row of a and the jth column of b
            dot_product = sum(a[i][k] * b[k][j] for k in range(len(b))) % mod
            row.append(dot_product)
        result.append(row)
    return result


def decrypt(cipher, key, t):
    mod = len(t)
    C = text_matrix_to_digit(string_to_matrix(cipher), t)
    K_inverse = invert_matrix_mod(key, mod)
    P = mult_matrix_mod(K_inverse, C, mod)
    return matrix_to_string(P, t)


def key_from_known_plaintext(plaintext, cipher, t):
    """
    :param plaintext: plaintext supposed coresponding to cipher. length must be 4
    :param cipher : cipher corresponding to aforementionned plaintext, length must be 4
    :param t: table to retrieve numeric values from key strings
    :return: key matrix if the pair was correctly formatted and the plaintext matrix invertible. ELse, raise error
    """
    if len(plaintext) != 4 or len(cipher) != 4:
        raise ValueError(f"Found lengths {(len(plaintext), len(cipher))}. Expected (4,4).")

    p = plaintext
    c = cipher
    p_matrix = text_matrix_to_digit(string_to_matrix(p), t)
    c_matrix = text_matrix_to_digit(string_to_matrix(c), t)
    mod = len(t)

    return mult_matrix_mod(c_matrix, invert_matrix_mod(p_matrix, mod), mod)


def test_key_from_quadgrams(cipher,supposed_quad,table):
    results = {}
    for p in supposed_quad:
        for i in main.count_quadgrams(cipher, False).keys():
            k = f"{p}={i}"
            try:
                v = decrypt(cipher, key_from_known_plaintext(p, i, table), table)
                # main.plot_frequencies(main.to_frequencies_sorted(main.letter_count(v), len(v)))
            except ValueError as e:
                v = e
            results[k] = v
    for k, v in results.items():
        print(f"Trying with {k}\n{v}\n")
    return results



