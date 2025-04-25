import xml.etree.ElementTree as ET

import requests

from utils.constants import header
from utils.utils import get_source_logo


def fetch_yahoonews_articles(rss_url, is_trending=False):
    # Fetch the RSS feed
    headers = {
        "User-Agent": header,
    }
    try:
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch RSS feed: {e}")
        return []

    root = ET.fromstring(response.content)
    channel = root.find('channel')

    articles_data = []

    for item in channel.findall('item'):
        title = item.findtext("title").strip()
        article_url = item.findtext("link").strip()
        pub_date = item.findtext("pubDate").strip()
        source_name = item.findtext("source").strip()
        media = item.find("{http://search.yahoo.com/mrss/}content")
        media_url = media.attrib['url'] if media is not None and 'url' in media.attrib else None

        articles_data.append({
            "title": title,
            "url": article_url,
            "description": None,
            "urlToImage": media_url,
            "publishedAt": pub_date,
            "source": {
                "name": source_name,
                "imageUrl": get_source_logo(source_name)
            },
            "is_trending": is_trending
        })

    print(f"Scrapped {len(articles_data)} articles from Yahoo News.")
    return articles_data
