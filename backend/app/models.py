# app/models.py
from pydantic import BaseModel
from typing import Optional, Dict

class RetrieverConfigModel(BaseModel):
    k: int = 3
    score_threshold: Optional[float] = None
    filter_metadata: Optional[Dict[str, str]] = None

# class PromptRequest(BaseModel):
#     prompt: str             # prompt
#     model: str = "llama3"
#     use_rag: bool = False
#     use_memory: bool = False
#     session_id: Optional[str] = None
#     retriever_config: Optional[RetrieverConfigModel] = None

# class PromptResponse(BaseModel):
#     response: str

class PromptRequest(BaseModel):
    question: str           # 用户的问题
    isAudio: bool = False   # 是否需要返回语音，默认 False

class PromptResponse(BaseModel):
    response: str   # AI文本回复
    audio_url: str  # 语音文件URL

