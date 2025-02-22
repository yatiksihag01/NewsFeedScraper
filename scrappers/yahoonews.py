import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_yahoonews_articles():
        
    # Yahoo News URL
    url = "https://news.yahoo.com/"

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
        articles = soup.find_all('div', class_='react-wafer-ntk-desktop js-stream-item-wrap Pos(r)')

        for article in articles:
            # Extract title
            title_tag = article.find('h3')
            title = title_tag.text.strip() if title_tag else 'No title found'

            # Extract article URL
            link_tag = article.find('a', class_='ntk-link')
            article_url = urljoin(url, link_tag['href']) if link_tag and link_tag.has_attr('href') else 'No URL found'

            # Extract description
            desc_tag = article.find('p')
            description = desc_tag.text.strip() if desc_tag else 'No description found'

            # Extract image URL
            img_tag = article.find('img')
            url_to_image = urljoin(url, img_tag['src']) if img_tag and img_tag.has_attr('src') else 'No image found'

            # Extract published date
            date_tag = article.find('time')
            published_at = date_tag.text.strip() if date_tag else 'No date found'

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "sourceDto": {
                    "name": "Yahoo News"
                }
            })

        # ---- Extract "Stories for you" articles separately ----
    stories_section = soup.find('div', id='module-stream')

    if stories_section:
        stories_articles = stories_section.find_all('li', class_='stream-item')

        for story in stories_articles:
            # Extract title
            title_tag = story.find('h3', class_='stream-item-title')
            title = title_tag.text.strip() if title_tag else 'No title found'

            # Extract article URL
            link_tag = story.find('a', class_='js-content-viewer')
            article_url = urljoin(url, link_tag['href']) if link_tag and link_tag.has_attr('href') else 'No URL found'

            # Extract description
            description_tag = story.find('p')  # This will get the first <p> tag found
            description = description_tag.text.strip() if description_tag else "No description available"
            # Extract image URL
            img_tag = story.find('img')
            url_to_image = urljoin(url, img_tag['src']) if img_tag and img_tag.has_attr('src') else 'No image found'

            # Extract published date
            date_tag = story.find('time')
            published_at = date_tag.text.strip() if date_tag else 'No date found'

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "sourceDto": {
                    "name": "Yahoo News"
                }
            })

    return articles_data
