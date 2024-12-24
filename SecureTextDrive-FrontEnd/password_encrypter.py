import string
from math import gcd

# Define the character set for mod-n (A-Z, a-z, 0-9, and some symbols)
CHARSET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "@#?!"

# Calculate mod length based on CHARSET
mod_length = len(CHARSET)
print(mod_length)

# Create a dictionary to map characters to numbers and vice versa
char_to_num = {char: idx for idx, char in enumerate(CHARSET)}
num_to_char = {idx: char for idx, char in enumerate(CHARSET)}

# Function to find the modular inverse of a mod m (Extended Euclidean Algorithm)
def mod_inverse(a, m):
    if gcd(a, m) != 1:
        raise ValueError(f"No modular inverse for a={a} mod m={m}. They are not coprime.")
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Modular inverse does not exist for a={a} mod m={m}.")

# Encryption function
def encrypt(plaintext, a):
    encrypted_text = ''
    for char in plaintext:
        if char in char_to_num:
            x = char_to_num[char]
            # E(x) = (a * x) % mod_length
            encrypted_char = num_to_char[(a * x) % mod_length]
            encrypted_text += encrypted_char
        else:
            encrypted_text += char  # Non-alphabetic characters remain unchanged
    return encrypted_text

# Decryption function
def decrypt(ciphertext, a):
    decrypted_text = ''
    a_inverse = mod_inverse(a, mod_length)  # Find the modular inverse of a mod mod_length
    for char in ciphertext:
        if char in char_to_num:
            y = char_to_num[char]
            # D(y) = (a_inverse * y) % mod_length
            decrypted_char = num_to_char[(a_inverse * y) % mod_length]
            decrypted_text += decrypted_char
        else:
            decrypted_text += char  # Non-alphabetic characters remain unchanged
    return decrypted_text

# Example usage:
# a = 23  # Encryption key, must be coprime with mod_length
# plaintext = "Hello123@#?ooopppp"
#
# # Encrypt the message
# ciphertext = encrypt(plaintext, a)
# print(f"Encrypted: {ciphertext}")
#
# # Decrypt the message
# decrypted_message = decrypt(ciphertext, a)
# print(f"Decrypted: {decrypted_message}")
