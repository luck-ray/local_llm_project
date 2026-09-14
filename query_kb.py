#导入环境和加载库
import os
# 必须放在最前面：设置国内镜像 + 关闭 Windows 软链接，强制复制文件
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from models import ask_cloud,ask_local          #调用云端和本地模型封装

CHROMA_PATH="D:/chroma_db"



#编写检索函数
def search_kb(query):
    print("正在打开文件柜...")
    
    embeddings=HuggingFaceEmbeddings(
    model_name=r"D:\models\bge-small-zh-v1.5",
    model_kwargs={'device':'cpu'}
)
#打开已有向量库
    db=Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)
    
    print(f"\n正在检索:{query}")
    #核心方法：similarity_search(相似度搜索)
    #k=3意思是找出三个文本片段
    results=db.similarity_search(query,k=3)
    print(f"检索到{len(results)}个相关片段。")

    for i, doc in enumerate(results):
            print(f"--- 检索到的块 {i+1} ---")
            print(doc.page_content)
            print("\n")
    return results

#拼接搜索结果(用换行符)
def ask_rag(query,model="cloud"):
    #先去检索资料
    docs=search_kb(query)
    #把3个片段内容拼成一大段文字
    context="\n\n".join([doc.page_content for doc in docs])
    print(f"\n---拼接好的背景资料---")
    print(context)
    #构造严格的提示词
    prompt = f"""你是一个严谨的AI助手。请严格根据以下参考资料回答用户的问题。
    【检索变通规则】：
    1. 如果用户询问具体日期（如9月13日），但参考资料中只有相近日期（如9月11日~12日）的内容，请直接总结这些相近日期的资料，并告知用户“未找到精确日期的记录，以下为相近日期的信息供参考”。
    2. 如果参考资料完全没有相关内容，请直接回答“根据已知资料无法回答”，绝不允许编造。
    【参考资料】：
    {context}
    【用户问题】：
    {query}
    """
    #根据参数决定调用云端还是本地
    print(f"\n正在交由{model}模型生成回答...")
    if model=="local":
        answer=ask_local(prompt)
    else:
        answer=ask_cloud(prompt)
    return answer

#测试
if __name__=="__main__":
    #提个问题
    user_question="简要总结一下9月13日的报错情况"
    final_answer=ask_rag(user_question,model="cloud")
    print("\n最终回答：\n",final_answer)        