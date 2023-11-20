#!/bin/zsh

aws events put-rule \
	--profile se-dev \
	--region us-east-1 \
	--name "TestEventBridgeSchedule" \
	--schedule-expression "cron(0 4 ? * * * | ? * WED *)" \
	--state "ENABLED" \
	--description "Testing schedule expressions"

