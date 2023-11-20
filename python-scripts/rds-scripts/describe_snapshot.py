#!/opt/homebrew/bin/python3
import boto3
import json
import sys


def rds_client(profile, region):
    session = boto3.session.Session(
        profile_name=profile,
        region_name=region,
    )
    return session.client("rds")


if __name__ == "__main__":
    # extract snapshot name from command line
    snapshot_name = str(sys.argv[1])

    # snapshot attributes does not show KMS key. do not use
    # response = rds_client().describe_db_snapshot_attributes(
    #     DBSnapshotIdentifier="se-financial-reports-20231116"
    # )
    try:
        kms_key_id = ""
        response = rds_client("se-staging", "us-east-1").describe_db_snapshots(
            DBSnapshotIdentifier=snapshot_name
        )["DBSnapshots"][0]
        kms_key_id = response["KmsKeyId"]
        snapshot_arn = response["DBSnapshotArn"]
        print(
            "Describing RDS Snapshot: \n" + json.dumps(response, indent=4, default=str)
        )
        print("Extracting KMS Key ID: " + kms_key_id)

    except KeyError as error:
        if "KmsKeyId" in error.args[0]:
            print("The snapshot is not encrypted with a KMS key")
        else:
            print(error)

    print("Copying snapshot into target account")
    if kms_key_id == "":
        response = rds_client("se-dev", "us-east-1").copy_db_snapshot(
            SourceDBSnapshotIdentifier=snapshot_arn,
            TargetDBSnapshotIdentifier=snapshot_arn + "-copy",
        )
    else:
        response = rds_client("se-dev", "us-east-1").copy_db_snapshot(
            SourceDBSnapshotIdentifier=snapshot_arn,
            TargetDBSnapshotIdentifier="test-snapshot-copy",
            KmsKeyId=kms_key_id,
        )
