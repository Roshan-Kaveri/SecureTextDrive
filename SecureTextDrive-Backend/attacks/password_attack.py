import string
from math import gcd

# Define the character set (A-Z, a-z, 0-9, and some symbols)
CHARSET = string.ascii_uppercase + string.ascii_lowercase + string.digits + "@#?!"

# Calculate mod length based on CHARSET
mod_length = len(CHARSET)

# Create a dictionary to map characters to numbers and vice versa
char_to_num = {char: idx for idx, char in enumerate(CHARSET)}
num_to_char = {idx: char for idx, char in enumerate(CHARSET)}


# Function to find the modular inverse of a mod m (Extended Euclidean Algorithm)
def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None  # No inverse exists if gcd(a, m) != 1
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# Decryption function
def decrypt(ciphertext, a):
    decrypted_text = ''
    a_inverse = mod_inverse(a, mod_length)  # Find the modular inverse of a mod mod_length
    if a_inverse is None:
        return None  # Skip this value of a if no inverse exists
    for char in ciphertext:
        if char in char_to_num:
            y = char_to_num[char]
            # D(y) = (a_inverse * y) % mod_length
            decrypted_char = num_to_char[(a_inverse * y) % mod_length]
            decrypted_text += decrypted_char
        else:
            decrypted_text += char  # Non-alphabetic characters remain unchanged
    return decrypted_text


# Brute force attack
def brute_force_attack(ciphertext):
    # Possible values of 'a' that are coprime with mod_length
    possible_keys = [a for a in range(1, mod_length) if gcd(a, mod_length) == 1]

    # Try each possible key and decrypt the message
    for a in possible_keys:
        decrypted_message = decrypt(ciphertext, a)
        if decrypted_message:
            print(f"Key a={a}: {decrypted_message}")


# Example usage:
ciphertext = "de77@f2Lo#U"  # The encrypted message to brute force
print("Attempting brute force attack...")
brute_force_attack(ciphertext)
