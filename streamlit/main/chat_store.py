"""
会话存档：把聊天记录存成 json 文件，方便以后回看。

存到哪里？config.py 里 SAVE_DIR 指定的文件夹（默认 data/sessions/）。
文件名长这样：session_state_20261030221530.json，中间那串是保存时间。
"""

import json
import time

from config import SAVE_DIR


def save_chat(messages):
    """保存一次会话，返回保存的文件路径；没有内容就不保存，返回 None。"""
    if not messages:
        return None

    # 文件夹可能不存在（第一次运行），先建出来；parents=True 表示中间目录一起建
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    # 用"年月日时分秒"当文件名，同一秒内点了两次"新建会话"就加个序号，避免覆盖上一份
    stamp = time.strftime("%Y%m%d%H%M%S")
    path = SAVE_DIR / f"session_state_{stamp}.json"
    index = 1
    while path.exists():
        path = SAVE_DIR / f"session_state_{stamp}_{index}.json"
        index += 1

    # ensure_ascii=False 的作用：中文直接按中文写进文件，而不是 \u4f60\u597d 这种编码
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False)

    return path
