from typing import List, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import crud
from database.base import get_db, Base, engine
from database.crud import delete_old_articles
from schemas.news import NewsResponse
from scrappers.tasks import scrap_and_save_articles

app = FastAPI()
Base.metadata.create_all(bind=engine)
scheduler = BackgroundScheduler()


@app.on_event("startup")
async def start_scheduler():
    scheduler.add_job(scrap_and_save_articles, "interval", minutes=20)
    scheduler.add_job(delete_old_articles, "interval", hours=24)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


@app.get("/fetch_news", response_model=List[NewsResponse])
def fetch_news(
        last_item_uuid: Optional[str] = None,
        limit: int = 100, db: Session = Depends(get_db)
):
    if limit > 100: limit = 100
    article = crud.get_article_by_uuid(db=db, uuid=last_item_uuid)
    # If UUID not found (e.g., scraper DB reset), start from the first article
    last_item_id = article.id if article else 0
    return crud.get_news_from_db(db=db, last_item_id=last_item_id, limit=limit)


@app.get("/fetch_trending_news", response_model=List[NewsResponse])
def fetch_trending_news(
        last_item_uuid: Optional[str] = None,
        limit: int = 50,
        db: Session = Depends(get_db)
):
    if limit > 50: limit = 50
    article = crud.get_article_by_uuid(db=db, uuid=last_item_uuid)
    last_item_id = article.id if article else 0
    return crud.get_trending_news_from_db(db=db, last_item_id=last_item_id, limit=limit)
