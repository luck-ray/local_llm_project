import os
import requests
from dotenv import load_dotenv

# 校验磁盘真实文件，防止VSCode未保存
with open(".env","r",encoding="utf-8") as f:
    print(".env磁盘校验:", repr(f.read()))

load_dotenv(".env", encoding="utf-8")

api_key = os.getenv("DEEPSEEK_API_KEY")
api_url = os.getenv("DEEPSEEK_BASE_URL")
model_name = os.getenv("DEEPSEEK_MODEL")

if not api_key:
    raise ValueError("DEEPSEEK_API_KEY读取失败,请检查.env")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": model_name,
    "messages": [
        {"role":"system","content":"回答尽量简洁"},
        {"role":"user","content":"简单介绍requests库"}
    ],
    "temperature":0.7,
    "max_tokens":512
}

try:
    resp = requests.post(
        url=api_url,
        headers=headers,
        json=payload,
        timeout=20
    )
    if resp.status_code == 200:
        res_data = resp.json()
        content = res_data["choices"][0]["message"]["content"]
        print("\nAI回复：\n", content)
    elif resp.status_code == 401:
        print("【401鉴权失败】密钥错误或者密钥存在空格换行")
    elif resp.status_code == 429:
        print("【429请求限流】请求太快，等待一会重试")
    else:
        print(f"请求失败 status_code:{resp.status_code}")
        print("返回详情：", resp.text)

except requests.exceptions.Timeout:
    print("【异常】请求超时，检查网络，可以切换手机热点")
except Exception as e:
    print("【未知异常】", str(e))
