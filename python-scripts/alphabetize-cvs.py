import sys


def split_and_print_words(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            words = content.split(",")
            words = [word.strip() for word in words]
            words.sort()
            for word in words:
                print(word)
    except FileNotFoundError:
        print(f"File not found: {file_path}")


# Check if a file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide a file path as a command-line argument.")
else:
    file_path = sys.argv[1]
    split_and_print_words(file_path)
