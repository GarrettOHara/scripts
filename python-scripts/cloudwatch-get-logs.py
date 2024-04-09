import boto3
import json

# AWS profile and region
aws_profile = "se-ops"
aws_region = "us-east-1"

# Log group and stream information
log_group_name = "/aws/lambda/se-ops-db-reloads-lambda"
log_stream_name = "2024/01/10/[$LATEST]312d5f1c71e94bb187ee98b757700c60"

# Create a CloudWatch Logs client
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
client = session.client("logs")


# Get the log events from the specified log stream
response = client.get_log_events(
    logGroupName=log_group_name,
    logStreamName=log_stream_name,
    limit=50,  # Adjust the limit based on your needs
    startFromHead=True,
)

# Extract and save log messages to a JSON file
log_events = response.get("events", [])

if log_events:
    # Create a list to store log messages
    log_messages = []

    # Extract and append log messages to the list
    for event in log_events:
        log_messages.append(event["message"])

    # Save log messages to a JSON file
    json_filename = "cloudwatch_logs.json"
    with open(json_filename, "w") as json_file:
        json.dump(log_messages, json_file, indent=2)

    print(f"Log messages saved to {json_filename}")
else:
    print("No log events found in the specified log stream.")
