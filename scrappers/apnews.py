from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils.constants import header, apnews_url


def fetch_apnews_articles():
    # Headers to mimic a browser request
    headers = {
        "User-Agent": header
    }

    # List to store articles
    articles_data = []

    # Create a session
    session = requests.Session()
    session.headers.update(headers)

    # Send a GET request
    response = session.get(apnews_url)

    # Check response status
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Error: Unable to retrieve page.")
        print(response.text[:1000])  # Print first 1000 characters for debugging
    else:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # ---- Extract main news articles ----
        articles = soup.find_all('div', class_='PagePromo')  # Updated class to match the provided HTML

        for article in articles:
            # Extract title
            title_tag = article.find('h3', class_='PagePromo-title')
            title = title_tag.text.strip() if title_tag else None

            # Extract article URL
            link_tag = title_tag.find('a')
            article_url = urljoin(apnews_url, link_tag['href']) if link_tag and link_tag.has_attr(
                'href') else None
            if not title or article_url: continue

            # Extract description
            description_tag = article.find('div', class_='PagePromo-description')
            description = description_tag.text.strip() if description_tag else 'No description found'

            # Extract image URL
            img_tag = article.find('img')
            url_to_image = urljoin(apnews_url, img_tag['src']) if img_tag and img_tag.has_attr(
                'src') else None

            # Try to extract published date
            published_at_tag = article.find('time')  # Look for a <time> element
            published_at = published_at_tag.text.strip() if published_at_tag else None
            if not published_at: continue

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "source": {
                    "name": "AP News",
                    "imageUrl": "https://assets.apnews.com/fa/ba/9258a7114f5ba5c7202aaa1bdd66/aplogo.svg"
                }
            })

    print(f"Scrapped {len(articles_data)} articles from AP News.")
    return articles_data
