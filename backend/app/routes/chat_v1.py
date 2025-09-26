# app/routes/chat_v1.py
from fastapi import APIRouter, HTTPException, Query
from backend.app.models import PromptRequest, PromptResponse
from backend.app.services.ollama_service import call_ollama
from backend.app.services.rag_service import rag_query
from backend.app.services.memory_service_redis import generate_session_id
from backend.app.services.retriever_service import RetrieverConfig
from backend.app.logger import logger
from backend.app.services.tts_service import call_tts
import traceback

router = APIRouter()

# 固定 Prompt 模板
PROMPT_TEMPLATE = """
你是哈利波特，请用魔法师的语气。
用户问题如下：
{question}
请根据已有知识给出简洁清晰的回答。
"""

@router.post("/chat_v1", response_model=PromptResponse)
def chat_with_model(
    data: PromptRequest,
    # session_id: str = Query(None, description="会话ID，可由外部系统传入（未传则自动生成）"),
):
    print(data)
    try:
        # # 会话管理
        # # 如果 session_id 未传，则生成一个新的
        # if not session_id:
        #     session_id = generate_session_id()

        # 模型 和 是否调用RAG
        model = "llama3"
        use_rag = False

        # 拼接 Prompt
        final_prompt = PROMPT_TEMPLATE.format(question=data.question)
        print(final_prompt)

        # 调用 LLM
        try:
            if use_rag:
                retriever_config = RetrieverConfig(k=3, score_threshold=0.5)
                answer = rag_query(
                    final_prompt,
                    model=model,
                    # session_id=session_id,
                    use_memory=False,
                    retriever_config=retriever_config
                )
            else:
                print("model: llama3")
                logger.info(f"Calling LLM with prompt: {final_prompt}")
                answer = call_ollama(final_prompt, model=model)
                print("文本消息生成完毕")

            # logger.info("chat_request_received", prompt=final_prompt, use_rag=use_rag)

        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"LLM 调用失败: {str(e)}\n{tb}")
            raise HTTPException(status_code=500, detail=f"LLM 调用失败: {str(e)}")


        # 调用 TTS
        audio_url = ""
        if data.isAudio:
            try:
                audio_url = call_tts(answer)
            except Exception as e:
                logger.error(f"TTS 调用失败: {str(e)}")
                # 可以选择继续返回文本，而不是完全失败
                audio_url = ""

        return PromptResponse(response=answer, audio_url=audio_url)

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"LLM 调用失败: {str(e)}\n{tb}")
        raise HTTPException(status_code=500, detail=str(e))

# 纯文本版

# @router.post("/chat_v1", response_model=PromptResponse)
# def chat_with_model(
#     data: PromptRequest,
#     use_rag: bool = Query(False, description="是否使用知识库RAG"),
#     use_memory: bool = Query(False, description="是否使用历史上下文（仅RAG模式有效）"),
#     session_id: str = Query(None, description="会话ID，可由外部系统传入（未传则自动生成，用于测试）"),
#     k: int = Query(3, description="检索文档数量"),
#     score_threshold: float = Query(None, description="相似度阈值 (0-1)"),
#     filter_department: str = Query(None, description="可选：部门过滤，例如 legal"),
# ):
#     try:
#         # 如果 session_id 未传，则生成一个测试用的
#         if not session_id:
#             session_id = generate_session_id()
#
#         if use_rag:
#             filter_metadata = {"department": filter_department} if filter_department else None
#             retriever_config = RetrieverConfig(k=k, score_threshold=score_threshold, filter_metadata=filter_metadata)
#
#             answer = rag_query(
#                 data.prompt,
#                 model=data.model,
#                 session_id=session_id,
#                 use_memory=use_memory,
#                 retriever_config=retriever_config
#             )
#         else:
#             answer = call_ollama(data.prompt, model=data.model)
#
#         logger.info("chat_request_received", prompt=data.prompt, use_rag=use_rag, retriever_config=retriever_config)
#
#         # # 🔹 调用 TTS，将文字转语音
#         if isAudio:
#             audio_url = call_tts(answer)
#         else:
#             audio_url = None
#
#
#         return PromptResponse(response=answer, audio_url=audio_url)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#


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
