# app/services/rag_service.py

from app.vectorstore.faiss_store import get_faiss_store
from app.services.ollama_service import call_ollama
from app.services.memory_service_redis import get_memory, save_message

def rag_query(query: str, model: str = None, session_id: str = "default", use_memory: bool = False):
    store = get_faiss_store()
    if not store:
        return "知识库为空，请先上传文档。"

    # 1.历史对话
    history_text = ""
    if use_memory:
        history = get_memory(session_id)
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    # 2.检索相似内容
    docs = store.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # 3.构造 prompt
    prompt_parts = []
    if use_memory and history_text:
        prompt_parts.append(f"之前的对话记录：\n{history_text}")
    prompt_parts.append(f"知识库内容：\n{context}")
    prompt_parts.append(f"用户问题：{query}")
    prompt = "\n\n".join(prompt_parts)

    # 4.调用模型
    answer = call_ollama(prompt, model=model)

    # 5.保存历史
    if use_memory:
        save_message(session_id, "user", query)
        save_message(session_id, "assistant", answer)

    return answer
