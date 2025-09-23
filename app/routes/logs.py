# app/routes/logs.py
# 加个接口方便下载 CSV（若启用 csv sink）：
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.logging_service import get_logger
import os

router = APIRouter()

@router.get("/logs/export")
def export_logs():
    path = get_logger().export_csv_path()
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="CSV 日志未启用或文件不存在")
    return FileResponse(path, filename="rag_logs.csv", media_type="text/csv")
