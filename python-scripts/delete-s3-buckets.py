import os
import boto3

def delete_s3_buckets(profile_name, prefix):
    # Set AWS profile based on the provided environment variable
    os.environ['AWS_PROFILE'] = profile_name

    # Create an S3 client using the configured profile
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client('s3')

    # Retrieve the list of S3 buckets
    response = s3_client.list_buckets()

    if 'Buckets' in response:
        buckets = response['Buckets']

        if len(buckets) > 0:
            print(f"Deleting {len(buckets)} bucket(s) with prefix '{prefix}':")
            for bucket in buckets:
                bucket_name = bucket['Name']
                if bucket_name.startswith(prefix):
                    print(f"Bucket: {bucket_name}")
                    choice = input("Do you want to delete this bucket? [Y or N]: ")
                    if choice.lower() == 'y':
                        # List objects in the bucket
                        objects = s3_client.list_objects_v2(Bucket=bucket_name)['Contents']
                        if objects:
                            # Delete each object in the bucket
                            for obj in objects:
                                obj_key = obj['Key']
                                print(f"Deleting object: s3://{bucket_name}/{obj_key}")
                                s3_client.delete_object(Bucket=bucket_name, Key=obj_key)

                        # Delete the bucket
                        print(f"Deleting bucket: {bucket_name}")
                        s3_client.delete_bucket(Bucket=bucket_name)
                    else:
                        print(f"Skipping deletion of bucket: {bucket_name}")
                print()
        else:
            print("No S3 buckets found.")
    else:
        print("Failed to retrieve S3 bucket list.")

# Specify the AWS profile and bucket prefix using environment variables
aws_profile = os.environ.get('AWS_PROFILE')
bucket_prefix = 'terratest-'  # Update with your desired prefix

# Ensure the AWS profile is provided
if aws_profile:
    delete_s3_buckets(aws_profile, bucket_prefix)
else:
    print("Please set the AWS_PROFILE environment variable.")

