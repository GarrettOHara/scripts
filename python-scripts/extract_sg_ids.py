#! /opt/homebrew/bin/python3

import boto3

boto_session = boto3.Session(profile_name="se-dev", region_name="us-east-1")
rds_client = boto_session.client("rds")


def describe_db(instance_name: str):
    return rds_client.describe_db_instances(DBInstanceIdentifier=instance_name)


res = describe_db("terratestdbreloadpostgresprod")
json_objects = res["DBInstances"][0]

security_groups = [d["VpcSecurityGroupId"] for d in json_objects["VpcSecurityGroups"]]
print(security_groups)

parameter_groups = [
    d["DBParameterGroupName"] for d in json_objects["DBParameterGroups"]
]
print(parameter_groups)

tags = json_objects["TagList"]


def test(tags: dict):
    print(tags)


test(tags)
