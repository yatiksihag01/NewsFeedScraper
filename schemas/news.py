from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SourceResponse(BaseModel):
    name: str
    logo_url: Optional[str]

    class Config:
        from_attributes: True


class NewsResponse(BaseModel):
    id: int
    title: str
    url: str
    urlToImage: Optional[str]
    description: Optional[str]
    publishedAt: datetime
    source: SourceResponse
    isTrending: bool

    class Config:
        from_attributes: True
