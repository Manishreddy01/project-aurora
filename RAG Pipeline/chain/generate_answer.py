# backend/rag/chain/generate_answer.py
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# add parent folder to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from tools.web_search import search_web  # ← fallback

# Load API key
load_dotenv()
openrouter_key = os.getenv("OPENROUTER_API_KEY")


def generate_answer(query: str, k: int = 3):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    client = QdrantClient(url="http://localhost:6333")
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="rag_collection",
        embedding=embedder
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

    docs = retriever.get_relevant_documents(query)

    if not docs:
        print("🔁 No relevant documents found in Qdrant. Triggering fallback...")
        fb = search_web(query)
        if isinstance(fb, dict):
            fb_answer = fb.get("answer") or fb.get("result") or str(fb)
            fb_sources = fb.get("sources", [])
        else:
            fb_answer = str(fb)
            fb_sources = []
        return {
            "answer": fb_answer,
            "result": fb_answer,
            "sources": fb_sources,
            "sourceDocuments": fb_sources,
            "confidence": 0.0,
            "type": "web"
        }

    # Use LLM to answer from documents
    llm = ChatOpenAI(
        temperature=0,
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=openrouter_key,
        model="openai/gpt-3.5-turbo"
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    chain_output = qa_chain.invoke({"query": query})

    # Normalize different possible return shapes
    if isinstance(chain_output, str):
        answer_text = chain_output
        source_docs = []
    elif isinstance(chain_output, dict):
        answer_text = (
            chain_output.get("result")
            or chain_output.get("output_text")
            or str(chain_output)
        )
        source_docs = chain_output.get("source_documents") or chain_output.get("context") or []
    else:
        answer_text = str(chain_output)
        source_docs = []

    # Build normalized sources
    sources = []
    for i, d in enumerate(source_docs):
        meta = getattr(d, "metadata", {}) or (d.get("metadata", {}) if isinstance(d, dict) else {})
        score = getattr(d, "score", None)
        sources.append({
            "source": meta.get("source") or meta.get("fileName") or "unknown",
            "chunkIndex": meta.get("chunkIndex", i),
            "score": float(score) if score is not None else float(meta.get("score", 0.0)),
            "metadata": meta
        })

    # Debug log
    print("\n🧠 Answer:", answer_text)

    # Always return a structured payload
    return {
        "answer": answer_text,
        "result": answer_text,        # keep for backward-compat
        "sources": sources,
        "sourceDocuments": sources,   # alt key some code expects
        "confidence": 0.9,
        "type": "document"
    }


if __name__ == "__main__":
    out = generate_answer("Who is Manesh Reddy?")
    print(out)
