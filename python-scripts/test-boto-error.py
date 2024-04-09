import boto3
import json
import os
import sys
from botocore.exceptions import ClientError
from mypy_boto3_rds.client import RDSClient

PROFILE = os.environ["AWS_PROFILE"]
REGION = sys.argv[1]
SNAPSHOT = sys.argv[2]

# INSTANCE_ID = sys.argv[2]

# try:
#     boto_session = boto3.Session(profile_name=PROFILE)
#     rds_client: RDSClient = boto_session.client('rds', region_name=REGION)
#
#     # Describe and print DB snapshots for the specified RDS instance
#     response = rds_client.describe_db_snapshots(
#         DBInstanceIdentifier=INSTANCE_ID
#     )
#     snapshots = response.get('DBSnapshots', [])
#     if snapshots:
#         print(f"DB Snapshots for instance {INSTANCE_ID}:")
#         for snapshot in snapshots:
#             print(f"Snapshot Identifier: {snapshot['DBSnapshotIdentifier']}")
#             print(f"Snapshot Status: {snapshot['Status']}")
#             print("---")
#     else:
#         print(f"No DB snapshots found for instance {INSTANCE_ID}")

# Specify the snapshot identifier you want to delete
snapshot_identifier_to_delete = "your_snapshot_identifier"

# Delete the specified RDS snapshot with exception handling
try:
    boto_session = boto3.Session(profile_name=PROFILE)
    rds_client: RDSClient = boto_session.client("rds", region_name=REGION)
    response = rds_client.delete_db_snapshot(
        DBSnapshotIdentifier=snapshot_identifier_to_delete
    )
    print(
        f"Snapshot {snapshot_identifier_to_delete} "
        + f"deletion initiated. Response: {response}"
    )

except ClientError as error:
    # Check if the error is due to the snapshot not being found
    if error.response["Error"]["Code"] == "DBSnapshotNotFoundFault":
        print(f"Snapshot {snapshot_identifier_to_delete} not found.")
    else:
        # Handle other exceptions
        print(json.dumps(error.response, default=str))

except ClientError as error:
    print(json.dumps(error.response, default=str))
