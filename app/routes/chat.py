# app/routes/chat.py
from fastapi import APIRouter, HTTPException, Query
from app.models import PromptRequest, PromptResponse
from app.services.ollama_service import call_ollama
from app.services.rag_service import rag_query

router = APIRouter()

@router.post("/chat_old", response_model=PromptResponse)
def chat_with_model_old(data: PromptRequest,
                        use_rag: bool = Query(False, description="是否使用知识库RAG")):
    try:
        if use_rag:
            answer = rag_query(data.prompt, model=data.model)
        else:
            answer = call_ollama(data.prompt, model=data.model)
        return PromptResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=PromptResponse)
def chat_with_model(
    data: PromptRequest,
    use_rag: bool = Query(False, description="是否使用知识库RAG"),
    session_id: str = Query("default", description="会话ID，用于区分不同用户/对话")
):
    try:
        if use_rag:
            answer = rag_query(data.prompt, model=data.model, session_id=session_id)
        else:
            answer = call_ollama(data.prompt, model=data.model)
        return PromptResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
