# backend/rag/chain/generate_answer.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

from services.chat_history import get_chat_history, add_to_chat_history

import os

openrouter_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_key:
    raise ValueError("OPENROUTER_API_KEY not set in environment variables.")


def _normalize_answer(chain_output) -> str:
    """Return a string answer from various possible CRC outputs."""
    if isinstance(chain_output, str):
        return chain_output
    if isinstance(chain_output, dict):
        # CRC usually returns 'answer'; older chains might use 'result' or 'output_text'
        return (
            chain_output.get("answer")
            or chain_output.get("result")
            or chain_output.get("output_text")
            or ""
        )
    return str(chain_output)


def _extract_sources(chain_output):
    """Return a list of source ids/paths; tolerate missing keys."""
    docs = []
    if isinstance(chain_output, dict):
        docs = chain_output.get("source_documents") or chain_output.get("context") or []
    sources = []
    for i, d in enumerate(docs):
        meta = getattr(d, "metadata", {}) or (d.get("metadata", {}) if isinstance(d, dict) else {})
        sources.append(meta.get("source", f"chunk_{i}"))
    return sources


def generate_answer(
    query: str,
    chat_history: list = None,
    conversation_id: str = "",
    k: int = 3
) -> dict:
    if chat_history is None:
        chat_history = []

    # --- Retriever (Qdrant + HF embeddings) ---
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    client = QdrantClient(url="http://localhost:6333")
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="rag_collection",
        embedding=embedder
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

    docs = retriever.get_relevant_documents(query)
    print(f"🔎 Retrieved {len(docs)} documents for query: {query}")
    for i, doc in enumerate(docs):
        print(f"--- Doc {i} ---\n{doc.page_content[:300]}\n")

    confidence = 0.85 if docs else 0.5
    if not docs:
        # No docs → let caller decide about web fallback using confidence
        return {
            "answer": "",
            "sources": [],
            "type": "document",
            "confidence": confidence
        }

    # --- LLM QA with conversational context ---
    llm = ChatOpenAI(
        temperature=0,
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=openrouter_key,
        model="openai/gpt-3.5-turbo"
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    history = get_chat_history(conversation_id)
    raw = qa_chain.invoke({
        "question": query,
        "chat_history": history
    })

    answer_text = _normalize_answer(raw)
    sources = _extract_sources(raw)

    # persist conversational turn
    try:
        add_to_chat_history(conversation_id, query, answer_text)
    except Exception as e:
        print(f"[warn] add_to_chat_history failed: {e}")

    # unified return shape
    return {
        "answer": answer_text,          # <- use 'answer' consistently
        "sources": sources,
        "type": "document",
        "confidence": confidence
    }
