python3 -c "
import struct
chunks = [b'A' * 20, b'B' * 30]
seed = struct.pack('<H', len(chunks))
for chunk in chunks:
    seed += struct.pack('<H', len(chunk)) + chunk
open('_seed_', 'wb').write(seed)
"

