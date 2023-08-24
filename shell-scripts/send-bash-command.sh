#!/bin/bash
aws ssm send-command \
    --document-name "AWS-RunShellScript" \
    --parameters "commands=[$1]" \
    --targets "Key=instanceids,Values=$2" \
	--profile $3 \
	--region $4

