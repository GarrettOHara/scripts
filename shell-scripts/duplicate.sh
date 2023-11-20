#!/bin/zsh

# THIS DOES WORK
aws events put-rule \
	--profile se-dev \
	--region us-east-1 \
	--name "TestEventBridgeSchedule" \
	--schedule-expression "cron(0 20 * * ? *)"
	--state "ENABLED" \
	--description "Testing schedule expressions"

# THIS ONE DOESN'T WORK
aws events put-rule \
  --profile se-dev \
  --region us-east-1 \
  --name "TestEventBridgeSchedule" \
  --schedule-expression "cron(0 4 ? * * * | ? * WED *)" \
  --state "ENABLED" \
  --description "Testing schedule expressions"

# THIS ONE DOESN'T WORK
aws events put-rule \
  --profile se-dev \
  --region us-east-1 \
  --name "TestEventBridgeSchedule" \
  --schedule-expression "cron(0 0 1-7,15-21 ? * WED *)" \
  --state "ENABLED" \
  --description "Testing schedule expressions"

