#!/bin/bash
aws ssm send-command \
	--profile $1 \
	--region $2 \
	--document-name "AWS-RunShellScript" \
	--parameters "commands=['$3']" \
	--targets "Key=instanceids,Values=$4"
