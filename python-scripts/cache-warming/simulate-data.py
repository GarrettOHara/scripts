#!/usr/bin/env python3
"""
simulated-data.py

Generates a JSON file of simulated cache_key entries,
with a controlled amount of duplicate values.
Each entry is a dict {"cache_key": <random_string>}.
By default, 10% of the total entries are unique keys; the remainder
are randomly sampled (with replacement) from those unique keys,
ensuring many duplicates.
"""
import sys
import json
import random
import string

# Configuration: average sentence length and variability
MEAN_LENGTH = 80   # average length of cache_key strings
STDDEV_LENGTH = 20 # standard deviation for string length
DUPLICATE_RATIO = 0.9  # fraction of entries that are duplicates


def random_string(mean=MEAN_LENGTH, stddev=STDDEV_LENGTH):
    """
    Generate a random string whose length is sampled from a Gaussian
    distribution around `mean` with standard deviation `stddev`.
    Minimum length is 1.
    """
    length = max(1, int(random.gauss(mean, stddev)))
    alphabet = string.ascii_letters + string.digits + '_:'
    return ''.join(random.choices(alphabet, k=length))


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <number_of_entries> <output_filename>")
        sys.exit(1)

    try:
        total = int(sys.argv[1])
        if total < 1:
            raise ValueError()
    except ValueError:
        print("Please provide a positive integer for number_of_entries.")
        sys.exit(1)

    # Determine how many unique keys to generate
    unique_count = max(1, int(total * (1 - DUPLICATE_RATIO)))
    print(f"Generating {unique_count} unique keys...")
    unique_keys = [ random_string() for _ in range(unique_count) ]

    # Build final list with duplicates sampled from unique_keys
    print(f"Sampling {total} entries ({DUPLICATE_RATIO*100:.0f}% duplicates)...")
    data = [ {"cache_key": random.choice(unique_keys)} for _ in range(total) ]

    # Write to JSON file
    with open(sys.argv[2], 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Wrote {total} simulated entries (with duplicates) to '{sys.argv[2]}'")


if __name__ == '__main__':
    main()