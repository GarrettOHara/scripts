import googleapiclient.discovery
from datetime import datetime

# Set your API key
api_key = "YOUR_API_KEY"

# Create a YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

# Set the search parameters
query = "Modern Warfare 2 gameplay"
published_after = datetime(2009, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")
published_before = datetime(2016, 1, 1).strftime("%Y-%m-%dT%H:%M:%SZ")

# Make the API request
search_response = (
    youtube.search()
    .list(
        q=query,
        type="video",
        part="id",
        publishedAfter=published_after,
        publishedBefore=published_before,
    )
    .execute()
)

# Extract video IDs from the search results
video_ids = [item["id"]["videoId"] for item in search_response["items"]]

# Print the video IDs
print("Video IDs:", video_ids)
