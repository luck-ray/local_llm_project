from dotenv import load_dotenv
import os

res=load_dotenv()
print("是否加载到env文件:",res)
test_val=os.getenv("TEST")
print("测试环境变量读取：",test_val)