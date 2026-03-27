from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from datetime import datetime
from database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    url = Column(String(1000), unique=True, index=True)
    source_name = Column(String(100))
    published_at = Column(DateTime)
    content_markdown = Column(Text, nullable=True)
    
    # Analysis fields flattened for easy querying and JSON payload
    is_analysed = Column(Boolean, default=False)
    sentiment = Column(String(50), default="محايد")
    sentiment_score = Column(Float, default=0.0)
    urgency_score = Column(Float, default=0.0)
    sarcasm_prob = Column(Float, default=0.0)
    
    # Store complex JSON entities (persons, locations, orgs) 
    entities = Column(JSON, default=dict)
    topics = Column(JSON, default=list)
    keywords = Column(JSON, default=list)
    
    summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    analysed_at = Column(DateTime, nullable=True)
