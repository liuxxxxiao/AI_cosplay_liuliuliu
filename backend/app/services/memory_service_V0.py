# app/services/memory_service_V0.py
from langchain.memory import ConversationBufferMemory

# 暂时用一个字典保存不同 session 的 Memory
# 企业中可以换成 Redis / 数据库
_memory_store = {}

def get_memory(session_id: str):
    """获取某个 session 的记忆，如果不存在则创建"""
    if session_id not in _memory_store:
        _memory_store[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return _memory_store[session_id]

def clear_memory(session_id: str):
    """清空某个 session 的记忆"""
    if session_id in _memory_store:
        del _memory_store[session_id]


# # # 为什么要使用一个session作为单元，管理内存单元
# 在多轮对话系统里，session 是一个自然的上下文边界。
# 一个用户的一个会话 就是一个 session
# 在 session 内，模型会记住之前说过的话
# 清除一个 session 的记忆，不会影响其他用户或其他会话
# 如果不按 session 划分，所有用户的历史都会混在一起，容易出现“串话”问题
# 💡 在企业项目中，session_id 通常来自：
# WebSocket 连接 ID
# 登录用户 ID + 时间戳
# 前端生成的 UUID


