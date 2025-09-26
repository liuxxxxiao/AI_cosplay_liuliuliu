# AI_cosplay_liuliuliu
开发一个利用AI来做角色扮演的网站

# 《运行程序说明文档》  
## 1. 项目结构  
AI_cosplay_liuliuliu/  
│── backend/              # FastAPI 后端  
│   ├── run.py            # 后端入口  
│   ├── app/              # 后端入口  
│   │  ├── routers/       # API 路由（含 chat，upload）  
│   │  ├── services/      # LLM 调用、RAG 逻辑、tts调用  
│   │  ├── vectorstore/   # faiss 向量检索  
│   ├── data/             # 数据库
│   └── requirements.txt  # Python 依赖  
│  
│── frontend/             # 前端  
│   ├── index.html        # 页面入口  
│   ├── src/              # 前端源码  
│   └── package.json      # npm 配置 
## 2. 环境准备及启动
### 1. 后端  
      cd backend\
      pip install -r requirements.txt  
      python run.py  
### 2. 前端  
      cd frontend  
      npm install  
      npm run dev  
### 3. 启动后打开：http://127.0.0.1:5173/
