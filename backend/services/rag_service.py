import sys
import os

# Add sibling folder 'rag_pipeline/' to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'rag_pipeline')))
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document
from typing import List, Tuple
from rag.chain.generate_answer import generate_answer

def run_rag_pipeline(question: str, chat_history: list, conversation_id: str):
    try:
        result = generate_answer(
            query=question,
            conversation_id=conversation_id,
            chat_history=chat_history
        )

        return {
            "answer": result["answer"],
            "sources": result.get("sources", []),
            "type": result.get("type", "document"),
            "confidence": result.get("confidence", 0.9)
        }

    except Exception as e:
        print(f"[ERROR] Failed in run_rag_pipeline: {e}")
        return {
            "answer": "An error occurred while generating a response.",
            "sources": [],
            "type": "document",
            "confidence": 0.0
        }