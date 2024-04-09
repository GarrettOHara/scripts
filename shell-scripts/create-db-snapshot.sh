#!/bin/zsh

aws rds create-db-snapshot \
	--profile $1 \
	--region $2 \
	--db-snapshot-identifier $3 \
	--db-instance-identifier $4
