import argparse
import boto3
import os


def delete_db_snapshot(snapshot_identifier, region):
    session = boto3.Session(region_name=region)
    client = session.client("rds")

    response = client.delete_db_snapshot(DBSnapshotIdentifier=snapshot_identifier)
    print("Snapshot deleted successfully.")


def get_snapshot_status(snapshot_identifier, region):
    session = boto3.Session(region_name=region)
    client = session.client("rds")

    response = client.describe_db_snapshots(DBSnapshotIdentifier=snapshot_identifier)
    snapshot_status = response["DBSnapshots"][0]["Status"]

    print(f"Snapshot status: {snapshot_status}")


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Delete and check status of a DB snapshot")
parser.add_argument(
    "snapshot_identifier", type=str, help="Identifier of the DB snapshot"
)
parser.add_argument("--region", type=str, help="AWS region name")

args = parser.parse_args()

# Retrieve AWS profile from environment variable
profile = os.environ.get("AWS_PROFILE")

# Delete the snapshot
delete_db_snapshot(args.snapshot_identifier, args.region)

# Check the status of the snapshot
get_snapshot_status(args.snapshot_identifier, args.region)
