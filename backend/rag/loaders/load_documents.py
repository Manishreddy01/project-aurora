from typing import List, Union
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from pathlib import Path
import tempfile

def load_documents(file_content_or_path: Union[str, bytes], file_name: str) -> List[Document]:
    suffix = Path(file_name).suffix.lower()

    # If content is a file path
    if isinstance(file_content_or_path, str) and Path(file_content_or_path).exists():
        file_path = file_content_or_path

    else:
        # Write bytes or string to a temp file
        if isinstance(file_content_or_path, str):
            file_content_or_path = file_content_or_path.encode()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_content_or_path)
            tmp.flush()
            file_path = tmp.name

    if suffix == ".pdf":
        loader = PyPDFLoader(file_path)
    elif suffix == ".txt":
        loader = TextLoader(file_path)
    elif suffix == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    documents = loader.load()
    print(f"📄 Loaded {len(documents)} pages from {file_name}")
    return documents
