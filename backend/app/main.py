from fastapi import FastAPI

from backend.app.routes import chat, health, upload

app = FastAPI()


# 注册路由
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(health.router)

