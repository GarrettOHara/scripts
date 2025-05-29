import feedparser
import requests
from bs4 import BeautifulSoup

def get_ft_articles_from_rss():
    """
    Get article URLs from FT RSS feeds (these are usually accessible)
    Then attempt to access full articles
    """

    rss_feeds = [
        'https://www.ft.com/rss/home/uk',
        'https://www.ft.com/rss/companies',
        'https://www.ft.com/rss/world'
    ]

    articles = []

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary
            })

    return articles

# Get article URLs from RSS, then try to access full content
rss_articles = get_ft_articles_from_rss()
for article in rss_articles[:5]:  # Test first 5
    print(f"Title: {article['title']}")
    print(f"URL: {article['link']}")
