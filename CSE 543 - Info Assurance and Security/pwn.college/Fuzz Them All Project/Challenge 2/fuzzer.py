#!/usr/bin/env python3
import sys
import random

def mutate(data, prng_seed, num_iterations):
    random.seed(prng_seed)
    data = bytearray(data)

    for i in range(num_iterations):
        # 13% chance to change each byte
        for j in range(len(data)):
            if random.random() < 0.13:
                data[j] = random.randint(0, 255)

        # Extend input every 500 iterations
        if (i + 1) % 500 == 0:
            data += bytearray(random.randint(0, 255) for _ in range(10))

    return data

def main():
    if len(sys.argv) != 3:
        print("Usage: ./fuzzer.py prng_seed num_iterations", file=sys.stderr)
        sys.exit(1)

    prng_seed = int(sys.argv[1])
    num_iterations = int(sys.argv[2])

    with open("_seed_", "rb") as f:
        seed = f.read()

    result = mutate(seed, prng_seed, num_iterations)
    sys.stdout.buffer.write(result)

if __name__ == "__main__":
    main()


