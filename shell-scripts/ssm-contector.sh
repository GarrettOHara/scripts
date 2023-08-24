#!/bin/zsh

echo "use script with arguments <REGION> <PROFILE> <INSTANCE ID>..."

aws ssm start-session \
	--region  $1 \
	--profile $2 \
	--target  $3 \
	--parameters command="bash -l" \
	--document-name AWS-StartInteractiveCommand

