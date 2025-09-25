# app/logger.py
import logging
import time

import structlog
from logging.handlers import RotatingFileHandler
import os

# 日志文件路径
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

uuid_str = time.strftime("%Y-%m-%d-%H_%M",time.localtime())
tmp_file_name ='%s.log' % uuid_str

# 配置标准 logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        RotatingFileHandler(os.path.join(LOG_DIR, tmp_file_name), maxBytes=5_000_000, backupCount=5),
        logging.StreamHandler()
    ],
)

# structlog 配置
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()  # 输出 JSON 格式，方便机器分析
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
