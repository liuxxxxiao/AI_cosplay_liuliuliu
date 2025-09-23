# app/routes/chat_v1.py
from fastapi import APIRouter, HTTPException, Query
from app.models import PromptRequest, PromptResponse
from app.services.ollama_service import call_ollama
from app.services.rag_service import rag_query
from app.services.memory_service_redis import generate_session_id
from app.services.retriever_service import RetrieverConfig
from app.logger import logger

router = APIRouter()

@router.post("/chat", response_model=PromptResponse)
def chat_with_model(
    data: PromptRequest,
    use_rag: bool = Query(False, description="是否使用知识库RAG"),
    use_memory: bool = Query(False, description="是否使用历史上下文（仅RAG模式有效）"),
    session_id: str = Query(None, description="会话ID，可由外部系统传入（未传则自动生成，用于测试）"),
    k: int = Query(3, description="检索文档数量"),
    score_threshold: float = Query(None, description="相似度阈值 (0-1)"),
    filter_department: str = Query(None, description="可选：部门过滤，例如 legal")
):
    try:
        # 如果 session_id 未传，则生成一个测试用的
        if not session_id:
            session_id = generate_session_id()

        if use_rag:
            filter_metadata = {"department": filter_department} if filter_department else None
            retriever_config = RetrieverConfig(k=k, score_threshold=score_threshold, filter_metadata=filter_metadata)

            answer = rag_query(
                data.prompt,
                model=data.model,
                session_id=session_id,
                use_memory=use_memory,
                retriever_config=retriever_config
            )
        else:
            answer = call_ollama(data.prompt, model=data.model)

        logger.info("chat_request_received", prompt=data.prompt, use_rag=use_rag, retriever_config=retriever_config)


        return PromptResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# 5. 工作流程
# 1.用户调用 /chat
# 如果没传 session_id → 自动生成 UUID
# 如果 use_rag=True & use_memory=True → 带上历史记录
#
# 2.rag_service.py 检索 FAISS 结果
#
# 3.拼接 历史 + 知识库内容 + 问题
#
# 4.调用 call_ollama
#
# 5.如果 use_memory=True → 保存问答到 Redis
#
# 6.Redis 自动清理超过 TTL 的会话
