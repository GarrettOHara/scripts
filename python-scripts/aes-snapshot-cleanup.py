import re
import sys
import boto3
from datetime import datetime
from botocore.exceptions import ClientError


import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="botocore.client")


def instantiate_rds_client(profile, region):
    """
    Creates a boto3 Session object. Instantiates and returns a client
    to access that aws resource for the passed argument.

    Parameters
    ----------
    profile: string
        profile that corresponds to the credentials stored in ~/.aws/config
    region: string
        describes the region within the desired aws account.

    Raises
    ------
    ClientError
        raised when there is not an acceptable client object to be returned
        the reload step should be retried from the StepFunction Manager Level.

    Returns
    -------
    boto3.session.client(<CLIENT_TYPE>)
        boto3 client to the resource that was passed via client_type
    """
    try:
        boto_session = boto3.Session(profile_name=profile, region_name=region)
        boto_client = boto_session.client("rds")

    except ClientError as error:
        print(f"There was an error instantiating the boto3 client: {error}")
        raise error

    return boto_client


def describe_snapshots(client, retention_period=30, max=100):
    """
    Query RDS Manual Snapshots for a given environment, delete snapshots older than
    retention period (default is 30 days).

    Parameters
    ----------
    client: boto3.Session().client("rds")
        Client object instantiated from boto3 session.
    retention_period: int
        Lifecycle rule for snapshot lifetimes.
    max: int
        Number of snapshots to query per batch (max is 100).

    Returns
    -------
    none

    Sources
    -------
    Comparing times in python:
        - https://stackoverflow.com/questions/21378977/how-to-compare-two-timestamps-in-python
    Python Datetime strptime:
        - https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    """
    print("\nQuerying snapshots...\n")

    snaps_deleted = -1

    # iterate until to delete is 0
    while snaps_deleted != 0:
        try:
            response = client.describe_db_snapshots(
                SnapshotType="manual", MaxRecords=max
            )
        except client.exceptions.DBSnapshotNotFoundFault:
            print("There are no manual snapshots. Program exiting...")
            sys.exit(0)

        current_timestamp = datetime.now()
        current_timestamp = datetime.strptime(
            str(current_timestamp), "%Y-%m-%d %H:%M:%S.%f"
        )

        for snap in response["DBSnapshots"]:
            # transfer timestamps into python datetime objects to compare
            snapshot_timestamp = str(
                re.sub("\+(.*)", "", str(snap["SnapshotCreateTime"]))
            )
            snapshot_timestamp = datetime.strptime(
                snapshot_timestamp, "%Y-%m-%d %H:%M:%S.%f"
            )

            # extract time delta in days
            delta = (current_timestamp - snapshot_timestamp).days

            # if the snapshot is older than 30 days delete it
            if delta >= retention_period:
                print("DAYS: ", delta, "\tIDENTIFIER: ", snap["DBSnapshotIdentifier"])

                snaps_deleted += 1

                # TODO: remove snapshots with this after approval.
                # try:
                #     client.delete_db_snapshot(
                #         DBSnapshotIdentifier='snap["DBSnapshotIdentifier"]'
                #     )
                # except client.exceptions.DBSnapshotNotFoundFault:
                #     print(f"There was an error deleting {snap["DBSnapshotIdentifier"]}. Program continuing...")
                #     continue

        print(f"\nDELETED {snaps_deleted} SNAPSHOTS\n")

        # TODO: remove break statement, let snaps_deleted satisfy while loop condition.
        break


if __name__ == "__main__":
    client = instantiate_rds_client("aes-prod", "us-east-1")
    describe_snapshots(client)
