#!/opt/pwn.college/python

import glob
import hashlib

EXPECTED = "c8579d69a72dc24609d268d6e263daf018f4da025341240a2d47f79d1cbb7bb7"


def grade():
    # find esper_plaintext.txt
    if 'esper_plaintext.txt' not in glob.glob("*"):
        print('esper_plaintext.txt is not found.')
        return

    # open caesarplaintext.txt
    with open('esper_plaintext.txt', 'rb') as f:
        data = f.read()

    # try to decode it
    try:
        txt = data.decode("ascii")
    except UnicodeDecodeError:
        print('esper_plaintext.txt cannot be decoded as ASCII text.')
        return

    txt = txt.strip("\r\n ")
    checksum = hashlib.sha256(txt.encode("ascii")).hexdigest()

    if checksum == EXPECTED:
        print("Good job!")
        print("Here is your flag:")
        with open("/flag", "r") as f:
            print(f.read())
    else:
        print("Incorrect plaintext.")


if __name__ == "__main__":
    grade()
