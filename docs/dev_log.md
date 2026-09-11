# 📘 RAG知识库项目开发日志

## 📌 前期阶段总结（2026-09-03 ~ 2026-09-09）
> 由于前期处于学习摸索阶段，现集中补录总结。
- **完成内容**：完成了 Anaconda 双环境搭建、pip源配置、DeepSeek云端API调用脚本编写、LM Studio 本地 Qwen3-8B 模型部署与本地 API 调用测试。
- **踩坑简记**：对 Python 环境、依赖包冲突有了初步认识，并成功规避了 Windows Defender 隔离导致的问题。

---

## 📅 2026-09-10 ~ 2026-09-11（M4里程碑：FastAPI后端搭建）
**状态**：✅ 通关（云端/本地双模型切换均测试成功）

### 🎯 今日目标
1. 将散落的脚本重构为工程化代码：`main.py`（路由） + `models.py`（业务逻辑）。
2. 搭建 FastAPI 服务，实现 `/chat` 接口，通过参数一键切换云端 DeepSeek 与本地 Qwen3-8B。

### 🚧 踩坑记录与解决方案
*   **坑1：终端路径错误导致服务无法启动**
    *   **报错**：`Could not import module "main"`
    *   **原因**：终端停留在外层目录 `D:\ai_work`，找不到 `local_llm_project` 里的 `main.py`。
    *   **解决**：VSCode 中右键项目文件夹 -> “在集成终端中打开”，确保终端路径与 `main.py` 同级。
*   **坑2：模块导入失败（ImportError）**
    *   **报错**：`cannot import name 'ask_cloud' from 'models'`
    *   **原因**：粘贴了新代码，但**忘记按 `Ctrl+S` 保存**。
    *   **解决**：写代码后强制检查保存状态，确认标签页小白点消失。
*   **坑3：云端API 404报错**
    *   **报错**：`{"answer": "请求失败，状态码: 404"}`
    *   **原因**：`.env` 里 `DEEPSEEK_BASE_URL` 多写了 `/chat/completions`，导致代码拼接后出现双重后缀。
    *   **解决**：`.env` 里只保留到 `/v1`，即 `https://api.deepseek.com/v1`。
*   **坑4：修改 `.env` 后顽固报错**
    *   **原因**：`uvicorn --reload` 只监听 `.py` 文件，不会重新加载 `.env` 环境变量。
    *   **解决**：修改 `.env` 后，必须在终端按 `Ctrl+C` 彻底停止，然后重新启动 `uvicorn main:app --reload`。
*   **坑5：本地大模型报 400 Bad Request**
    *   **报错**：`{"answer": "本地请求失败，状态码: 400"}`
    *   **原因**：LM Studio 的 Server 开着，但没有加载任何模型；且模型名字配置不对。
    *   **解决**：在 LM Studio 里加载 Qwen 模型，去 Local Server 页面复制准确的 Model Identifier 填入 `.env`。

### 💡 核心心法
1. **看报错的层级**：FastAPI 返回 200 代表网络请求通了，内部 JSON 写的 404/400 才是业务逻辑错误，分层排查。
2. **环境变量的独立性**：修改 `.env` 必须重启服务进程，不要迷信热重载。
3. **脚本 vs 服务**：终端聊天脚本里的 `while True` 绝不能带进 FastAPI，否则一个请求就会卡死服务器。

### 📅 下一步计划（M5阶段）
*   准备引入 `chromadb` 和 `langchain`，实现本地文档的加载、切分、向量化。
*   将 RAG 能力接入 `/chat` 接口，并测试幻觉。

---
*(未来的日志继续在下方按日期追加)*