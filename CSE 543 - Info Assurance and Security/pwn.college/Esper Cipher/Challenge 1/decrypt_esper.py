import argparse
import sys

# Handle command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--decrypt", help='Decrypt a file', required=False)
parser.add_argument("-e", "--encrypt", help='Encrypt a file', required=False)
parser.add_argument("-o", "--outfile", help='Output file', required=False)
parser.add_argument("-k", "--key", help='Key - only used for decryption', required=False)
parser.add_argument("-b", "--bits", help='Bits for key rotation - only used for decryption', required=False)

args = parser.parse_args()

ENCRYPTING = True

try:
    ciphertext = open(args.decrypt, "rb").read()
    ENCRYPTING = False
    if args.key is None or args.bits is None:
        print("Error: Decryption requires both -k (key) and -b (bits).")
        exit(1)

    decryptkey = args.key
    if len(decryptkey) != 7:
        print("Error: The decryption key must be exactly 7 characters.")
        exit(1)

    rotatebits = int(args.bits)
    if not (1 <= rotatebits <= 8):
        print("Error: Rotation bits must be between 1 and 8.")
        exit(1)

except Exception:
    try:
        plaintext = open(args.encrypt, "rb").read()
    except Exception:
        print("Input file error (did you specify -e or -d?)")
        exit(1)


def lrot(n, d):
    """Left rotate a byte by d bits."""
    return ((n << d) & 0xFF) | (n >> (8 - d))


def rrot(n, d):
    """Right rotate a byte by d bits (reverse of lrot)."""
    return ((n >> d) | (n << (8 - d))) & 0xFF


if ENCRYPTING:
    # Encryption Function
    key = "rORTrfA"
    keyxor = [114, 79, 82, 84, 114, 102, 65]
    keyrotate = 2
    print("The key is %s rotated by %d bits." % (key, keyrotate))

    ciphertext = []
    for i in range(len(plaintext)):
        ciphertext.append(lrot(plaintext[i], keyrotate) ^ keyxor[i % len(keyxor)])

    with open(args.outfile, "wb") as output:
        output.write(bytes(ciphertext))
        output.close()

else:
    # **Completely Separate Decryption Function**

    # Extract correct keyxor sequence
    keyxor = [ord(c) for c in decryptkey]
    plaintext = bytearray()

    for i in range(len(ciphertext)):
        # Reverse XOR
        decrypted_byte = ciphertext[i] ^ keyxor[i % len(keyxor)]
        # Reverse Rotation
        restored_byte = rrot(decrypted_byte, rotatebits)
        plaintext.append(restored_byte)

    with open(args.outfile, "wb") as output:
        output.write(plaintext)

    print("Decryption complete! Check", args.outfile)
