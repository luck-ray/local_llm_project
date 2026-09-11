import os
import requests
from dotenv import load_dotenv

# 读取 .env 文件
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")

LOCAL_URL = os.getenv("LOCAL_URL")
LOCAL_MODEL = os.getenv("LOCAL_MODEL")


def ask_cloud(prompt):
    """云端 DeepSeek API 调用函数"""
    url = f"{DEEPSEEK_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "你是一个有用的助手"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            res_data = resp.json()
            return res_data["choices"][0]["message"]["content"]
        elif resp.status_code == 401:
            return "【401权限失败】密钥错误或过期"
        elif resp.status_code == 429:
            return "【429请求限流】请求太快，请稍等"
        else:
            return f"请求失败，状态码: {resp.status_code}"
    except requests.exceptions.Timeout:
        return "【异常】请求超时，请检查网络"
    except Exception as e:
        return f"【未知异常】{str(e)}"


def ask_local(prompt):
    """本地 LM-Studio API 调用函数"""
    payload = {
        "model": LOCAL_MODEL,
        "messages": [
            {"role": "system", "content": "你是一个有用的助手"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": False
    }

    try:
        resp = requests.post(LOCAL_URL, json=payload, timeout=80)
        if resp.status_code == 200:
            res_data = resp.json()
            return res_data["choices"][0]["message"]["content"]
        else:
            return f"本地请求失败，状态码: {resp.status_code}"
    except requests.exceptions.ConnectionError:
        return "【连接失败】确认 LM-Studio 已加载模型且已开启本地 API 服务（端口 1234）"
    except requests.exceptions.Timeout:
        return "【超时】本地推理时间过长，请检查显存或降低 max_tokens"
    except Exception as e:
        return f"【未知异常】{str(e)}"