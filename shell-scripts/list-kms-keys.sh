#!/bin/bash
echo "Make sure to pass KMS key ID as argument"

key_id_to_search=$1

regions=$(aws ec2 describe-regions --output json | jq -r '.Regions[].RegionName')

for region in $regions; do
    echo "Searching in region: $region"
    
    result=$(aws kms list-keys --region $region --output json | jq -r --arg key_id "$key_id_to_search" '.Keys[] | select(.KeyId == $key_id)')
    
    if [ ! -z "$result" ]; then
        echo "Key found in region $region: $result"
    else
        echo "Key not found in region $region"
    fi
done

