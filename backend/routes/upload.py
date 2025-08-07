from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
import os
import sys

# Import store_vectors from Manesh's rag_pipeline folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'rag_pipeline')))
from rag.vectorstore.store_vectors import store_vectors

router = APIRouter()

@router.post("/")
async def upload_files(
    files: Optional[List[UploadFile]] = File(None),
    text: Optional[str] = Form(None),
    conversationId: Optional[str] = Form(None)
):
    if not conversationId:
        raise HTTPException(status_code=400, detail="Missing conversationId")

    if not files and not text:
        return { "success": False, "message": "No content received" }

    try:
        # Handle file uploads
        if files:
            for file in files:
                content = await file.read()
                decoded = content.decode("utf-8", errors="ignore")
                store_vectors(
                    content=decoded,
                    file_name=file.filename,
                    conversation_id=conversationId
                )
        
        # Handle pasted text
        if text:
            store_vectors(
                content=text,
                file_name="pasted_text.txt",
                conversation_id=conversationId
            )

        return {
            "success": True,
            "uploadedFiles": [f.filename for f in files] if files else [],
            "textReceived": bool(text)
        }

    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        raise HTTPException(status_code=500, detail="Upload failed. Check logs.")
