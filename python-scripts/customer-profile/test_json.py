import json

json_string = """
{
        "conversation_profile": "This is a short summary of customer-XYZ's preferences and how to personalize recommendations for customer-XYZ.",
        "conversation_genres": [
            "genre1",
            "genre2"
        ],
        "conversation_preference": "This is a short summary of customer-XYZ's preferences and how to personalize recommendations for customer-XYZ."
}
"""
data_list = json.loads(json_string)
print(json.dumps(data_list, indent=2))
print(f"profile: {data_list['conversation_profile']}")
