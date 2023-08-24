#!/bin/bash
OUTPUT = 'aws ssm send-command \
    --document-name "AWS-RunShellScript" \
    --parameters "commands=[$1]" \
    --targets "Key=instanceids,Values=$2" \
	--query "CommandId" \
	--output text'

sleep(3)
echo $OUTPUT

# aws ssm get-command-invocation \
# 	--command-id $1 \
# 	--instance-id $2
