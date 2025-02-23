import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_theguardian_articles():
    # The Guardian URL
    url = "https://www.theguardian.com/international"

    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # List to store articles
    articles_data = []

    # Create a session
    session = requests.Session()
    session.headers.update(headers)

    # Send a GET request
    response = session.get(url)

    # Check response status
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Error: Unable to retrieve page.")
        print(response.text[:1000])  # Print first 1000 characters for debugging
    else:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # ---- Extract articles from the new HTML structure ----
        new_articles = soup.find_all('div', class_='dcr-f9aim1')  # New articles

        for new_article in new_articles:
            try:
                # Extract title
                title_tag = new_article.find('a')
                title = title_tag['aria-label'].strip() if title_tag and title_tag.has_attr('aria-label') else 'No title found'

                # Extract article URL
                article_url = urljoin(url, title_tag['href']) if title_tag and title_tag.has_attr('href') else 'No URL found'

                # Extract description
                description = title  # Use title as description

                # Extract image URL
                img_tag = new_article.find('img')
                url_to_image = urljoin(url, img_tag['src']) if img_tag and img_tag.has_attr('src') else 'No image found'

                # Extract the published date from <time> tag
                time_tag = new_article.find('time')
                if time_tag and time_tag.has_attr('datetime'):
                    published_at = time_tag['datetime']  # Extract the datetime attribute (ISO format)
                else:
                    published_at = 'No date found'

                # Add article data to the list
                articles_data.append({
                    "title": title,
                    "url": article_url,
                    "description": description,
                    "urlToImage": url_to_image,
                    "publishedAt": published_at,
                    "sourceDto": {
                        "name": "The Guardian",
                        "imageUrl": "https://assets.guim.co.uk/images/guardian-logo-rss.c45beb1bafa34b347ac333af2e6fe23f.png"
                    }
                })

            except Exception as e:
                print(f"Error parsing new article: {e}")

    return articles_data
