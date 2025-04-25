from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils.constants import ny_times_url, header


def fetch_ny_times_articles():
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
    response = session.get(ny_times_url)

    # Check response status
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # List to store articles
        articles_data = []

        # Extract main news articles
        articles = soup.find_all('a', class_='css-9mylee')  # Adjust class if necessary

        for article in articles:
            # Extract title
            title_tag = article.find('p', class_='indicate-hover')
            title = title_tag.text.strip() if title_tag else None

            # Extract article URL
            article_url = urljoin(ny_times_url, article['href']) if article.has_attr('href') else None
            if not title or not article_url: continue

            # Extract description
            description_tag = article.find('p', class_='summary-class')
            description = description_tag.text.strip() if description_tag else None

            # Extract image URL
            url_to_image = 'No image found'
            figure_tag = article.find('figure', class_='css-hurk9l')  # Locate figure container

            if figure_tag:
                picture_tag = figure_tag.find('picture', class_='css-hdqqnp')  # Locate picture tag
                if picture_tag:
                    # Check for <source> tag with srcset attribute
                    source_tag = picture_tag.find('source')
                    if source_tag and source_tag.has_attr('srcset'):
                        srcset_images = source_tag['srcset'].split(',')  # srcset is comma-separated
                        highest_quality_image = srcset_images[-1].split(' ')[0]  # Get the last src (highest quality)
                        url_to_image = urljoin(ny_times_url, highest_quality_image)
                    # If no <source>, check for <img> tag
                    elif picture_tag.find('img'):
                        img_tag = picture_tag.find('img')
                        if img_tag and img_tag.has_attr('src'):
                            url_to_image = urljoin(ny_times_url, img_tag['src'])

            # Published date (not available in provided HTML)
            published_at = 'No date found'

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "source": {
                    "name": "New York Times",
                    "imageUrl": None
                }
            })

    else:
        print("Error: Unable to retrieve page.")
        print(response.text[:1000])  # Print first 1000 characters for debugging

    print(f"Scrapped {len(articles_data)} articles from NY Times.")
    return articles_data
