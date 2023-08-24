#!/bin/zsh
aws ssm get-parameter \
	--region  $1 \
	--profile $2 \
	--name    $3  \
	--with-decryption \
	--query 'Parameter.Value'
