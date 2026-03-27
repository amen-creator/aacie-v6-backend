from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    url: HttpUrl
    source_name: str
    published_at: Optional[datetime] = None
    content_markdown: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    is_analysed: bool
    sentiment: str
    sentiment_score: float
    urgency_score: float
    sarcasm_prob: float
    entities: Dict[str, Any]
    topics: List[str]
    keywords: List[str]
    summary: str
    analysed_at: datetime

class ArticleResponse(ArticleBase):
    id: int
    is_analysed: bool
    sentiment: str
    sentiment_score: float
    urgency_score: float
    sarcasm_prob: float
    entities: Dict[str, Any]
    topics: List[str]
    keywords: List[str]
    summary: Optional[str] = None
    created_at: datetime
    analysed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_articles: int
    analysed_articles: int
    avg_sentiment: float
    avg_urgency: float
    top_entities: Dict[str, List[str]]
