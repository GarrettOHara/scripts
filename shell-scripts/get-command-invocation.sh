#/bin/bash

aws ssm get-command-invocation \
	--profile $1 \
	--region $2 \
	--instance-id $3 \
	--command-id $4

