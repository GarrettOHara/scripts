#!/bin/bash

# Use existing env var
API_KEY="${OPENAI_API_KEY}"
API_KEY="***REMOVED***"
MODEL="gpt-4"
ENDPOINT="https://api.openai.com/v1/chat/completions"

if [[ -z "$API_KEY" ]]; then
	echo "❌ Error: OPENAI_API_KEY is not set in environment."
	echo "Set it with: export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx"
	exit 1
fi

RESPONSE=$(curl -sS -X POST "$ENDPOINT" \
	-H "Authorization: Bearer $API_KEY" \
	-H "Content-Type: application/json" \
	-d '{
    "model": "'"$MODEL"'",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Say hello in one sentence."}
    ],
    "temperature": 0.3,
    "max_tokens": 50
  }')

if echo "$RESPONSE" | grep -q '"choices"'; then
	echo "✅ API key is valid. Response:"
	echo "$RESPONSE" | jq -r '.choices[0].message.content'
else
	echo "❌ API call failed. Full response:"
	echo "$RESPONSE"
fi
