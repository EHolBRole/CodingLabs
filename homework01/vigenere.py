def encrypt_vigenere(plaintext="", keyword="") -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    i = 0
    # abra abra abra test test
    # abra abra abra test test
    while len(plaintext) > len(keyword):
        keyword += keyword[i]
        i += 1
    for i in range(0, len(plaintext)):
        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                ciphertext += chr((ord(plaintext[i]) + (ord(keyword[i]) - 65) - 64) % 26 + 64)
            else:
                ciphertext += chr((ord(plaintext[i]) + (ord(keyword[i]) - 97) - 97) % 26 + 97)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext="", keyword=""):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    i = 0
    while len(ciphertext) > len(keyword):
        keyword += keyword[i]
        i += 1
    for i in range(0, len(ciphertext)):
        if ciphertext[i].isalpha():
            if ciphertext[i].isupper():
                plaintext += chr((ord(ciphertext[i]) - (ord(keyword[i]) - 65) - 64) % 26 + 64)
            else:
                plaintext += chr((ord(ciphertext[i]) - (ord(keyword[i]) - 97) - 97) % 26 + 97)
        else:
            plaintext += ciphertext[i]
    return plaintext
