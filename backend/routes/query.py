from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from services.rag_service import run_rag_pipeline
from services.web_search import search_web_with_tavily  
router = APIRouter()

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
    question = payload.question
    conversation_id = payload.conversationId

    if not question or not conversation_id:
        raise HTTPException(status_code=400, detail="Missing question or conversationId")

    rag_result = run_rag_pipeline(question, chat_history, conversation_id)

    # Step 2: Fallback to web search if confidence too low
    if rag_result["confidence"] < CONFIDENCE_THRESHOLD:
        print("RAG confidence too low. Switching to web search fallback.")
        return search_web_with_tavily(question)

    return rag_result
