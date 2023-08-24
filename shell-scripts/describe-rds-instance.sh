#!/bin/bash

aws rds describe-db-instances \
	--region $1 \
	--db-instance-identifier $2 \
	--query 'DBInstances[0].Endpoint.Address' \
	--output text
