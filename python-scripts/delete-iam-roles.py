#!/opt/homebrew/bin/python3
import boto3
import sys

def delete_iam_roles_with_string(profile_name, string, aws_account_id):
    # Create a session using the specified profile
    session = boto3.Session(profile_name=profile_name)

    # Create an IAM client
    iam = session.client("iam")

    # List all IAM roles
    response = iam.list_roles()

    # Extract the roles
    roles = response["Roles"]

    # Filter roles with the specified string
    roles_to_delete = [
        role["RoleName"] for role in roles if string in role["RoleName"]
    ]

    if not roles_to_delete:
        print(f"No IAM roles contain '{string}'.")
        return

    print("The following IAM roles will be deleted:")
    for role_name in roles_to_delete:
        print(role_name)

    # Ask for confirmation
    confirmation = input(
        "Are you sure you want to delete these IAM roles? (Type 'yes' or 'no'): "
    )
    if confirmation.lower() in ["y", "yes"]:
        # Delete each role
        deleted_roles = 0
        for role_name in roles_to_delete:
            try:
                iam.delete_role(
                    RoleName=role_name
                )
                deleted_roles += 1
                print(f"Deleted IAM role: {role_name}")
            except iam.exceptions.NoSuchEntityException as e:
                print(f"Error deleting role {role_name}: {e}")
                continue
            except iam.exceptions.DeleteConflictException as e:
                print(f"Error deleting role {role_name}: {e}")
                continue

        print(
            f"Deleted {deleted_roles} out of "
            + f"{len(roles_to_delete)} IAM roles with string '{string}'."
        )
    else:
        print("Deletion cancelled.")


def main():
    # Check if the number of arguments is correct
    if len(sys.argv) != 4:
        print("Please pass in <AWS_PROFILE> and <ROLE_CONTAINING_STRING> and <AWS_ACCOUNT_ID>")
        sys.exit(1)

    profile_name = sys.argv[1]
    string_to_search = sys.argv[2]
    aws_account_id = sys.argv[3]

    # Call the function to delete roles
    delete_iam_roles_with_string(profile_name, string_to_search, aws_account_id)


if __name__ == "__main__":
    main()

