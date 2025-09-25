# run.py
import uvicorn

# 运行过程：
# 1.启动 API：python run.py
#
# 2.访问 Swagger UI：http://127.0.0.1:8000/docs
#
# 3.上传文档：POST /upload, 上传一个 .txt 文件
#
# 4.用知识库问问题：POST /chat?use_rag=true /普通对话：POST /chat?use_rag=false
#   "model": "llama3"


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


