from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional

router = APIRouter()

@router.post("/")
async def upload_files(
    files: Optional[List[UploadFile]] = File(None),
    text: Optional[str] = Form(None)
):
    uploaded_file_names = []

    # Log uploaded file names
    if files:
        for file in files:
            uploaded_file_names.append(file.filename)
            # You can save to disk or forward to n8n here
            # content = await file.read()

    # Log pasted text
    if text:
        print("Received pasted text:", text)
        # Forward to n8n/RAG ingestion if needed

    if not files and not text:
        return { "success": False, "message": "No content received" }

    return {
        "success": True,
        "uploadedFiles": uploaded_file_names,
        "textReceived": bool(text)
    }
