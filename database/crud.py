from datetime import datetime, timezone, timedelta
from sqlite3 import IntegrityError
from typing import List, cast

from dateutil import parser
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from database.base import SessionLocal
from models.news import Article, Source
from schemas.news import NewsResponse
from utils.utils import article_to_news_response


def get_news_from_db(db: Session, last_item_id: int, limit: int = 100) -> list[NewsResponse]:
    articles = (
        db.query(Article)
        .options(joinedload(Article.source))
        .filter(Article.id > last_item_id)
        .limit(limit)
        .all()
    )
    articles = cast(List[Article], articles)
    return [article_to_news_response(article) for article in articles]


def get_trending_news_from_db(
        db: Session, last_item_id: int, limit: int = 100
) -> List[NewsResponse]:
    articles = (
        db.query(Article)
        .options(joinedload(Article.source))
        .filter(and_(Article.isTrending == True, Article.id > last_item_id))
        .limit(limit)
        .all()
    )
    articles = cast(List[Article], articles)
    return [article_to_news_response(article) for article in articles]


def save_articles(articles: list[dict]):
    db: Session = SessionLocal()
    try:
        for raw_article in articles:
            try:
                source_data = raw_article.get("source")
                source_name = source_data.get("name")
                if not source_data:
                    continue

                source_obj = db.query(Source).filter_by(name=source_name).first()
                if not source_obj:
                    source_obj = Source(
                        logo_url=source_data.get("imageUrl"),
                        name=source_name
                    )
                    db.add(source_obj)
                    db.flush()  # Ensures source is present for FK constraint

                article = Article(
                    title=raw_article.get("title"),
                    url=raw_article.get("url"),
                    urlToImage=raw_article.get("urlToImage"),
                    description=raw_article.get("description"),
                    publishedAt=parse_datetime(raw_article.get("publishedAt")),
                    source_name=source_name,
                    isTrending=raw_article.get("is_trending", False)
                )

                db.add(article)

            except IntegrityError:
                db.rollback()
            except Exception as e:
                db.rollback()
                print(f"Error saving article ({raw_article.get('url', 'N/A')}): {e}")
        db.commit()
    finally:
        db.close()


def delete_old_articles():
    db = SessionLocal()
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=2)
        cutoff = cutoff_date.isoformat()
        db.query(Article).filter(Article.publishedAt < cutoff).delete(synchronize_session=False)
        db.commit()
        print(f"[{datetime.now()}] Old articles deleted (before {cutoff_date})")
    except Exception as e:
        print(f"Error deleting old articles: {e}")
    finally:
        db.close()


def parse_datetime(value):
    if isinstance(value, datetime):
        return value
    try:
        return parser.parse(value)
    except Exception:
        return datetime.now(timezone.utc)
