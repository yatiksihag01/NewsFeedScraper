from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils.constants import header, un_news_url


def fetch_un_news_articles():
    # Headers to mimic a real browser request
    headers = {
        "User-Agent": header
    }

    # List to store articles
    articles_data = []

    response = requests.get(un_news_url, headers=headers)

    # Check if request is successful
    if response.status_code != 200:
        print(f"Error: Unable to retrieve page. Status code: {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all article blocks
        articles = soup.find_all('article', class_='node--type-news-story')

        for article in articles:
            # Extract Title
            title_tag = article.find('h2', class_='node__title')
            title = title_tag.text.strip() if title_tag else None

            # Extract Article URL
            link_tag = title_tag.find('a') if title_tag else None
            article_url = urljoin(un_news_url, link_tag['href']) if link_tag else None

            # Extract Description
            description_tag = article.find('div', class_='field--name-field-news-story-lead')
            description = description_tag.text.strip() if description_tag else 'No description found'

            # Extract Image URL
            url_to_image = 'No image found'  # Default value

            image_container = article.find('div', class_='node__media')
            if image_container:
                picture_tag = image_container.find('picture')

                if picture_tag:
                    # Look for the best quality image in <source> tags
                    source_tags = picture_tag.find_all('source')
                    if source_tags:
                        url_to_image = urljoin(un_news_url, source_tags[-1]['srcset'].split(',')[0].strip().split(' ')[
                            0])  # Get the last <source>

                # If <picture> not found or no <source> images, try <img>
                if url_to_image == 'No image found':
                    img_tag = image_container.find('img')
                    if img_tag and 'src' in img_tag.attrs:
                        url_to_image = img_tag['src']

            # Extract Published Date (if available)
            time_tag = article.find('time')
            published_at = time_tag['datetime'].split('T')[0] if time_tag else None
            if not article_url or not title or not published_at: continue

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "source": {
                    "name": "United Nations",
                    "imageUrl": "https://news.un.org/en/themes/custom/un_base_theme/images/un-emblem-for-rss.png"
                }
            })

    print(f"Scrapped {len(articles_data)} articles from UN News.")
    return articles_data
