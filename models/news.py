from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.base import Base


class Source(Base):
    __tablename__ = 'sources'
    name = Column(String, nullable=False, primary_key=True)
    logo_url = Column(String)

    article = relationship('Article', back_populates='source')


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    urlToImage = Column(String)
    description = Column(String, nullable=True)
    publishedAt = Column(DateTime, nullable=False)
    isTrending = Column(Boolean, default=False)

    source_name = Column(String, ForeignKey("sources.name"), nullable=False)
    source = relationship("Source", back_populates="article")
