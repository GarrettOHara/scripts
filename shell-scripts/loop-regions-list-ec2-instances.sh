#!/bin/bash

INSTANCE_ID=$1

for region in $(aws ec2 describe-regions --query "Regions[].RegionName" --output text); do
    echo "Searching in region: $region"
    aws ec2 describe-instances --instance-ids $INSTANCE_ID --region $region
done

