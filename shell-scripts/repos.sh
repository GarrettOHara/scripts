#!/bin/zsh

ORG_NAME="sportngin" # Your organization name
LIMIT=1000           # Set the number of repositories to list

# List repositories in the organization and check for .travis.yml and .travis.yaml
gh repo list "$ORG_NAME" --limit "$LIMIT" --json name | jq -r '.[] | .name' | while read -r repo; do
	# Check if .travis.yml or .travis.yaml file exists in the repository
	if gh api repos/"$ORG_NAME/$repo/contents/.travis.yml" --silent 2>/dev/null || \
        gh api repos/"$ORG_NAME/$repo/contents/.travis.yaml" --silent 2>/dev/null; then
		echo "$repo"
	fi
done
