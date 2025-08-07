import sys
from pathlib import Path
from typing import Union

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

from embeddings.text_splitter import chunk_documents
from loaders.load_documents import load_documents


def get_qdrant_client():
    return QdrantClient(url="http://localhost:6333")


def create_collection(client, collection_name="rag_collection"):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )


def store_in_qdrant(chunks, collection_name="rag_collection", metadata=None):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    client = get_qdrant_client()
    create_collection(client, collection_name)

    if metadata:
        for i, chunk in enumerate(chunks):
            chunk.metadata = {
                "conversationId": metadata.get("conversationId"),
                "source": metadata.get("fileName"),
                "chunkIndex": i
            }

    Qdrant.from_documents(
        documents=chunks,
        embedding=embedder,
        url="http://localhost:6333",
        collection_name=collection_name
    )

    print(f"✅ Stored {len(chunks)} chunks in Qdrant under collection '{collection_name}'.")


def store_vectors(content: Union[str, bytes], file_name: str, conversation_id: str):
    try:
        # Case 1: content is file path
        if isinstance(content, str) and Path(content).exists():
            documents = load_documents(file_path=Path(content))
        
        # Case 2: content is in-memory bytes (file upload)
        elif isinstance(content, bytes):
            documents = load_documents(content, file_name)

        
        # Case 3: content is plain text (from textarea)
        elif isinstance(content, str):
            documents = load_documents(file_content=content.encode(), file_name="pasted_text.txt")
        
        else:
            raise ValueError("Unsupported content type in store_vectors()")

        chunks = chunk_documents(documents)
        if not chunks:
            print("⚠️ No chunks generated from document. Skipping embedding.")
            return

        store_in_qdrant(chunks, metadata={
            "fileName": file_name,
            "conversationId": conversation_id
        })

    except Exception as e:
        print(f"[ERROR] store_vectors failed: {e}")
        raise


if __name__ == "__main__":
    docs = load_documents(file_path=Path("irrelevant_data.txt"))
    chunks = chunk_documents(docs)
    store_in_qdrant(chunks)
