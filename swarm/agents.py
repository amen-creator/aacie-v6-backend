import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List, Optional

from swarm.state import AgentState
from swarm.tools import scrape_duckduckgo, extract_article_content

load_dotenv()

class IntelligenceSchema(BaseModel):
    sentiment: str = Field(description="المشاعر العامة للنص (إيجابي، سلبي، محايد)")
    sentiment_score: float = Field(description="درجة المشاعر من -1.0 إلى 1.0")
    urgency_score: float = Field(description="مدى خطورة أو أهمية الخبر من 0.0 إلى 1.0")
    sarcasm_prob: float = Field(description="احتمالية السخرية من 0.0 إلى 1.0")
    persons: List[str] = Field(description="أسماء الشخصيات المذكورة")
    locations: List[str] = Field(description="أسماء الأماكن المذكورة")
    orgs: List[str] = Field(description="أسماء المنظمات والشركات المذكورة")
    topics: List[str] = Field(description="المواضيع الرئيسية (سياسة، اقتصاد، تكنولوجيا...)")
    keywords: List[str] = Field(description="أهم الكلمات المفتاحية")
    summary: str = Field(description="ملخص شامل باللغة العربية في حدود 50 كلمة")

# Define the LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=1000,
    api_key=os.getenv("GROQ_API_KEY")
)
structured_llm = llm.with_structured_output(IntelligenceSchema)

# ── Nodes ─────────────────────────────────────────────────────────────

def scout_node(state: AgentState):
    """Searches for news based on the topic."""
    topic = state.get("topic", "أهم الأخبار العاجلة الشرق الأوسط")
    limit = state.get("target_count", 3)
    print(f"🕵️ Scout Agent deployed. Hunting for: {topic}")
    
    results = scrape_duckduckgo(topic, max_results=limit)
    new_urls = [r["url"] for r in results]
    state_updates = {"raw_urls": new_urls, "scraped_content": []}
    
    # Store minimal metadata
    for r in results:
        state_updates["scraped_content"].append({
            "title": r.get("title"),
            "url": r.get("url"),
            "source": r.get("source"),
        })
        
    return state_updates

def extractor_node(state: AgentState):
    """Extracts markdown content via Jina Reader."""
    print("🕸️ Extractor Agent pulling raw markdown...")
    current = state.get("scraped_content", [])
    updated = []
    
    for item in current:
        url = item["url"]
        content = extract_article_content(url)
        item["content_markdown"] = content
        updated.append(item)
        
    return {"scraped_content": updated}

def analyst_node(state: AgentState):
    """Analyzes the extracted content using Llama-3."""
    print("🧠 Analyst Agent processing intelligence...")
    items = state.get("scraped_content", [])
    final_reports = []
    
    for item in items:
        content = item.get("content_markdown", "")
        if not content or len(content) < 100:
            continue
            
        try:
            prompt = f"قم بتحليل هذا المقال الإخباري بدقة واستخرج المطلوبات باللغة العربية:\n\nالعنوان: {item.get('title')}\n\nالنص:\n{content[:4000]}"
            analysis: IntelligenceSchema = structured_llm.invoke(prompt)
            
            report = item.copy()
            report["analysis"] = analysis.dict()
            final_reports.append(report)
            print(f"✅ Analyzed: {item['title']}")
        except Exception as e:
            print(f"❌ Analysis failed for {item.get('url')}: {e}")
            
    return {"final_reports": final_reports}
