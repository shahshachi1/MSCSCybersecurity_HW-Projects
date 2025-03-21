import string

# Read the key from caesarkey.txt
key_file_path = "/mnt/data/caesarkey.txt"
with open(key_file_path, "r") as key_file:
    key_line = key_file.read().strip()
    key_letter = key_line.split()[-1]  # Extract the last word ("K")
    key_shift = string.ascii_uppercase.index(key_letter)  # Convert to integer (K=10)

# Read the ciphertext from ciphertext.txt
ciphertext_file_path = "/mnt/data/ciphertext.txt"
with open(ciphertext_file_path, "r") as cipher_file:
    ciphertext = cipher_file.read().strip()

# Define the decryption function
def caesar_decrypt(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char in string.ascii_uppercase:
            decrypted_text += string.ascii_uppercase[(string.ascii_uppercase.index(char) - shift) % 26]
        else:
            decrypted_text += char  # Should not happen as per the problem statement
    return decrypted_text

# Decrypt the ciphertext
decrypted_text = caesar_decrypt(ciphertext, key_shift)

# Save the decrypted text to caesarplaintext.txt
plaintext_file_path = "/challenge/caesarplaintext.txt"
with open(plaintext_file_path, "w") as plaintext_file:
    plaintext_file.write(decrypted_text)

print("Decryption completed. The decrypted text is saved in caesarplaintext.txt.")

#final command: run: /challenge/challenge.py
