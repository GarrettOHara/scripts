import json
import boto3
import traceback

def lambda_handler(event, context):
    """
    Ping EC2 instance, start instance if powered down.
    
    Leveraging the Boto3 package, create a client to query the status of a
    given EC2 instance by ARN id passed in the Lambda event body.
    
    Parameters
    ----------
    event: dict
        Represents the event or trigger that caused the invocation
        of the lambda.
    context: dict
        Provides information about the invocation, function, 
        and execution environment of the Lambda.
    
    Returns
    -------
    dict
        statusCode: The state of the EC2 instance.
        body: Message describing EC2 instance state.
    """
    
    # Instantiate Boto3 EC2 client to access EC2 instances
    client = boto3.client("ec2", region_name="us-east-1")
    
    # Parse event meta data for EC2 ARN id
    instance_id = event["ec2_instance_id"]
    
    # Use boto3 client to query EC2 status
    instance = client.describe_instance_status(InstanceIds=[instance_id])

    # Print response fro logging
    print(json.dumps(instance, sort_keys=False, indent=2))

    # If there is no instance status, the instance is powered off, boot it on!
    if len(instance["InstanceStatuses"]) == 0:
        client.start_instances(InstanceIds=[instance_id])
        msg = "EC2 Instance is booting up."
        print(msg)
        return {
            "ec2_instance_id": instance_id,
            "response": "pending",
            "statusCode": 200,
            "body": msg
        }

    instance_status = instance["InstanceStatuses"][0]["InstanceState"]["Name"]
    
    if instance_status == "running":
        msg = "EC2 Instance available."
        print(msg)
        return {
            "ec2_instance_id": instance_id,
            "response": "running",
            "statusCode": 200,
            "body": msg
        }        

    else:
        print(traceback.format_exc())
        raise Exception("ERROR: Program state undefined")
