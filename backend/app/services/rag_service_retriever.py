# app/services/rag_service_retriever.py

from backend.app.services.ollama_service import call_ollama
from backend.app.services.memory_service_redis import get_memory, save_message
from backend.app.services.retriever_service import RetrieverConfig, retrieve_docs
import time
from backend.app.services.logging_service import log_interaction

def rag_query(
        query: str,
        model: str = None,
        session_id: str = "default",
        use_memory: bool = False,
        retriever_config: RetrieverConfig = None,
        user_id: str = None  # 可选：从上游传入
):
    # store = get_faiss_store()
    # if not store:
    #     return "知识库为空，请先上传文档。"
    if retriever_config is None:
        retriever_config = RetrieverConfig(k=3)  # 默认配置

    # 1.历史对话
    history_text = ""
    if use_memory:
        history = get_memory(session_id)
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    # 2.检索相似内容
    t0 = time.time()
    docs = retrieve_docs(query, retriever_config)
    context = "\n".join(docs)

    if not context:
        return "知识库为空或未检索到相关内容，请先上传文档。"

    # 3.构造 prompt
    prompt_parts = []
    if use_memory and history_text:
        prompt_parts.append(f"之前的对话记录：\n{history_text}")
    prompt_parts.append(f"知识库内容：\n{context}")
    prompt_parts.append(f"用户问题：{query}")
    prompt = "\n\n".join(prompt_parts)

    # 4.调用模型
    answer = call_ollama(prompt, model=model)
    latency_ms = (time.time() - t0) * 1000

    # 5.保存历史
    if use_memory:
        save_message(session_id, "user", query)
        save_message(session_id, "assistant", answer)

    # 6. 日志（输入/检索/输出）
    log_interaction(
        session_id=session_id,
        user_id=user_id,
        use_rag=True,
        use_memory=use_memory,
        retriever_k=retriever_config.k,
        retriever_score_threshold=retriever_config.score_threshold,
        retriever_filter=retriever_config.filter_metadata,
        query=query,
        retrieved_docs=docs,
        prompt=prompt,
        answer=answer,
        model=model,
        latency_ms=latency_ms,
    )

    return answer
