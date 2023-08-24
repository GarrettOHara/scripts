#!/bin/zsh

aws rds describe-db-instances \
	--profile $1 \
	--region  $2 \
	--db-instance-identifier $3 | jq


aws rds describe-db-instances \
	--profile $1 \
	--region  $2 \
	--db-instance-identifier $3 \
	--output text \
	--query "DBInstances[0].DBInstanceArn"

