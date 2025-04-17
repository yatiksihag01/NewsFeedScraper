from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utils.constants import header, mprnews_url


def fetch_mprnews_articles():
    # Send an HTTP request to get the page content with User-Agent header
    headers = {
        "User-Agent": header
    }

    # List to store articles
    articles_data = []

    response = requests.get(mprnews_url, headers=headers)

    # Check if the request is successful
    if response.status_code != 200:
        print("Error: Unable to retrieve page.")
    else:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the source name and image URL
        source_name = "MPR News"
        source_image_url = mprnews_url + "img/MPR-news-logo.svg"

        # Scrape the main story section
        main_story = soup.find('div', class_='home-main-story-body')
        if main_story:
            title_tag = main_story.find('h2') or main_story.find('h3') or main_story.find('a')
            title = title_tag.text.strip() if title_tag else 'No title found'
            link_tag = main_story.find('a', href=True)
            article_url = urljoin(mprnews_url, link_tag['href']) if link_tag else 'No URL found'
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

            articles_data.append({
                "title": title,
                "url": article_url,
                "description": description,
                "urlToImage": url_to_image,
                "publishedAt": published_at,
                "source": {
                    "name": source_name,
                    "imageUrl": source_image_url
                }
            })

        # Scrape the latest news section
        latest_news = soup.find('div', class_='home-latest-news')
        if latest_news:
            articles = latest_news.find_all('li')
            for article in articles:
                title_tag = article.find('h2') or article.find('h3')
                title = title_tag.text.strip() if title_tag else 'No title found'
                link_tag = article.find('a', href=True)
                article_url = urljoin(mprnews_url, link_tag['href']) if link_tag else 'No URL found'
                description_tag = article.find('p')
                description = description_tag.text.strip() if description_tag else 'No description found'
                img_tag = article.find('img')
                url_to_image = img_tag['src'] if img_tag else 'No image found'

                # Extract published date
                time_tag = article.find('div', class_='home-time-ago')
                date_tag = article.find_all('div')[1]  # Assuming the date is the second div in the article
                published_at = f"{date_tag.text.strip()} {time_tag.text.strip()}" if time_tag and date_tag else 'No date found'

                articles_data.append({
                    "title": title,
                    "url": article_url,
                    "description": description,
                    "urlToImage": url_to_image,
                    "publishedAt": published_at,
                    "source": {
                        "name": source_name,
                        "imageUrl": source_image_url
                    }
                })

        # Scrape the home more stories section
        more_stories = soup.find('div', class_='home-more-stories')
        if more_stories:
            articles = more_stories.find_all('li')
            for article in articles:
                title_tag = article.find('h2') or article.find('h3')
                title = title_tag.text.strip() if title_tag else 'No title found'
                link_tag = article.find('a', href=True)
                article_url = urljoin(mprnews_url, link_tag['href']) if link_tag else 'No URL found'
                description_tag = article.find('p')
                description = description_tag.text.strip() if description_tag else 'No description found'
                img_tag = article.find('img')
                url_to_image = img_tag['src'] if img_tag else 'No image found'

                # Extract only the time
                time_tag = article.find('div', class_='home-time-ago')
                published_at = time_tag.text.strip() if time_tag else 'No time found'

                articles_data.append({
                    "title": title,
                    "url": article_url,
                    "description": description,
                    "urlToImage": url_to_image,
                    "publishedAt": published_at,
                    "source": {
                        "name": source_name,
                        "imageUrl": source_image_url
                    }
                })

    print(f"Scrapped {len(articles_data)} articles from MPR News.")
    return articles_data
