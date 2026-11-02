"""
ShelledTurtle —— 一个和 AI 聊天的网页。

运行方式（在项目根目录执行）：
    streamlit run streamlit/main/main.py

只有这一个文件是"页面"，它负责显示界面、接收输入。
真正干活的两个帮手在隔壁：
    chat_api.py    负责和大模型说话
    chat_store.py  负责把聊天记录存成文件

读代码小提示：Streamlit 的规则是「每次操作，整个文件从头再跑一遍」。
所以聊天记录必须放在 st.session_state 里，否则一刷新就丢了。
"""

import streamlit as st

from chat_api import ask_model, read_reply
from chat_store import save_chat
from config import APP_TITLE, DEFAULT_PROMPT, MODELS, PNG_PATH

# ============================================================ 1. 页面基本设置
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=str(PNG_PATH) if PNG_PATH.exists() else "🐢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://chat.deepseek.com/",
        "Report a bug": "https://chat.deepseek.com/",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

st.title(APP_TITLE)
st.logo(str(PNG_PATH))

# ============================================================ 2. 准备聊天记录
# 第一次打开页面时还没有这个变量，先建一个空列表。
# 注意：一定要写在侧边栏之前！否则下面点"新建会话"时会报错说找不到 messages。
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================ 3. 侧边栏
with st.sidebar:
    st.subheader(APP_TITLE)

    if st.button("新建会话", width="stretch"):
        save_path = save_chat(st.session_state.messages)  # 先把当前对话存成文件
        st.session_state.messages = []                    # 再清空，开始新的一轮
        if save_path:
            print(f"已保存到：{save_path}")
        st.rerun()                                        # 让页面重新画一遍

    model = st.selectbox("选择模型", MODELS)

    # 用户填的"模型参数"其实就是人设（system 提示词）。
    # 留空时用 config.py 里的默认人设——这里的 or 就是为了处理这种情况。
    user_prompt = st.text_area("请定义模型的参数", height=140)
    system_prompt = user_prompt.strip() or DEFAULT_PROMPT

    st.caption("当前人设：" + ("自定义" if user_prompt.strip() else "默认（高中语文老师）"))

# ============================================================ 4. 把历史消息画出来
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# ============================================================ 5. 处理这次输入
prompt = st.chat_input("请输入:")
if prompt:
    # 先把用户这句话显示出来，并存进聊天记录
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()  # 先占个位置，回复会一点点填进去
        reply = ""

        try:
            response = ask_model(model, system_prompt, st.session_state.messages)
        except Exception as e:
            # 网络断了、ollama 没启动，都会走到这里。给句人话，别让页面白屏
            st.error(f"连接模型失败：{e}")
            response = None

        if response is not None:
            if response.status_code != 200:
                st.error(f"模型返回了错误 {response.status_code}：{response.text[:200]}")
            else:
                try:
                    for piece in read_reply(response):
                        reply += piece
                        placeholder.markdown(reply)
                except Exception as e:
                    st.error(f"读取回复时出错：{e}")

        if not reply:
            placeholder.write("（这次没有收到内容）")

    # 只有真的收到内容才存进记录，避免聊天记录里出现空回复
    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
