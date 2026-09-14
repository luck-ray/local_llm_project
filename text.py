import os
# 必须放在最前面：设置国内镜像 + 关闭 Windows 软链接，强制复制文件
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings

print("正在加载模型（如果有下载，请耐心等待）...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'device': 'cpu'}
)

print("正在测试向量化...")
try:
    # 尝试将一句测试文本转化为向量
    res = embeddings.embed_documents(["你好，这是一个测试句子。"])
    print(f"✅ 成功！生成的向量数量：{len(res)}")
    print(f"向量维度：{len(res[0]) if len(res) > 0 else '空'} ")
except Exception as e:
    print(f"❌ 报错：{e}")