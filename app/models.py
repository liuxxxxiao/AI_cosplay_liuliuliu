# app/models.py
from pydantic import BaseModel
from typing import Optional, Dict

class RetrieverConfigModel(BaseModel):
    k: int = 3
    score_threshold: Optional[float] = None
    filter_metadata: Optional[Dict[str, str]] = None

class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3"
    use_rag: bool = False
    use_memory: bool = False
    session_id: Optional[str] = None
    retriever_config: Optional[RetrieverConfigModel] = None

class PromptResponse(BaseModel):
    response: str