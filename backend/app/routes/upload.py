# app/routes/upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from backend.app.vectorstore.faiss_store import add_document_to_store

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = (await file.read()).decode("utf-8")
        add_document_to_store(content)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
