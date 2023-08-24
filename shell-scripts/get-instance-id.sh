#!/bin/bash

aws ec2 describe-instances \
	--region us-east-1 \
	--profile se-dev \
	--filters "Name=tag:Name,Values=terratestdbreload-bastion" \
	--query Reservations[0].Instances[0].InstanceId --output text | tr -d '[:space:]'

