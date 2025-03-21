1. Copy files from /challenge/ folder (including the ciphertext.txt)
2. Re-encrypt it correctly if need be by running:
	python esper.py -e plaintext.txt -o ciphertext.txt
3. Verify the ciphertext:
	ls -l ciphertext.txt
	sha256sum ciphertext.txt
4. Decrypt: 
	python decrypt_esper.py -d ciphertext.txt -o esper_plaintext.txt -k rORTrfA -b 2
5. Check if the ciphertext.txt is readable:
	cat esper_plaintext.txt
6. Final validation with challenge.py
	/challenge/challenge.py

