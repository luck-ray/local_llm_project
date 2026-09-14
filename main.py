from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import ask_cloud, ask_local
from query_kb import ask_rag        #导入问答函数

app = FastAPI(title="RAG知识库问答系统")

# 解决跨域问题，允许前端调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求体格式
class ChatRequest(BaseModel):
    message: str
    model: str = "cloud"  # 默认使用云端

@app.get("/health")
def root():
    return {"status": "ok", "message": "后端运行中"}

@app.post("/chat")
def chat(req: ChatRequest):
    """根据传入的 model 参数，自动切换云端或本地模型"""
    if req.model == "local":
        answer = ask_local(req.message)
    elif req.model == "rag":
        #走RAG流程，强制使用云端
        answer = ask_rag(req.message)           #增加了RAG分支
    else:
        answer = ask_cloud(req.message)
    
    return {
        "model": req.model,
        "answer": answer
    }

app.mount("/",StaticFiles(directory="static",html=True),name="static")