from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db
from swarm.graph import swarm_app

router = APIRouter(prefix="/articles", tags=["articles"])

def execute_swarm(topic: str, limit: int, db: Session):
    print(f"🚀 Triggering Swarm for: {topic}")
    initial_state = {
        "topic": topic,
        "target_count": limit,
        "raw_urls": [],
        "scraped_content": [],
        "final_reports": [],
        "errors": []
    }
    final_state = swarm_app.invoke(initial_state)
    reports = final_state.get("final_reports", [])
    
    # Save the reports to the database
    for r in reports:
        # Check if URL exists
        existing = db.query(models.Article).filter(models.Article.url == str(r["url"])).first()
        if not existing:
            ana = r["analysis"]
            art_data = {
                "title": r["title"],
                "url": r["url"],
                "source_name": r.get("source", "Unknown"),
                "content_markdown": r.get("content_markdown", ""),
                "is_analysed": True,
                "sentiment": ana.get("sentiment"),
                "sentiment_score": ana.get("sentiment_score", 0.0),
                "urgency_score": ana.get("urgency_score", 0.0),
                "sarcasm_prob": ana.get("sarcasm_prob", 0.0),
                "entities": {"persons": ana.get("persons", []), "locations": ana.get("locations", []), "orgs": ana.get("orgs", [])},
                "topics": ana.get("topics", []),
                "keywords": ana.get("keywords", []),
                "summary": ana.get("summary", ""),
            }
            new_art = models.Article(**art_data)
            db.add(new_art)
    
    db.commit()
    print(f"✅ Swarm completed. Saved {len(reports)} intel drops.")

@router.post("/run_swarm", status_code=202)
def run_swarm(background_tasks: BackgroundTasks, topic: str = "أهم الأخبار العاجلة", limit: int = 3, db: Session = Depends(get_db)):
    """Triggers the Multi-Agent LangGraph Swarm to gather and analyze intelligence."""
    background_tasks.add_task(execute_swarm, topic, limit, db)
    return {"message": "Swarm initiated in background.", "topic": topic, "expected_targets": limit}

@router.get("/", response_model=List[schemas.ArticleResponse])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = db.query(models.Article).order_by(models.Article.created_at.desc()).offset(skip).limit(limit).all()
    return articles

@router.post("/", response_model=schemas.ArticleResponse)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    db_article = db.query(models.Article).filter(models.Article.url == str(article.url)).first()
    if db_article:
        raise HTTPException(status_code=400, detail="Article already exists in Intelligence DB")
    
    new_art = models.Article(**article.dict())
    db.add(new_art)
    db.commit()
    db.refresh(new_art)
    return new_art

@router.get("/{article_id}", response_model=schemas.ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

