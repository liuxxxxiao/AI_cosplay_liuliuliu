from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import chat, health, upload

app = FastAPI()


# 注册路由
app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(health.router)

# CORS 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段可用 "*"，生产可指定前端地址，比如 ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is running."}


