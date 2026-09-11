import os
import requests
from dotenv import load_dotenv

load_dotenv(r"D:\ai_work\local_llm_project\.env", encoding="utf-8")

api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = os.getenv("DEEPSEEK_BASE_URL")
model_name = os.getenv("DEEPSEEK_MODEL")

messages = []
print("开始对话,输入exit退出")

while True:
    user_text = input("你：")
    if user_text.strip() == "exit":
        break
    messages.append({"role":"user","content":user_text})
    payload = {
        "model": model_name,
        "messages": messages,
        "temperature":0.7
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    res = requests.post(api_url,json=payload,headers=headers,timeout=120)
    res_data = res.json()
    ans = res_data["choices"][0]["message"]["content"]
    print(f"AI:{ans}\n")
    messages.append({"role":"assistant","content":ans})

