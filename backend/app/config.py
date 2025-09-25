# app/config.py
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"
VECTOR_DB_PATH = "data/faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

import os

# —— 日志总开关 ——
LOG_SINKS = os.getenv("LOG_SINKS", "csv").split(",")  # 例如: "csv,db,http"
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_CSV_FILE = os.getenv("LOG_CSV_FILE", "rag_logs.csv")

# —— 是否记录敏感字段（谨慎开启）——
LOG_INCLUDE_PROMPT = os.getenv("LOG_INCLUDE_PROMPT", "true").lower() == "true"
LOG_INCLUDE_DOCS = os.getenv("LOG_INCLUDE_DOCS", "true").lower() == "true"

# —— 数据库（用于 DB Sink）——
# SQLite: sqlite:///logs.db
# Postgres: postgresql+psycopg2://user:pass@host:5432/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///logs.db")

# —— Spring Boot 接入（用于 HTTP Sink）——
# 你的点评项目提供的接收日志入口（示例）
SPRING_INGEST_URL = os.getenv(
    "SPRING_INGEST_URL",
    "http://localhost:8080/api/rag/logs/ingest"
)
SPRING_INGEST_TIMEOUT = int(os.getenv("SPRING_INGEST_TIMEOUT", "3"))
