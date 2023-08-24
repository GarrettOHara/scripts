#!/bin/bash

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install the AWS CLI and try again."
    exit 1
fi

# Check if required arguments are provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <aws_profile> <aws_region>"
    exit 1
fi

# Extract the arguments
aws_profile=$1
# aws_region=$2

# Set AWS profile and region for AWS CLI commands
export AWS_PROFILE=$aws_profile
# export AWS_DEFAULT_REGION=$aws_region

# Get the list of IAM policies starting with the prefix "terratest"
policy_names=$(aws iam list-policies --query "Policies[?starts_with(PolicyName, 'terratest')].PolicyName" --output text)

# Delete each IAM policy
for policy_name in $policy_names; do
    echo "Deleting IAM policy: $policy_name"
    aws iam delete-policy --policy-arn "arn:aws:iam::$aws_account_id:policy/$policy_name"
done

