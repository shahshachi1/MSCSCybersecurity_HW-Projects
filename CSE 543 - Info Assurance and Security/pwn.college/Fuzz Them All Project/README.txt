1. Setup
	- chmod +x prog
	- chmod +x fuzzer.py

2. Copy and paste into Terminal:
	python3 -c "
	import struct
	chunks = [b'A' * 20, b'B' * 30]
	seed = struct.pack('<H', len(chunks))
	for chunk in chunks:
    		seed += struct.pack('<H', len(chunk)) + chunk
	open('_seed_', 'wb').write(seed)
	"

3. Run Your Fuzzer
	- Example: ./fuzzer.py 1337 50000 > level-1.crash

4. Check for Crash
	- Example: ./prog < level-1.crash

5. In pwn.college vm
	- Example: /challenge/challenge < level-1.crash
