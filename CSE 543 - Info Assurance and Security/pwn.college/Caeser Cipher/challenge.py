#!/opt/pwn.college/python

import glob
import hashlib

EXPECTED = "2edc7214153f529c32bb561514935f5286c9a77baba3c2990b461565275bc793"


def grade():
    # find caesarplaintext.txt
    if 'caesarplaintext.txt' not in glob.glob("*"):
        print('caesarplaintext.txt is not found.')
        return

    # open caesarplaintext.txt
    with open('caesarplaintext.txt', 'rb') as f:
        data = f.read()

    # try to decode it
    try:
        txt = data.decode("ascii")
    except UnicodeDecodeError:
        print('caesarplaintext.txt cannot be decoded as ASCII text.')
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