import os
import requests
from dotenv import load_dotenv

load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")

def search_web(query: str) -> str:
    """
    Searches the web using Tavily and returns the top result summary.
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": tavily_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "include_raw_content": False,
        "max_results": 3
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "No web result found.")
    except Exception as e:
        return f"❌ Web search failed: {str(e)}"
