#  AI-RAG 多模态私有知识库问答系统

基于 FastAPI + LangChain + ChromaDB + YOLO 构建的私有知识库问答系统。支持文本与图像双模态输入，可实现“视觉感知 -> 知识检索 -> 智能决策”的端到端闭环。

##  核心特性
- **多模态闭环**：支持上传图片，通过 YOLO 进行目标检测，并将识别结果作为检索条件，交由 RAG 系统生成决策建议。
- **双模型热切换**：前端网页一键切换云端大模型（DeepSeek）与本地大模型（Qwen3-8B）。
- **多格式文档解析**：支持 TXT、MD、PDF、DOCX 四种格式的私有文档加载与向量化。
- **工程化规范**：`.env` 密钥隔离，`.gitignore` 过滤敏感数据，完善了 401/429/超时/显存溢出等异常处理。
- **Windows 踩坑实录**：项目附带开发日志，记录了多线程导致系统蓝屏、网络超时、日期检索语义漂移等真实问题的解决方案。

##  技术栈
- **后端**：Python 3.11, FastAPI, Uvicorn
- **RAG**：LangChain, ChromaDB, HuggingFace Embeddings (BGE)
- **视觉**：YOLOv8 (Ultralytics)
- **模型**：DeepSeek API（云端） / Qwen3-8B（本地 LM Studio）

##  快速启动
1. 安装依赖：`pip install -r requirements.txt`
2. 配置 `.env` 文件（参考 `.env.example` 或在本地新建）
3. 构建知识库：`python build_kb.py`
4. 启动服务：`uvicorn main:app --reload --app-dir local_llm_project`
5. 访问 `http://127.0.0.1:8000` 进行多模态问答体验。

##  演示截图
*(把你在网页上传图片后，YOLO识别结果和RAG建议的那张截图贴在这里)*

##  开发日志
详细的环境搭建、踩坑记录与排错过程，请查看 [docs/dev_log.md](docs/dev_log.md)。
