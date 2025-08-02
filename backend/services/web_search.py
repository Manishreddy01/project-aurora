import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_web_with_tavily(question: str):
    url = "https://api.tavily.com/search"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TAVILY_API_KEY}"
    }

    payload = {
        "query": question,
        "search_depth": "advanced",
        "include_answer": True,
        "include_raw_content": False
    }

    try:
        response = httpx.post(url, json=payload, headers=headers)
        data = response.json()

        return {
            "answer": data.get("answer", "No answer found from web."),
            "sources": [s["url"] for s in data.get("results", [])],
            "type": "web",
            "confidence": 0.75
        }
    except Exception as e:
        return {
            "answer": "Web search failed.",
            "sources": [],
            "type": "web",
            "confidence": 0.0
        }
