#!/bin/bash

AWS_PROFILE="se-dev"

# List all IAM policies
policy_list=$(aws iam list-policies --profile $AWS_PROFILE --output json | jq -r '.Policies[] | select(.PolicyName | contains("terratest")) | .PolicyName')

# Loop through the list and prompt the user before deleting each policy
for policy_name in $policy_list; do
    read -p "Do you want to delete IAM policy $policy_name? [y/n]: " choice
    case "$choice" in
        y|Y )
            echo "Deleting IAM policy: $policy_name"
            aws iam delete-policy --policy-arn "arn:aws:iam::$(aws sts get-caller-identity --profile $AWS_PROFILE --output json | jq -r '.Account'):policy/$policy_name" --profile $AWS_PROFILE
            ;;
        n|N )
            echo "Skipped deletion of IAM policy: $policy_name"
            ;;
        * )
            echo "Invalid choice. Skipping deletion of IAM policy: $policy_name"
            ;;
    esac
done

