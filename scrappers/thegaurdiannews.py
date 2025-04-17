import re
import xml.etree.ElementTree as ET

import requests

from utils.utils import is_trending


def strip_html_tags(text):
    return re.sub(r'<[^>]+>', '', text)


def fetch_guardian_rss_articles(rss_url):
    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch Guardian RSS feed from {rss_url}: {e}")
        return []

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"Failed to parse Guardian RSS XML: {e}")
        return []

    channel = root.find("channel")
    if channel is None:
        print("Invalid RSS feed: <channel> not found")
        return []

    articles = []
    media_ns = "{http://search.yahoo.com/mrss/}"
    dc_ns = "{http://purl.org/dc/elements/1.1/}"

    for item in channel.findall("item"):
        title = item.findtext("title", default="No Title").strip()
        description_raw = item.findtext("description", default="No Description")
        description = strip_html_tags(description_raw).strip()

        link = item.findtext("link", default="No URL").strip()
        pub_date = item.findtext("pubDate", default=None).strip()

        # Get the highest resolution media:content
        image_url = None
        for media in item.findall(f"{media_ns}content"):
            url = media.attrib.get("url")
            width = int(media.attrib.get("width", 0))
            if url and (image_url is None or width > 140):  # prefer larger image
                image_url = url

        if not image_url:
            image_url = "No image found"

        articles.append({
            "title": title,
            "url": link,
            "description": description,
            "urlToImage": image_url,
            "publishedAt": pub_date,
            "source": {
                "name": "The Guardian",
                "imageUrl": "https://assets.guim.co.uk/images/guardian-logo-rss.c45beb1bafa34b347ac333af2e6fe23f.png"
            },
            "is_trending": is_trending(pub_date)  # Assume trending if published recently
        })
    print(f"Fetched {len(articles)} articles from {rss_url}")
    return articles
