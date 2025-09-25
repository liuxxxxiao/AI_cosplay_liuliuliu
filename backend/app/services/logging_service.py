# app/services/logging_service.py
import os
import csv
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.app.config import (
    LOG_SINKS, LOG_DIR, LOG_CSV_FILE,
    LOG_INCLUDE_PROMPT, LOG_INCLUDE_DOCS,
    DATABASE_URL, SPRING_INGEST_URL, SPRING_INGEST_TIMEOUT
)

# ---------- 通用工具 ----------
def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

# ---------- 定义日志记录结构 ----------
def build_record(
    *,
    session_id: str,
    user_id: Optional[str],
    use_rag: bool,
    use_memory: bool,
    retriever_k: Optional[int],
    retriever_score_threshold: Optional[float],
    retriever_filter: Optional[Dict[str, Any]],
    query: str,
    retrieved_docs: Optional[List[str]],
    prompt: Optional[str],
    answer: str,
    model: Optional[str],
    latency_ms: float,
) -> Dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "ts": _now_iso(),
        "session_id": session_id,
        "user_id": user_id,
        "use_rag": use_rag,
        "use_memory": use_memory,
        "retriever_k": retriever_k,
        "retriever_score_threshold": retriever_score_threshold,
        "retriever_filter": retriever_filter or {},
        "query": query,
        # 根据配置决定是否落库/落盘完整内容
        "retrieved_docs": retrieved_docs if LOG_INCLUDE_DOCS else None,
        "prompt": prompt if LOG_INCLUDE_PROMPT else None,
        "answer": answer,
        "model": model,
        "latency_ms": round(latency_ms, 2),
    }

# ---------- CSV Sink ----------
class CsvSink:
    def __init__(self, dir_path: str, filename: str):
        _ensure_dir(dir_path)
        self.filepath = os.path.join(dir_path, filename)
        # 若文件不存在，写入表头
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self._fields())
                writer.writeheader()

    def _fields(self) -> List[str]:
        return [
            "id", "ts", "session_id", "user_id",
            "use_rag", "use_memory",
            "retriever_k", "retriever_score_threshold", "retriever_filter",
            "query", "retrieved_docs", "prompt", "answer",
            "model", "latency_ms"
        ]

    def write(self, record: Dict[str, Any]):
        # 将 dict / list 转成 JSON 字符串，便于 CSV 存储
        row = record.copy()
        for k in ["retriever_filter", "retrieved_docs"]:
            if row.get(k) is not None and not isinstance(row[k], str):
                row[k] = json.dumps(row[k], ensure_ascii=False)
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self._fields())
            writer.writerow(row)

    def export_path(self) -> str:
        return self.filepath

# ---------- DB Sink (SQLAlchemy) ----------
Base = declarative_base()

class RagLog(Base):
    __tablename__ = "rag_logs"

    id = Column(String(64), primary_key=True)
    ts = Column(DateTime, nullable=False, default=datetime.utcnow)

    session_id = Column(String(128), index=True)
    user_id = Column(String(128), index=True)

    use_rag = Column(String(5))     # "true"/"false"
    use_memory = Column(String(5))  # "true"/"false"

    retriever_k = Column(Integer)
    retriever_score_threshold = Column(Float)
    retriever_filter = Column(Text)     # JSON
    query = Column(Text)
    retrieved_docs = Column(Text)       # JSON
    prompt = Column(Text)
    answer = Column(Text)
    model = Column(String(128))
    latency_ms = Column(Float)

class DbSink:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, future=True)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def write(self, record: Dict[str, Any]):
        db = self.SessionLocal()
        try:
            obj = RagLog(
                id=record["id"],
                ts=datetime.strptime(record["ts"], "%Y-%m-%dT%H:%M:%SZ"),
                session_id=record["session_id"],
                user_id=record.get("user_id"),
                use_rag="true" if record["use_rag"] else "false",
                use_memory="true" if record["use_memory"] else "false",
                retriever_k=record.get("retriever_k"),
                retriever_score_threshold=record.get("retriever_score_threshold"),
                retriever_filter=json.dumps(record.get("retriever_filter") or {}, ensure_ascii=False),
                query=record.get("query"),
                retrieved_docs=json.dumps(record.get("retrieved_docs")) if record.get("retrieved_docs") else None,
                prompt=record.get("prompt"),
                answer=record.get("answer"),
                model=record.get("model"),
                latency_ms=record.get("latency_ms"),
            )
            db.add(obj)
            db.commit()
        finally:
            db.close()

# ---------- HTTP Sink（推送给 Spring Boot） ----------
class HttpSink:
    def __init__(self, url: str, timeout: int = 3):
        self.url = url
        self.timeout = timeout

    def write(self, record: Dict[str, Any]):
        try:
            # 失败不抛出，避免影响主流程
            requests.post(self.url, json=record, timeout=self.timeout)
        except Exception:
            pass

# ---------- 组合式 Logger ----------
class RAGLogger:
    def __init__(self):
        self.sinks = []
        if "csv" in LOG_SINKS:
            self.sinks.append(CsvSink(LOG_DIR, LOG_CSV_FILE))
        if "db" in LOG_SINKS:
            self.sinks.append(DbSink(DATABASE_URL))
        if "http" in LOG_SINKS:
            self.sinks.append(HttpSink(SPRING_INGEST_URL, SPRING_INGEST_TIMEOUT))

    def log(self, record: Dict[str, Any]):
        for sink in self.sinks:
            try:
                sink.write(record)
            except Exception:
                # 单个 sink 失败不影响整体
                continue

    # 导出 CSV（若启用 csv sink），返回路径，便于提供下载
    def export_csv_path(self) -> Optional[str]:
        for sink in self.sinks:
            if isinstance(sink, CsvSink):
                return sink.export_path()
        return None

# 单例
_logger: Optional[RAGLogger] = None

def get_logger() -> RAGLogger:
    global _logger
    if _logger is None:
        _logger = RAGLogger()
    return _logger

# 对外：统一的记录接口
def log_interaction(
    *,
    session_id: str,
    user_id: Optional[str],
    use_rag: bool,
    use_memory: bool,
    retriever_k: Optional[int],
    retriever_score_threshold: Optional[float],
    retriever_filter: Optional[Dict[str, Any]],
    query: str,
    retrieved_docs: Optional[List[str]],
    prompt: Optional[str],
    answer: str,
    model: Optional[str],
    latency_ms: float
):
    record = build_record(
        session_id=session_id,
        user_id=user_id,
        use_rag=use_rag,
        use_memory=use_memory,
        retriever_k=retriever_k,
        retriever_score_threshold=retriever_score_threshold,
        retriever_filter=retriever_filter,
        query=query,
        retrieved_docs=retrieved_docs,
        prompt=prompt,
        answer=answer,
        model=model,
        latency_ms=latency_ms,
    )
    get_logger().log(record)

