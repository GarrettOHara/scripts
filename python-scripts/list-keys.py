import boto3

# Replace this with the access key ID you are searching for
search_key_id = input("Key ID to search: ")

# Initialize an IAM client
iam_client = boto3.client('iam')

def find_access_key(search_key_id):
    # List all IAM users
    users = iam_client.list_users()['Users']
    
    # Iterate through each user
    for user in users:
        user_name = user['UserName']
        
        # List all access keys for the current user
        access_keys = iam_client.list_access_keys(UserName=user_name)['AccessKeyMetadata']
        
        # Check if the access key ID matches the one you're looking for
        for key in access_keys:
            if key['AccessKeyId'] == search_key_id:
                print(f"Access Key ID '{search_key_id}' found for user: {user_name}")
                return

    print(f"Access Key ID '{search_key_id}' not found in any users.")

# Run the search function
find_access_key(search_key_id)

