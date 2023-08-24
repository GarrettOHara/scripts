#!/opt/homebrew/bin/python3

import boto3
import sys

print("Usage: <PROFILE> <REGION>")

client = boto3.Session(profile_name=sys.argv[1], region_name=sys.argv[2]).client("rds")
rds_instances = client.describe_db_instances()

for instance in rds_instances["DBInstances"]:
    if "terratest" in instance["DBInstanceIdentifier"]:
        res = input(f"Do you want to delete {instance['DBInstanceIdentifier']} [y or N]?: ")
        if "y" in res.lower():
            client.delete_db_instance(
                DBInstanceIdentifier=instance["DBInstanceIdentifier"],
                SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True,
            )
        print(instance)
        print(f"{instance['DBInstanceIdentifier']} is deleting...\n")
