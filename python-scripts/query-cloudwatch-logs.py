import boto3
import json

# AWS profile and region
aws_profile = "se-ops"
aws_region = "us-east-1"

# Log group and stream information
log_group_name = "/aws/lambda/se-ops-db-reloads-lambda"
log_stream_name = "2024/01/10/[$LATEST]312d5f1c71e94bb187ee98b757700c60"

# Create a boto3 session using the specified profile and region
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

# Create CloudWatch Logs client
logs_client = session.client("logs")

# Get log events
response = logs_client.get_log_events(
    logGroupName=log_group_name, logStreamName=log_stream_name
)

# Extract and format log messages
log_events = response.get("events", [])
formatted_logs = []

for event in log_events:
    # if 'message' in event and event['message'].strip():  # Check if 'message' is not empty
    #     try:
    #         formatted_logs.append(json.loads(event['message']))
    #     except json.JSONDecodeError as e:
    #         print(f"Error decoding JSON for event: {event}. Error: {e}")

    formatted_logs.append(event["message"])

# Save formatted logs to a JSON file
with open("logs.json", "w") as json_file:
    json.dump(formatted_logs, json_file, default=str, indent=2)
