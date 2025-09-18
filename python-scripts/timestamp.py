import datetime

# Get current time and calculate date 7 days ago
utc_now = datetime.datetime.now(datetime.timezone.utc)
seven_days_ago = utc_now - datetime.timedelta(days=7)

print(f"UTC Now: {utc_now.isoformat()}")
print(f"7 days ago: {seven_days_ago.isoformat()}")

print(f"UTC Now Timestamp: \t{int(utc_now.timestamp())}")
print(f"7 days ago: \t\t{int(seven_days_ago.timestamp())}")

