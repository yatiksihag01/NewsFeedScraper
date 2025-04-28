from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from models.news import Article
from schemas.news import NewsResponse, SourceResponse


def is_trending(pub_date_str):
    try:
        pub_date = parsedate_to_datetime(pub_date_str)
        age_hours = (datetime.now(timezone.utc) - pub_date).total_seconds() / 3600
        return age_hours < 2
    except Exception:
        return False


def article_to_news_response(article: Article):
    source = SourceResponse(
        name=article.source.name,
        logo_url=article.source.logo_url
    )
    news_response = NewsResponse(
        id=article.id,
        uuid=article.uuid,
        title=article.title,
        url=article.url,
        description=article.description,
        urlToImage=article.urlToImage,
        publishedAt=article.publishedAt,
        source=source,
        isTrending=article.isTrending
    )
    return news_response


def get_source_logo(source_name):
    logos = {
        'Associated Press': 'https://assets.apnews.com/fa/ba/9258a7114f5ba5c7202aaa1bdd66/aplogo.svg',
        'CNN': 'https://upload.wikimedia.org/wikipedia/commons/b/b1/CNN.svg',
        'BBC': 'https://news.bbcimg.co.uk/nol/shared/img/bbc_news_120x60.gif',
        'HuffPost': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/HuffPost.svg/1080px-HuffPost.svg.png',
        'Fox News': 'https://upload.wikimedia.org/wikipedia/commons/6/67/Fox_News_Channel_logo.svg',
        'TechCrunch': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/TechCrunch_logo.svg/300px-TechCrunch_logo.svg.png',
    }

    return logos.get(source_name)
