#!/bin/bash

aws stepfunctions start-execution \
	--profile $1 \
	--region $2 \
	--state-machine-arn $3 \
	--input $4

