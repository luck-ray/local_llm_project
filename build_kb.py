import os
# 必须放在最前面：设置国内镜像 + 关闭 Windows 软链接，强制复制文件
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from langchain_community.document_loaders import TextLoader,DirectoryLoader,PyPDFLoader,Docx2txtLoader #引入加载器
from langchain_text_splitters import RecursiveCharacterTextSplitter         #引入切分器
from langchain_community.vectorstores import Chroma         #引入Chroma数据库
    #使用新版
from langchain_huggingface import HuggingFaceEmbeddings         #引入嵌入模型
from pathlib import Path
import shutil

#获取当前脚本所在文件夹
BASE_DIR=Path(__file__).resolve().parent
#定义路径（用绝对路径）
DATA_PATH=str(BASE_DIR/"data")            #文件地址
CHROMA_PATH=r"D:\chroma_db"          #书架强制写在D盘


    #加载文档
def build_vector_db():
    # 调试打印
    print("1.正在加载文档...")
    #清理旧向量库
    if os.path.exists(CHROMA_PATH):
        print(f"检测到旧向量库，正在清理：{CHROMA_PATH}")
        shutil.rmtree(CHROMA_PATH)          #删除旧库

    print(">>> 程序正在扫描的绝对路径是：", DATA_PATH)
    print(">>> 该路径下真实存在的文件有：", os.listdir(DATA_PATH))
    #选择不同的加载器
    def get_loader(file_path):
        #把传进来的字符串转换成Path对象
        path=Path(file_path)
        if path.suffix in ['.txt','.md']:
            return TextLoader(str(path),encoding="utf-8")
        elif path.suffix=='.pdf':
            return PyPDFLoader(str(path))
        elif path.suffix=='.docx':
            return Docx2txtLoader(str(path))
        else:
            print(f"跳过不支持的文件格式：{path.suffix}")
            return None

    print("正在遍历data文件夹...")
    all_documents=[]
    data_dir=Path(DATA_PATH)

    for file_path in data_dir.rglob('*'):
        if not file_path.is_file():
            continue
        #调用上面的get_loader    
        loader=get_loader(file_path)
        #遇到不支持的文件（返回NONE），直接跳过
        if loader is None:
            continue
        try:
            #逐个加载文件
            docs=loader.load()
            all_documents.extend(docs)
            print(f"成功加载：{file_path.name}")
        except Exception as e:
            #遇到坏文件，打印错误并跳过
            print(f"读取{file_path.name}失败：{e}")

    documents=all_documents
    print(f"加载完成，共读取到{len(documents)}份文档")

    #切分文档
    print("2.正在切分文档...")
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=800,         #每个小纸条最多500个字符
        chunk_overlap=50,        #相邻纸条之间重叠50个字符，防止上写文断裂
        length_function=len
    )
    chunks=text_splitter.split_documents(documents)
    print(f"切分完成，共产生{len(chunks)}个小块")

    #加载模型
    print("3.正在加载嵌入模型（首次运行需下载，请耐心等待）...")
    #把文字转化为数学向量
    embeddings=HuggingFaceEmbeddings(
        model_name=r"D:\models\bge-small-zh-v1.5",            #轻量级中文嵌入模型
        model_kwargs={'device':'cpu'}           #先放在cpu跑，不吃显存
    )

    #存入库
    print("4.正在存入ChromaDB向量库...")
    #把向量和原文本存入D盘
    db=Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"向量库构建完成！文件柜（向量库）位置：{CHROMA_PATH}")

if __name__=="__main__":
    build_vector_db()
