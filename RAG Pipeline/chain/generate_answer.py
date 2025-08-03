import sys
from pathlib import Path
import os
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parents[1]))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from tools.web_search import search_web  # ← our fallback

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

    # Check for empty or low-quality results
    relevant_found = any(query.lower() in doc.page_content.lower() for doc in docs)

    if not docs or not relevant_found:
        print("🔁 No relevant documents found in Qdrant. Triggering fallback...")
        fallback_answer = search_web(query)
        print("\n🌐 Fallback Answer:", fallback_answer)
        return

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

    result = qa_chain.invoke({"query": query})

    print("\n🧠 Answer:", result["result"])
    print("\n📚 Source Docs:")
    for i, doc in enumerate(result["source_documents"], 1):
        print(f"\n--- Source {i} ---\n{doc.page_content}\n")

if __name__ == "__main__":
    generate_answer("Who is manesh reddy")
