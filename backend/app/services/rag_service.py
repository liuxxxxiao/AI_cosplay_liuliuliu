# app/services/rag_service.py
from backend.app.vectorstore.faiss_store import get_faiss_store
from backend.app.services.ollama_service import call_ollama
from backend.app.services.memory_service_V0 import get_memory  # 提取记忆功能
# from app.services.memory_service import get_memory, save_message

def rag_query_old(query: str, model: str = None):
    store = get_faiss_store()
    if not store:
        return "知识库为空，请先上传文档。"

    # 检索相似内容
    docs = store.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"基于以下内容回答问题：\n{context}\n\n问题：{query}"
    return call_ollama(prompt, model=model)

def rag_query(query: str, model: str = None, session_id: str = "default", use_memory: bool = False):
    store = get_faiss_store()
    if not store:
        return "知识库为空，请先上传文档。"

    # 1. 取历史记忆
    memory = get_memory(session_id)   # 获取该对话的历史
    history_messages = memory.load_memory_variables({}).get("chat_history", [])
    history_text = "\n".join([f"{m.type}: {m.content}" for m in history_messages])


    # 2. 检索相似内容
    docs = store.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # 3. 构造带历史的 prompt，把历史对话拼接到 prompt 里
    prompt = (
        f"以下是之前的对话：\n{history_text}\n\n"
        f"基于以下知识库内容回答问题：\n{context}\n\n"
        f"问题：{query}"
    )

    # 4. 调用模型
    answer = call_ollama(prompt, model=model)

    # 5. 更新记忆
    memory.save_context({"input": query}, {"output": answer})

    return answer

