#!/bin/zsh

aws rds describe-db-snapshots \
	--profile $1 \
	--region $2
