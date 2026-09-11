import requests

local_url = "http://127.0.0.1:1234/v1/chat/completions"

payload = {
    "model": "qwen3-8b:3",
    "messages": [
        {"role": "user", "content": "帮我看一下明天的天气预报"}
    ],
    "temperature": 0.7,
    "stream": False
}

try:
    resp = requests.post(local_url, json=payload, timeout=120)
    if resp.status_code == 200:
        res_data = resp.json()
        print("本地模型回复：\n", res_data["choices"][0]["message"]["content"])
    else:
        print(f"请求失败 {resp.status_code}")
        print(resp.text)
except requests.exceptions.ConnectionError:
    print("【连接失败】确认LM-Studio已经加载模型并且开启本地API服务")
except requests.exceptions.Timeout:
    print("【超时】本地推理时间过长,可调大timeout")
except Exception as e:
    print("异常：", str(e))
