#!/bin/bash

aws rds describe-db-instances \
	--region $1 \
	--profile $2 \
	--db-instance-identifier $3 \
	--query 'DBInstances[0].Endpoint.Address' \
	--output text

