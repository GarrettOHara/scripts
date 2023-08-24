#!/opt/homebrew/bin/python3
import boto3
from botocore.exceptions import NoSuchEntityException

def delete_iam_policies_with_prefix(prefix):
    iam_client = boto3.client('iam')

    # List all IAM policies
    response = iam_client.list_policies()
    policies = response['Policies']

    # Filter policies with the specified prefix
    policies_to_delete = [policy['PolicyName'] for policy in policies if policy['PolicyName'].startswith(prefix)]

    if not policies_to_delete:
        print(f"No IAM policies found with prefix '{prefix}'.")
        return

    print("The following IAM policies will be deleted:")
    for policy_name in policies_to_delete:
        print(policy_name)

    # Ask for confirmation
    confirmation = input("Are you sure you want to delete these IAM policies? (Type 'yes' or 'no'): ")
    if confirmation.lower() in ['y', 'yes']:
        # Delete each policy
        deleted_policies = 0
        for policy_name in policies_to_delete:
            try:
                iam_client.delete_policy(PolicyArn=f"arn:aws:iam::aws:policy/{policy_name}")
                deleted_policies += 1
                print(f"Deleted IAM policy: {policy_name}")
            except NoSuchEntityException:
                print(f"IAM policy not found: {policy_name}")
        
        print(f"Deleted {deleted_policies} out of {len(policies_to_delete)} IAM policies with prefix '{prefix}'.")
    else:
        print("Deletion cancelled.")

# Usage
delete_iam_policies_with_prefix("terratest")

