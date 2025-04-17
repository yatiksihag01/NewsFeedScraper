import random
from datetime import datetime

from database import crud
from scrappers.aljazeera import fetch_aljazeera_articles
from scrappers.apnews import fetch_apnews_articles
from scrappers.bbcnews import fetch_bbc_news_rss
from scrappers.mprnews import fetch_mprnews_articles
from scrappers.ndtvnews import fetch_ndtvnews_articles
from scrappers.nytimes import fetch_ny_times_articles
from scrappers.thegaurdiannews import fetch_guardian_rss_articles
from scrappers.un_news import fetch_un_news_articles
from scrappers.yahoonews import fetch_yahoonews_articles
from utils.constants import bbc_top_news_url, bbc_world_news_url, the_guardian_url, ndtv_world_news_url, \
    ndtv_trending_news_url

all_tasks = [
    fetch_aljazeera_articles,
    fetch_apnews_articles,
    lambda: fetch_bbc_news_rss(bbc_top_news_url),
    lambda: fetch_bbc_news_rss(bbc_world_news_url, trending=True),
    fetch_mprnews_articles,
    lambda: fetch_ndtvnews_articles(ndtv_trending_news_url, is_trending=True),
    lambda: fetch_ndtvnews_articles(ndtv_world_news_url),
    fetch_ny_times_articles,
    lambda: fetch_guardian_rss_articles(the_guardian_url),
    fetch_un_news_articles,
    fetch_yahoonews_articles
]
random.shuffle(all_tasks)
batch_size = 3
current_batch_index = {"index": 0}


def scrap_and_save_articles():
    articles_data = []
    start = current_batch_index["index"] * batch_size
    end = start + batch_size
    batch = all_tasks[start:end]

    print(f"\n[{datetime.now()}] Running batch {current_batch_index['index'] + 1}")
    for task in batch:
        try:
            articles = task()
            if isinstance(articles, list):
                articles_data.extend(articles)
        except Exception as e:
            print(f"Error in {task.__name__}: {e}")

    current_batch_index["index"] = (current_batch_index["index"] + 1) % (len(all_tasks) // batch_size)
    random.shuffle(articles_data)
    crud.save_articles(articles_data)
