import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def get_retriever(query: str, k: int = 3):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    client = QdrantClient(url="http://localhost:6333")
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="rag_collection",
        embedding=embedder
    )

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})
    results = retriever.get_relevant_documents(query)

    print(f"\n🔍 Query: {query}")
    for i, doc in enumerate(results, 1):
        print(f"\n📄 Result {i}:\n{doc.page_content}\n---")

if __name__ == "__main__":
    get_retriever("What is LangChain?")
