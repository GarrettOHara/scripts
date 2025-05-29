#!/bin/bash

# Define AWS profile
PROFILE="bi"

# Define ARN fragment to search for
ARN_FRAGMENT="3ZEAUNL6B5QSPWYUNB5G6YCAF4"

# List all DMS replication instances and filter for the ARN fragment
aws dms describe-replication-instances --profile "$PROFILE" --query "ReplicationInstances[*].{Name:ReplicationInstanceIdentifier, ARN:ReplicationInstanceArn}" --output json | \
  jq -r --arg fragment "$ARN_FRAGMENT" '.[] | select(.ARN | contains($fragment)) | "\(.Name) \(.ARN)"'
