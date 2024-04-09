#!/opt/homebrew/bin/python3
import boto3
import json
import sys

from mypy_boto3_rds.client import RDSClient

PROFILE = sys.argv[1]
REGION = sys.argv[2]
INSTANCE_ID = sys.argv[3]

session = boto3.session.Session(profile_name=PROFILE, region_name=REGION)
client: RDSClient = session.client("rds")

response = client.describe_db_instances(DBInstanceIdentifier=INSTANCE_ID)
print(json.dumps(response["DBInstances"][0], default=str, indent=4))
print(
    f'Extracting PendingModifiedValues: {response["DBInstances"][0]["PendingModifiedValues"]}'
)
if len(response["DBInstances"][0]["PendingModifiedValues"]) > 0:
    print("pending")
    print(response["DBInstances"][0]["PendingModifiedValues"])
else:
    print("nothing is pending")
