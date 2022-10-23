import typing as tp


def encrypt_caesar(plaintext="", key=3):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for c in plaintext:
        if c.isalpha():
            if c.isupper():
                ciphertext += chr((ord(c) + key - 64) % 26 + 64)
            else:
                ciphertext += chr((ord(c) + key - 97) % 26 + 97)
        else:
            ciphertext += c
    return ciphertext


def decrypt_caesar(ciphertext="", key=3):
    """
    Decrypts a ciphertext using a Caesar cipher.


    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for c in ciphertext:
        if c.isalpha():
            if c.isupper():
                plaintext += chr((ord(c) - key - 64) % 26 + 64)
            else:
                plaintext += chr((ord(c) - key - 97) % 26 + 97)
        else:
            plaintext += c

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
