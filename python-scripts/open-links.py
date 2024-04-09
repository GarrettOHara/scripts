#!/opt/homebrew/bin/python3
import os
import sys
from time import sleep

# Read in CLI arguments for script
if len(sys.argv) < 2:
    print("Please provide a file path and github username as command-line arguments.")
    sys.exit(1)

FILE_PATH = sys.argv[1]

# Read in URLS line by line and store as list
try:
    print("File content:")
    with open(FILE_PATH, "r") as file:
        urls = [line.rstrip() for line in file]
    print(lines)
except FileNotFoundError:
    print(f"File not found: {FILE_PATH}")
except Exception as error:
    print(f"An error occurred: {error}")

# Loop through Pull Requests
for url in urls:
    os.system(f"open {url}")

