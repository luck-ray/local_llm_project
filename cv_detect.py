from ultralytics import YOLO
from pathlib import Path
from query_kb import ask_rag
from fastapi import UploadFile
import shutil
import os

#定义上传文件夹
UPLOAD_DIR="static/uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)       #不存在就自动创建

BASE_DIR=Path(__file__).resolve().parent
MODEL_PATH=BASE_DIR/"models"/"yolov8n.pt"
#加载模型
print("正在加载YOLO模型...")
model=YOLO(str(MODEL_PATH))

def process_image(image_path):
    """接收图片路径，返回YOLO识别结果和RAG建议"""
    #把图片喂给模型
    print(f"正在识别图片：{image_path}")
    results=model(image_path)       #改用传入的路径

    #提取识别结果
    detected_objects=[]     #建一个空篮子，装识别出来的东西
    for result in results:
        for box in result.boxes:
            class_id=int(box.cls[0])
            label=model.names[class_id]
            detected_objects.append(label)      #把标签放进篮子里

    #如果检测到没有东西
    if not detected_objects:
        return{"cv_result":[],"rag_answer":"图片中未识别到任何物体。"}
    
    #拼接RAG
    unique_objects=list(set(detected_objects))      #去重，比如两个只留一个
    cv_query=f"图片中检测到了：{','.join(unique_objects)}。请根据知识库，给出处理建议。"
    print(f"RAG提问：{cv_query}")

   #调用RAG系统
    rag_answer=ask_rag(cv_query,model="cloud")
    
    #用return返回一个字典给网页
    return {
        "cv_result":unique_objects,
        "rag_answer":rag_answer
    }

    #测试函数
if __name__=="__main__":
    test_result=process_image("data/data_test/test_image.jpg")
    print("\n--- 测试结果 ---")
    print(f"识别到：{test_result['cv_result']}")
    print(f"RAG建议：{test_result['rag_answer']}")
