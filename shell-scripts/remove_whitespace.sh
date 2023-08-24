#!/bin/bash

# Check if a JSON file name is provided as an argument
if [ $# -eq 0 ]; then
  echo "Error: JSON file name not provided."
  echo "Usage: bash remove_whitespace.sh <json_file>"
  exit 1
fi

json_file="$1"

# Check if the JSON file exists
if [ ! -f "$json_file" ]; then
  echo "Error: JSON file '$json_file' not found."
  exit 1
fi

# Read the JSON file and remove the whitespace using jq
json=$(cat "$json_file")
json_string=$(echo "$json" | jq -c .)

echo -n "$json_string"
