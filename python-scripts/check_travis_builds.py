import requests

# Your GitHub personal access token
GITHUB_TOKEN = "your_personal_access_token"
ORG_NAME = "sportngin"

# Base URL for GitHub API
GITHUB_API_URL = "https://api.github.com"

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repositories(org_name):
    """Retrieve all repositories for the given organization."""
    url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
    repos = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def check_travis_file(repo_name):
    """Check if the repo contains .travis.yaml or .travis.yml file."""
    possible_files = ['.travis.yaml', '.travis.yml']
    for file in possible_files:
        url = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{repo_name}/contents/{file}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
    return False

def main():
    repos = get_repositories(ORG_NAME)
    repos_with_travis = []

    for repo in repos:
        repo_name = repo['name']
        print(f"Checking repository: {repo_name}")
        if check_travis_file(repo_name):
            repos_with_travis.append(repo_name)

    if repos_with_travis:
        print("\nRepositories with .travis.yaml or .travis.yml:")
        for repo in repos_with_travis:
            print(repo)
    else:
        print("\nNo repositories found with .travis.yaml or .travis.yml.")

if __name__ == "__main__":
    main()

