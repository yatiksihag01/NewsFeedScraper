import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_bbcnews_articles():
    # BBC News URL
    url = "https://www.bbc.com/news"

    # Fixing the User-Agent header to avoid bot detection
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # List to store articles
    articles_data = []

    # Create a session to handle requests
    session = requests.Session()
    session.headers.update(headers)

    # Send a GET request
    response = session.get(url)

    # Check response status
    if response.status_code != 200:
        print("Error: Unable to retrieve page. Status code:", response.status_code)
    else:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all news blocks using the updated class names
        articles = soup.find_all('div', class_='sc-c6f6255e-0')  # Updated class for article block

        for article in articles:
            # Extract title
            title_tag = article.find('h2', class_='sc-8ea7699c-3')  # Adjusted class name for title
            title = title_tag.text.strip() if title_tag else 'No title found'
            
            # Extract article URL
            link_tag = article.find('a', href=True)
            article_url = urljoin(url, link_tag['href']) if link_tag else 'No URL found'

            # Extract description using 'data-testid' for more accuracy
            desc_tags = article.find_all('p', {'data-testid': 'card-description'})
            description = ' '.join([desc.text.strip() for desc in desc_tags]) if desc_tags else 'No description found'
            
            # Extract image URL from the specific structure
            img_tag = None
            image_div = article.find('div', {'data-testid': 'card-media-wrapper'})
            if image_div:
                img_tag = image_div.find('img')  # Targeting image within the wrapper
            
            if img_tag:
                # Extract URLs from srcset attribute, if available
                if 'srcset' in img_tag.attrs:
                    srcset = img_tag['srcset']
                    srcset_urls = [item.split(' ')[0] for item in srcset.split(',')]
                    
                    # Log srcset URLs for debugging
                    print("Available srcset URLs:", srcset_urls)
                    
                    # Find the URL with 1024w resolution (if available)
                    url_to_image = next((url for url in srcset_urls if '1024w' in url), srcset_urls[0])  # Fall back to first available URL if 1024w not found
                elif 'src' in img_tag.attrs:
                    # Fallback: If no srcset, use the src attribute
                    url_to_image = img_tag['src']
                else:
                    url_to_image = 'No image found'
            else:
                url_to_image = 'No image found'

            # Extract published date from the new HTML structure
            published_tag = article.find('span', {'data-testid': 'card-metadata-lastupdated'})
            published_at = published_tag.text.strip() if published_tag else 'Not Available'

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "sourceDto": {
                    "name": "BBC News",
                    "imageUrl": "https://news.bbcimg.co.uk/nol/shared/img/bbc_news_120x60.gif"
                }
            })
            
    return articles_data
