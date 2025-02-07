import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class SourceDto:
    def __init__(self, name, imageUrl=None):
        self.name = name
        self.imageUrl = imageUrl

class ArticleDto:
    def __init__(self, title, url, description, urlToImage, publishedAt, sourceDto):
        self.title = title
        self.url = url
        self.description = description
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt
        self.sourceDto = sourceDto

# Target website URL
url = "https://news.un.org/en/news"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

# Check if request is successful
if response.status_code != 200:
    print(f"Error: Unable to retrieve page. Status code: {response.status_code}")
else:
    soup = BeautifulSoup(response.text, 'html.parser')

    articles_data = []

    # Find all article blocks
    articles = soup.find_all('article', class_='node--type-news-story')

    for article in articles:
        # Extract Title
        title_tag = article.find('h2', class_='node__title')
        title = title_tag.text.strip() if title_tag else 'No title found'

        # Extract Article URL
        link_tag = title_tag.find('a') if title_tag else None
        article_url = urljoin(url, link_tag['href']) if link_tag else 'No URL found'

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
                    url_to_image = urljoin(url, source_tags[-1]['srcset'].split(',')[0].strip().split(' ')[0])  # Get the last <source>

            # If <picture> not found or no <source> images, try <img>
            if url_to_image == 'No image found':
                img_tag = image_container.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    url_to_image = img_tag['src']

        # Extract Published Date (if available)
        time_tag = article.find('time')
        published_at = time_tag['datetime'].split('T')[0] if time_tag else 'No date found'

        # Hardcoded source name
        source_name = "United Nations"
        source_dto = SourceDto(name=source_name)

        # Create Article DTO
        article_dto = ArticleDto(
            title=title,
            url=article_url,
            description=description,
            urlToImage=url_to_image,
            publishedAt=published_at,
            sourceDto=source_dto
        )

        articles_data.append(article_dto)

    # Print extracted articles
    for article in articles_data:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Description: {article.description}")
        print(f"Image URL: {article.urlToImage}")
        print(f"Published At: {article.publishedAt}")
        print(f"Source: {article.sourceDto.name}")
        print("-" * 50)
