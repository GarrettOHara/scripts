#!/bin/zsh

export REPO_OWNER="sportngin"

response=$(curl -s -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/orgs/$REPO_OWNER/actions/runs?status=in_progress")

# Check if the response contains .workflow_runs
if [[ $(echo $response | jq -e '.workflow_runs') != "null" ]]; then
  echo $response | jq '.workflow_runs[] | {repository: .repository.name, workflow: .workflow.name, status: .status}'
else
  echo "No running workflows found."
fi

