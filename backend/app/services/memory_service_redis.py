# app/services/memory_service_redis.py
# Redis版本
import json
import uuid
import redis
from typing import List, Dict

# 初始化 Redis（生产环境可放 config.py）
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

MEMORY_PREFIX = "chat_memory"
MEMORY_TTL = 7 * 24 * 3600  # 7天, 过期时间

def generate_session_id() -> str:
    """生成全局唯一的session_id"""
    return str(uuid.uuid4())

def _get_redis_key(session_id: str) -> str:
    return f"{MEMORY_PREFIX}:{session_id}"

def get_memory(session_id: str) -> List[Dict]:
    """获取会话历史"""
    key = _get_redis_key(session_id)
    data = redis_client.get(key)
    if not data:
        return []
    return json.loads(data)

def save_message(session_id: str, role: str, content: str):
    """保存一条消息到会话"""
    key = _get_redis_key(session_id)
    history = get_memory(session_id)
    history.append({"role": role, "content": content})
    redis_client.setex(key, MEMORY_TTL, json.dumps(history, ensure_ascii=False)) # 使用String类型存储记忆

def clear_memory(session_id: str):
    """清除会话历史"""
    redis_client.delete(_get_redis_key(session_id))


