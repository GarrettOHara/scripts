#!/bin/zsh

echo "Please pass in parameters to script in this order: ./describe_rds.sh <REGION> <PROFILE> <INSTANCE_NAME>"

aws rds describe-db-instances \
	--region  $1 \
	--profile $2
