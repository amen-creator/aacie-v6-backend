import os
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")

def scrape_duckduckgo(query: str, max_results: int = 5) -> list[dict]:
    """Scout Tool: Finds recent news articles from DuckDuckGo."""
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.news(query, max_results=max_results):
                results.append({
                    "title": r.get('title'),
                    "url": r.get('url'),
                    "source": r.get('source'),
                    "date": r.get('date')
                })
        return results
    except Exception as e:
        print(f"Scout Tool Error (DDGS): {e}")
        return []

def extract_article_content(url: str) -> str:
    """Extraction Tool: Uses Jina Reader API to get clean markdown from a URL."""
    try:
        headers = {}
        if JINA_API_KEY:
            headers["Authorization"] = f"Bearer {JINA_API_KEY}"
            
        response = requests.get(f"https://r.jina.ai/{url}", headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Extraction Tool Error (Jina API): {url} -> {e}")
        return ""
