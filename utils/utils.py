from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def is_trending(pub_date_str):
    try:
        pub_date = parsedate_to_datetime(pub_date_str)
        age_hours = (datetime.now(timezone.utc) - pub_date).total_seconds() / 3600
        return age_hours < 2
    except Exception:
        return False
