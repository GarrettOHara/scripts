import boto3
from datetime import datetime

# Initialize a session using Amazon IAM
session = boto3.Session()

# Initialize IAM client
iam_client = session.client('iam')

# Function to get last used time of an access key
def get_last_used_access_key(username):
    keys = iam_client.list_access_keys(UserName=username)['AccessKeyMetadata']
    for key in keys:
        key_id = key['AccessKeyId']
        last_used_info = iam_client.get_access_key_last_used(AccessKeyId=key_id)
        last_used_date = last_used_info.get('AccessKeyLastUsed', {}).get('LastUsedDate')
        if last_used_date:
            print(f"User: {username}, Access Key: {key_id}, Last Used: {last_used_date}")
        else:
            print(f"User: {username}, Access Key: {key_id}, Last Used: Never")

# List all users
users = iam_client.list_users()['Users']

# Get last used date for each user's access keys
for user in users:
    username = user['UserName']
    get_last_used_access_key(username)
