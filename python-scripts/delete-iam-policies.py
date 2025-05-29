#!/opt/homebrew/bin/python3
import boto3
import sys


def delete_iam_policies_with_string(profile_name, string, aws_account_id):
    # Create a session using the specified profile
    session = boto3.Session(profile_name=profile_name)

    # Create an IAM client
    iam = session.client("iam")

    # List all IAM policies
    response = iam.list_policies(Scope="Local")
    iam_client = boto3.client("iam")

    # Extract the policies
    policies = response["Policies"]

    # Filter policies with the specified string
    policies_to_delete = [
        policy["PolicyName"] for policy in policies if string in policy["PolicyName"]
    ]

    if not policies_to_delete:
        print(f"No IAM policies contain '{string}'.")
        return

    print("The following IAM policies will be deleted:")
    for policy_name in policies_to_delete:
        print(policy_name)

    # Ask for confirmation
    confirmation = input(
        "Are you sure you want to delete these IAM policies? (Type 'yes' or 'no'): "
    )
    if confirmation.lower() in ["y", "yes"]:
        # Delete each policy
        deleted_policies = 0
        for policy_name in policies_to_delete:
            try:
                iam_client.delete_policy(
                    PolicyArn=f"arn:aws:iam::{aws_account_id}:policy/{policy_name}"
                )
                deleted_policies += 1
                print(f"Deleted IAM policy: {policy_name}")
            except iam_client.exceptions.NoSuchEntityException as e:
                print(f"Error deleting policy {policy_name}: {e}")
                continue
            except iam_client.exceptions.DeleteConflictException as e:
                print(f"Error deleting policy {policy_name}: {e}")
                continue

        print(
            f"Deleted {deleted_policies} out of "
            + f"{len(policies_to_delete)} IAM policies with string '{string}'."
        )
    else:
        print("Deletion cancelled.")


def main():
    # Check if the number of arguments is correct
    if len(sys.argv) != 4:
        print("UPlease pass in <AWS_PROFILE> and <POLICY_CONTAINING_STRING> and <AWS_ACCOUNT_ID>")
        sys.exit(1)

    profile_name = sys.argv[1]
    string_to_search = sys.argv[2]
    aws_account_id = sys.argv[3]

    # Call the function to delete policies
    delete_iam_policies_with_string(profile_name, string_to_search, aws_account_id)


if __name__ == "__main__":
    main()
