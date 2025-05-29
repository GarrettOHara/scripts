#!/bin/bash

# Set the organization name
ORG="sportngin"

# Function to check rate limit
check_rate_limit() {
	rate_limit=$(gh api rate_limit --jq '.resources.search.remaining')
	if [ "$rate_limit" -le 5 ]; then
		echo "Rate limit nearly exceeded. Waiting for 60 seconds..."
		sleep 60
	fi
}

# Function to make API request with retry
make_api_request() {
	local retries=3
	local wait_time=10
	local command="$1"

	for ((i = 0; i < retries; i++)); do
		result=$(eval "$command") && {
			echo "$result"
			return 0
		}
		echo "Request failed. Retrying in $wait_time seconds..."
		sleep $wait_time
		wait_time=$((wait_time * 2))
	done

	echo "Error: API request failed after $retries attempts." >&2
	return 1
}

# Get all repositories for the organization
repos=$(gh repo list $ORG --limit 1000 --json name --jq '.[].name')

# Loop through each repository
for repo in $repos; do
	echo "Checking repository: $repo"

	check_rate_limit

	# Search for .travis.yml
	yml_count=$(make_api_request "gh api -X GET search/code -f q=\"repo:$ORG/$repo filename:.travis.yml\" --jq '.total_count'")

	check_rate_limit

	# Search for .travis.yaml
	yaml_count=$(make_api_request "gh api -X GET search/code -f q=\"repo:$ORG/$repo filename:.travis.yaml\" --jq '.total_count'")

	# If either file is found, print the repository name
	if [ "$yml_count" -gt 0 ] || [ "$yaml_count" -gt 0 ]; then
		echo "Repository $repo contains Travis CI configuration file"
	fi

	# Add a small delay between repository checks
	sleep 2
done
