import sys
import os

# Add root folder to path so 'loaders' can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from loaders.load_documents import load_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def chunk_documents(documents: list[Document], chunk_size=100, chunk_overlap=20, metadata: dict = None):
    if metadata:
        for doc in documents:
            doc.metadata.update(metadata)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(documents)
    print(f"🧩 Chunked into {len(chunks)} segments.")
    return chunks


# Test only (will move to main.py later)
if __name__ == "__main__":
    from loaders.load_documents import load_documents

    docs = load_documents("sample.txt")
    chunk_documents(docs)
