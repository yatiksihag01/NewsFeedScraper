import xml.etree.ElementTree as ET

import requests


def fetch_bbc_news_rss(bbc_rss_url, trending=False):
    try:
        response = requests.get(bbc_rss_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch RSS feed: {e}")
        return []

    # Parse XML
    root = ET.fromstring(response.content)
    channel = root.find("channel")

    articles_data = []

    for item in channel.findall("item"):
        title = item.findtext("title").strip()
        description = item.findtext("description", default="No Description").strip()
        url = item.findtext("link").strip()
        pub_date = item.findtext("pubDate").strip()
        if not title or not pub_date or not url: continue

        # Use media namespace for thumbnail
        media = "{http://search.yahoo.com/mrss/}"
        thumbnail = item.find(f"{media}thumbnail")
        image_url = thumbnail.attrib["url"]
        if not image_url: continue

        articles_data.append({
            "title": title,
            "url": url,
            "description": description,
            "urlToImage": image_url,
            "publishedAt": pub_date,
            "source": {
                "name": "BBC News",
                "imageUrl": "https://news.bbcimg.co.uk/nol/shared/img/bbc_news_120x60.gif"
            },
            "is_trending": trending
        })

    print(f"Fetched {len(articles_data)} articles from BBC RSS feed.")
    return articles_data
