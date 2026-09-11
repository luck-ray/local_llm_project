import requests
def local_chat(messages, temperature=0.7, max_tokens=512, max_retry=2):
    """
    LM-Studio本地聊天封装函数
    :param messages: 对话列表 [{"role":"user","content":"xxx"}]
    :param temperature: 温度
    :param max_tokens: 最大输出token
    :param max_retry: 最大重试次数
    :return: (ok:bool, content/err_msg:str)
    """
    url = "http://127.0.0.1:1234/v1/chat/completions"
    # 【重点】这里填LM‑Studio右下角API Model Identifier，不是gguf文件名
    model_name = "qwen3-8b:3"
    for attempt in range(max_retry + 1):
        try:
            payload = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            resp = requests.post(url, json=payload, timeout=60) # 本地推理慢，把25改成60
            if resp.status_code == 200:
                data = resp.json()
                ans = data["choices"][0]["message"]["content"]
                return True, ans
            else:
                err = f"status_code:{resp.status_code}, {resp.text}"
        except requests.exceptions.ConnectionError:
            err = "连接失败：检查LM‑Studio模型与API服务是否开启"
        except requests.exceptions.Timeout:
            err = "请求超时"
        except Exception as e:
            err = f"异常：{str(e)}"

        if attempt < max_retry:
            print(f"第{attempt+1}次失败，正在重试...")
    return False, err

# ========= 测试调用 =========
if __name__ == "__main__":
    msgs = [
        {"role":"system","content":"简洁回答"},
        {"role":"user","content":"简单解释什么是NGL层数"}
    ]
    ok, res = local_chat(msgs)
    if ok:
        print("本地模型输出：\n", res)
    else:
        print("出错：", res)
