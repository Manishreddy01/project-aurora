from langchain_community.document_loaders import PyPDFLoader, TextLoader
from pathlib import Path

def load_documents(file_path: str):
    path = Path(file_path)
    
    if path.suffix == ".pdf":
        loader = PyPDFLoader(file_path)
    elif path.suffix == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or TXT.")

    documents = loader.load()
    print(f"📄 Loaded {len(documents)} pages from {file_path}")
    return documents

# Example use (will remove this and import from main.py later)
if __name__ == "__main__":
    sample_path = "sample.txt"  # Replace with your file path
    load_documents(sample_path)
