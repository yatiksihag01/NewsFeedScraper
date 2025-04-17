import xml.etree.ElementTree as ET

import requests
from dateutil import parser as dateparser


def fetch_ndtvnews_articles(rss_url: str, is_trending=False):
    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        channel = root.find("channel")
        items = channel.findall("item")

        articles = []

        for item in items:
            title = item.findtext("title", default="").strip()
            link = item.findtext("link", default="").strip()

            pub_date_raw = item.findtext("pubDate", default="").strip()
            pub_date = dateparser.parse(pub_date_raw).isoformat() if pub_date_raw else None

            description = item.findtext("description", default="").strip()
            content_encoded = item.findtext("{http://purl.org/rss/1.0/modules/content/}encoded", default="").strip()
            content = content_encoded if content_encoded else description

            media_content = item.find("{http://search.yahoo.com/mrss/}content")
            image_url = media_content.attrib.get("url") if media_content is not None else None

            articles.append({
                "title": title,
                "url": link,
                "description": description,
                "urlToImage": image_url,
                "publishedAt": pub_date,
                "source": {
                    "name": "NDTV",
                    "imageUrl": "https://www.ndtv.com/common/header/images/ndtv_logo_black.gif"
                },
                "is_trending": is_trending
            })

        return articles

    except Exception as e:
        print(f"[NDTV] Error fetching/parsing RSS: {e}")
        return []
