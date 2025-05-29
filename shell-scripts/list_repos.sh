#!/bin/zsh

ORG_NAME="sportngin" # Replace with your organization name
LIMIT=100            # Set the number of repositories to list

# List repositories in the organization and check for .travis.yml
gh repo list "$ORG_NAME" --limit "$LIMIT" | while read -r repo _; do
  # Check if the .travis.yml file exists in the repository
  if gh api repos/"$repo"/contents/.travis.yml --silent; then
    echo "$repo contains .travis.yml"
  else
    # Suppress the 404 error output
    gh api repos/"$repo"/contents/.travis.yml --silent 2>/dev/null
  fi
done
