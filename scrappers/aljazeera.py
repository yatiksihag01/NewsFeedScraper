from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils.constants import aljazeera_url, header


def fetch_aljazeera_articles():
    # Fixing the User-Agent header
    headers = {
        "User-Agent": header
    }

    # List to store articles
    articles_data = []

    # Create a session to handle requests
    session = requests.Session()
    session.headers.update(headers)

    # Send a GET request
    response = session.get(aljazeera_url)

    # Check response status
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Error: Unable to retrieve page.")
        print(response.text[:1000])  # Print first 1000 characters for debugging
    else:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all articles (adjust the class names based on Al Jazeera's HTML structure)
        articles = soup.find_all('article')

        for article in articles:
            # Extract title
            title_tag = article.find('h3')
            title = title_tag.text.strip() if title_tag else 'No title found'

            # Extract article URL
            link_tag = article.find('a')
            article_url = urljoin(aljazeera_url, link_tag['href']) if link_tag and link_tag.has_attr(
                'href') else 'No URL found'

            # Extract description
            desc_tag = article.find('p')
            description = desc_tag.text.strip() if desc_tag else 'No description found'

            # Extract image URL
            img_tag = article.find('img')
            url_to_image = urljoin(aljazeera_url, img_tag['src']) if img_tag and img_tag.has_attr(
                'src') else 'No image found'

            # Extract published date
            date_tag = article.find('span', class_='screen-reader-text')
            published_at = date_tag.text.strip() if date_tag else 'No date found'

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "source": {
                    "name": "Al Jazeera",
                    "imageUrl": "https://www.aljazeera.com/favicon.ico"
                }
            })

    print(f"Scrapped {len(articles_data)} articles from Al Jazeera.")
    return articles_data
