#!/bin/bash

aws opsworks describe-apps \
	--region $1 \
	--profile $2 \
	--stack-id $3 \
	--query Apps[0].SslConfiguration.PrivateKey \
	--output text

