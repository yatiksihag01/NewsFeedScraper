import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_ndtvnews_articles():
    
    # NDTV URL
    url = "https://www.ndtv.com/latest#pfrom=home-ndtv_mainnavigation"

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
    else:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # List to store articles
        articles_data = []

        # ---- Extract main news articles ----
        articles = soup.find_all('li', class_='NwsLstPg-a-li')  # Updated class to match provided HTML

        for article in articles:
            # Extract title
            title_tag = article.find('h2', class_='NwsLstPg_ttl')
            if title_tag:
                title = title_tag.text.strip()
                link_tag = title_tag.find('a')
                article_url = urljoin(url, link_tag['href']) if link_tag and link_tag.has_attr('href') else 'No URL found'
            else:
                title = 'No title found'
                article_url = 'No URL found'

            # Extract description
            description_tag = article.find('p', class_='NwsLstPg_txt txt_tct txt_tct-three')
            description = description_tag.text.strip() if description_tag else 'No description found'

            # Extract image URL
            img_tag = article.find('img', class_='NwsLstPg_img-full')
            url_to_image = urljoin(url, img_tag['src']) if img_tag and img_tag.has_attr('src') else 'No image found'

            # Extract published date
            published_at_tag = article.find('span', class_='NwsLstPg_pst_lnk')
            published_at = published_at_tag.text.strip() if published_at_tag else 'No date found'

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "sourceDto": {
                    "name": "NDTV News",
                    "imageUrl": "https://www.ndtv.com/common/header/images/ndtv_logo_black.gif"
                }
            })
            
    return articles_data