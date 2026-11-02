"""
聊天接口：负责"和大模型说话"。
一共三个函数：
    build_messages()  把「人设 + 聊天记录」拼成接口要的格式
    ask_model()       把请求发出去（返回还没读完的响应，边读边显示）
    read_reply()      把流式返回一行行拆开，每次产出一小段文字

为什么单独放一个文件？以后想换模型服务商，只改这里，不用动页面代码。
"""

import json

import requests

from config import API_KEY, API_URL, TIMEOUT


def build_messages(system_prompt, history):
    """拼接发给模型的消息列表：第一条是 system（人设），后面是聊天记录。"""
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(history)
    return messages


def ask_model(model, system_prompt, history):
    """发送请求，返回 requests 的响应对象。

    stream=True 表示"边生成边返回"，不用等模型全部写完，所以能一个字一个字显示。
    """
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    return requests.post(
        API_URL,
        headers=headers,
        json={
            "model": model,
            "messages": build_messages(system_prompt, history),
            "stream": True,
        },
        stream=True,
        timeout=TIMEOUT,
    )


def read_reply(response):
    """逐行读取流式返回，把每一小段文字 yield 出去（供页面边收边显示）。

    模型返回的数据长这样，每行一条：
        data: {"choices":[{"delta":{"content":"你"}}]}
        data: {"choices":[{"delta":{"content":"好"}}]}
        data: [DONE]
    空行、其他行都跳过，遇到 [DONE] 表示说完了。
    """
    for raw_line in response.iter_lines():
        if not raw_line:
            continue

        line = raw_line.decode("utf-8")
        if not line.startswith("data:"):
            continue

        # 去掉开头的 "data:"（5 个字符）和首尾空格
        data = line[5:].strip()
        if data == "[DONE]":
            break

        chunk = json.loads(data)
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content:
            yield content
