#!/opt/homebrew/bin/python3

import secrets
import subprocess


def read_file(file_path: str):
    """
    Read a file passed to function, return every
    line in file as a string in a Python List.
    """
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


def create_random_string():
    """
    Create random string to check data integrity.
    """
    return secrets.token_hex(50)


def execute_mysql_command(command: str):
    """
    Construct a command for the MySQL database and
    return STDOUT as a string.
    """
    # Grab credentials from environment variables
    host = os.environ.get("MYSQL_PROD_HOST")
    user = os.environ.get("MYSQL_PROD_USERNAME")
    password = os.environ.get("MYSQL_PROD_PASSWORD")
    database = os.environ.get("MYSQL_PROD_DATABASE")

    # Build the command string
    cmd = f"mysql -h {host} -u {user} -p{password} {database} -e '{command}'"

    # Execute the command and capture STDOUT
    result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)

    # Cast result to string, print to console, return string
    output = result.stdout.decode("utf-8")
    print(output)
    return output


if __name__ == "__main__":
    # Read in SQL commands to create terratest database
    lines = read_file("./mysql_commands.txt")

    # Execute the commands on the MySQL database
    # TODO: refactor so all commands are sent at once?
    for line in lines:
        execute_mysql_command(line)

    # Insert random data into terratest table to check data integrity
    execute_mysql_command(
        f"INSERT INTO terratest (name) VALUES ('create_random_string()');"
    )

    # Print out table and random data
    print(execute_mysql_command("SELECT * FROM terratest"))
