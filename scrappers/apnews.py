import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_apnews_articles():
    # AP News URL
    url = "https://apnews.com/world-news"

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

        # ---- Extract main news articles ----
        articles = soup.find_all('div', class_='PagePromo')  # Updated class to match provided HTML

        for article in articles:
            # Extract title
            title_tag = article.find('h3', class_='PagePromo-title')
            title = title_tag.text.strip() if title_tag else 'No title found'

            # Extract article URL
            link_tag = title_tag.find('a')
            article_url = urljoin(url, link_tag['href']) if link_tag and link_tag.has_attr('href') else 'No URL found'

            # Extract description
            description_tag = article.find('div', class_='PagePromo-description')
            description = description_tag.text.strip() if description_tag else 'No description found'

            # Extract image URL
            img_tag = article.find('img')
            url_to_image = urljoin(url, img_tag['src']) if img_tag and img_tag.has_attr('src') else 'No image found'

            # Try to extract published date
            published_at_tag = article.find('time')  # Look for a <time> element
            published_at = published_at_tag.text.strip() if published_at_tag else 'No date found'

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "sourceDto": {
                    "name": "AP News",
                    "imageUrl":"https://assets.apnews.com/fa/ba/9258a7114f5ba5c7202aaa1bdd66/aplogo.svg"
                }
            })
            
    return articles_data