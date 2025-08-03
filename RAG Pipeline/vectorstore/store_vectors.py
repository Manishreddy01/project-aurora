import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

from embeddings.text_splitter import chunk_documents
from loaders.load_documents import load_documents


def get_qdrant_client():
    return QdrantClient(
        url="http://localhost:6333"
    )

def create_collection(client, collection_name="rag_collection"):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def store_in_qdrant(chunks, collection_name="rag_collection"):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    client = get_qdrant_client()
    create_collection(client, collection_name)

    qdrant = Qdrant.from_documents(
        documents=chunks,
        embedding=embedder,
        url="http://localhost:6333",
        collection_name=collection_name
    )
    print(f"✅ Stored {len(chunks)} chunks in Qdrant under collection '{collection_name}'.")

if __name__ == "__main__":
    docs = load_documents("irrelevant_data.txt")
    chunks = chunk_documents(docs)
    store_in_qdrant(chunks)
