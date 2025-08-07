from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain.chains import ConversationalRetrievalChain
from services.chat_history import get_chat_history, add_to_chat_history

#from backend.env import openrouter_key  # if openrouter_key is defined there
import os

openrouter_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_key:
    raise ValueError("OPENROUTER_API_KEY not set in environment variables.")


def generate_answer(query: str, chat_history: list = [], conversation_id: str = "", k: int = 3) -> dict:
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

    #relevant_found = any(query.lower() in doc.page_content.lower() for doc in docs)
    #confidence = 0.9 if relevant_found else 0.5
    confidence = 0.85 if docs else 0.5


    if not docs:
        print("🔁 No relevant documents found in Qdrant.")
        return {
            "answer": "",
            "sources": [],
            "type": "document",
            "confidence": confidence
        }

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
    result = qa_chain.invoke({
        "question": query,
        "chat_history": history
    })

    add_to_chat_history(conversation_id, query, result["answer"])
    sources = [doc.metadata.get("source", f"chunk_{i}") for i, doc in enumerate(result["source_documents"])]

    return {
        "answer": result["result"],
        "sources": sources,
        "type": "document",
        "confidence": confidence
    }
