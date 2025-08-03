from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from services.rag_service import run_rag_pipeline
from services.web_search import search_web_with_tavily
import time

router = APIRouter()

# Confidence threshold for fallback
CONFIDENCE_THRESHOLD = 0.85

# Request payload format
class QueryRequest(BaseModel):
    question: str
    conversationId: str

# Response format
class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    type: Literal["document", "web"]
    confidence: float

@router.post("/", response_model=QueryResponse)
async def handle_query(payload: QueryRequest):
    start_time = time.time()

    question = payload.question
    conversation_id = payload.conversationId

    if not question or not conversation_id:
        raise HTTPException(status_code=400, detail="Missing question or conversationId")

    try:
        chat_history = []  # optional future use

        rag_result = run_rag_pipeline(question, chat_history, conversation_id)

        if rag_result["confidence"] < CONFIDENCE_THRESHOLD:
            print("RAG confidence too low. Switching to web search fallback.")
            return search_web_with_tavily(question)

        print(f"[Query] Processed in {round(time.time() - start_time, 2)}s")
        return rag_result

    except Exception as e:
        print(f"[ERROR] Exception in /query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
