#!/usr/bin/env python3
"""
generate_series.py

Calls simulated-data.py with a growing number of entries.
Each iteration doubles the number of entries, and
the JSON output gets renamed to simulated-data-<i>.json.
"""

import sys
import subprocess
import os

# Configuration: you can adjust these defaults or pass as arguments
INITIAL_SIZE   = 1000   # number of entries in the first run
ITERATIONS     = 5      # how many times to double
SIM_SCRIPT     = "simulate-data.py"
BASE_OUTPUT    = "simulated-data.json"

def main():
    # Optional: allow overrides via command-line
    global INITIAL_SIZE, ITERATIONS
    if len(sys.argv) == 3:
        INITIAL_SIZE = int(sys.argv[1])
        ITERATIONS   = int(sys.argv[2])
    elif len(sys.argv) != 1:
        print(f"Usage: {sys.argv[0]} [initial_size iterations]")
        sys.exit(1)

    size = INITIAL_SIZE
    for i in range(1, ITERATIONS + 1):
        print(f"\nIteration {i}: generating {size} entries…")
        # Call the simulated-data script
        subprocess.run(
            ["python3", SIM_SCRIPT, str(size), BASE_OUTPUT],
            check=True
        )

        # Rename the output file
        target = f"simulated-data-{i}.json"
        if os.path.exists(target):
            os.remove(target)
        os.rename(BASE_OUTPUT, target)
        print(f"→ saved to {target}")

        # double for next iteration
        size *= 2

if __name__ == "__main__":
    main()