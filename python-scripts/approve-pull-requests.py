#!/opt/homebrew/bin/python3
import os
import requests
import sys
from time import sleep

# Read in CLI arguments for script
if len(sys.argv) < 2:
    print("Please provide a file path and github username as command-line arguments.")
    sys.exit(1)

FILE_PATH = sys.argv[1]
USERNAME = sys.argv[2]

# Generate header for API request
token = os.environ["GH_TOKEN"]
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

review_data = {"event": "APPROVE"}

label_data = {"labels": ["qa-approved"]}

# Read in URLS line by line and store as list
try:
    print("File content:")
    with open(FILE_PATH, "r") as file:
        lines = [line.rstrip() for line in file]
    print(lines)
except FileNotFoundError:
    print(f"File not found: {FILE_PATH}")
except Exception as error:
    print(f"An error occurred: {error}")

# Loop through Pull Requests
for line in lines:
    # Extracting organization and repository name
    repo_slug_start = line.find("github.com/") + len("github.com/")
    repo_slug_end = line.find("/pull/")
    repo_slug = line[repo_slug_start:repo_slug_end]

    # Extracting pull request number
    number_start = line.find("/pull/") + len("/pull/")
    pull_number = line[number_start:]

    url = f"https://api.github.com/repos/{repo_slug}/pulls/{pull_number}"
    pull_request_creator = requests.get(url, headers=headers).json()["user"]["login"]

    # If Pull Request is not opened by USERNAME, skip to next PR
    if pull_request_creator != cSERNAME:
        print(
            f"Skipping {url} because Pull Request was opened by {pull_request_creator}"
        )
        print("Sleeping for 3 seconds to avoid API throttle...\n\n")
        sleep(3)
        continue

    # Approving Pull Request
    url = f"https://api.github.com/repos/{repo_slug}/pulls/{pull_number}/reviews"
    print("REQUEST URL: " + url)
    response = requests.post(url, headers=headers, json=review_data)
    if response.status_code == 200:
        print(f"Pull request approved successfully: {url}")
    else:
        print(f"Request failed with status code: {response.status_code}")

    # Applying qa-approved label to Pull Request
    url = f"https://api.github.com/repos/{repo_slug}/issues/{pull_number}/labels"
    response = requests.post(url, headers=headers, json=label_data)
    if response.status_code == 200:
        print(f"Pull request qa-label applied successfully: {url}")
    else:
        print(f"Request failed with status code: {response.status_code}")

    print("Sleeping for 3 seconds to avoid API throttle...\n\n")
    sleep(3)
