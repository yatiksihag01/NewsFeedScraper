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

# Base URL of the news website
url = "https://www.mprnews.org/"  

# Send an HTTP request to get the page content with User-Agent header
headers = {
    "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

# Check if the request is successful
print(f"Status Code: {response.status_code}")
if response.status_code != 200:
    print("Error: Unable to retrieve page.")
else:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    articles_data = []

    # Scrape the main story section
    main_story = soup.find('div', class_='home-main-story-body')
    if main_story:
        title_tag = main_story.find('h2') or main_story.find('h3') or main_story.find('a')
        title = title_tag.text.strip() if title_tag else 'No title found'
        link_tag = main_story.find('a', href=True)
        article_url = urljoin(url, link_tag['href']) if link_tag else 'No URL found'
        description_tag = main_story.find('p')
        description = description_tag.text.strip() if description_tag else 'No description found'
        img_tag = main_story.find('img')
        url_to_image = img_tag['src'] if img_tag else 'No image found'
        # Extract the date from the greeting container
        # Extract the time from the home-time-ago class
        time_tags = main_story.find_all('div', class_='home-time-ago')
        if time_tags:
            published_at = time_tags[-1].text.strip()  # Get the last time element
            print(f"Extracted Time: {published_at}")  # Debugging output
        else:
            published_at = 'No time found'
            
        source_name = "MPR News"
        source_image_url = url + "static/logo.png"  # Placeholder for source logo

        source_dto = SourceDto(name=source_name, imageUrl=source_image_url)

        article_dto = ArticleDto(
            title=title,
            url=article_url,
            description=description,
            urlToImage=url_to_image,
            publishedAt=published_at,
            sourceDto=source_dto
        )

        articles_data.append(article_dto)

    # Scrape the latest news section
    latest_news = soup.find('div', class_='home-latest-news')
    if latest_news:
        articles = latest_news.find_all('li')
        for article in articles:
            title_tag = article.find('h2') or article.find('h3')
            title = title_tag.text.strip() if title_tag else 'No title found'
            link_tag = article.find('a', href=True)
            article_url = urljoin(url, link_tag['href']) if link_tag else 'No URL found'
            description_tag = article.find('p')
            description = description_tag.text.strip() if description_tag else 'No description found'
            img_tag = article.find('img')
            url_to_image = img_tag['src'] if img_tag else 'No image found'
            
            # Extract published date
            time_tag = article.find('div', class_='home-time-ago')
            date_tag = article.find_all('div')[1]  # Assuming the date is the second div in the article
            published_at = f"{date_tag.text.strip()} {time_tag.text.strip()}" if time_tag and date_tag else 'No date found'

            source_name = "MPR News"
            source_image_url = url + "static/logo.png"  # Placeholder for source logo

            source_dto = SourceDto(name=source_name, imageUrl=source_image_url)

            article_dto = ArticleDto(
                title=title,
                url=article_url,
                description=description,
                urlToImage=url_to_image,
                publishedAt=published_at,
                sourceDto=source_dto
            )

            articles_data.append(article_dto)


    # Scrape the home more stories section
    more_stories = soup.find('div', class_='home-more-stories')
    if more_stories:
        articles = more_stories.find_all('li')
        for article in articles:
            title_tag = article.find('h2') or article.find('h3')
            title = title_tag.text.strip() if title_tag else 'No title found'
            link_tag = article.find('a', href=True)
            article_url = urljoin(url, link_tag['href']) if link_tag else 'No URL found'
            description_tag = article.find('p')
            description = description_tag.text.strip() if description_tag else 'No description found'
            img_tag = article.find('img')
            url_to_image = img_tag['src'] if img_tag else 'No image found'

            # Extract only the time
            time_tag = article.find('div', class_='home-time-ago')
            published_at = time_tag.text.strip() if time_tag else 'No time found'

            source_name = "MPR News"
            source_image_url = url + "static/logo.png"  # Placeholder for source logo

            source_dto = SourceDto(name=source_name, imageUrl=source_image_url)

            article_dto = ArticleDto(
                title=title,
                url=article_url,
                description=description,
                urlToImage=url_to_image,
                publishedAt=published_at,  # Now only contains the time (e.g., "9:06 PM")
                sourceDto=source_dto
            )

            articles_data.append(article_dto)


    # Print extracted articles
    for article in articles_data:
        print(f"Title: {article.title}")
        print(f"URL : {article.url}")
        print(f"Description: {article.description}")
        print(f"Image URL: {article.urlToImage}")
        print(f"Published At: {article.publishedAt}")
        print(f"Source: {article.sourceDto.name}")
        print("-" * 40)
