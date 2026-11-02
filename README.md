# 小乌龟助手（ShelledTurtle）

一个用 Streamlit 写的 AI 聊天网页：选模型、定人设、边生成边显示，还能把聊天记录存成文件。

- **输入框在底部**，打字回车就发出去
- **左边侧栏**可以新建会话、换模型、改人设
- **回复边生成边显示**，不用等全部写完
- **点"新建会话"**会把当前对话存成 json，再清空重来

---

## 一、怎么跑起来

### 1. 装依赖（只做一次）

```bash
cd /d D:\One\educational-administration
.venv\Scripts\activate
pip install -r requirements.txt
```

> 已经建好 `.venv` 的可跳过 `activate`，直接用 `.venv\Scripts\python.exe -m streamlit run ...` 也行。

### 2. 启动本地模型（另开一个窗口，一直开着）

```bash
ollama pull deepseek-r1:1.5b
ollama serve
```

### 3. 启动网页（回到项目根目录执行）

```bash
streamlit run streamlit\main\main.py
```

浏览器打开 **http://localhost:8501** ，在底部输入框打字就能聊。

> PyCharm：打开 `streamlit/main/main.py`，右键 → Run。注意把运行配置的 **Working directory** 设成项目根目录
> `D:\One\educational-administration`，否则 `.streamlit/config.toml` 读不到（见第三节）。

---

## 二、目录结构

```
educational-administration/
├── streamlit/
│   ├── main/
│   │   ├── main.py                 # 页面：界面长什么样、按钮点了做什么（先看这个）
│   │   ├── chat_api.py             # 和大模型说话：发消息、一个字一个字收回复
│   │   ├── chat_store.py           # 存聊天记录：写成 json 文件
│   │   └── config.py               # 配置：接口地址、模型名、人设、路径（想改东西先看这里）
│   └── png/
│       ├── logo_transparent.png    # 当前使用的图标（透明底）
│       ├── logo_1.png              # 原始图（白底，留档）
│       └── logo.png                # 更早的旧图标（留档）
├── .streamlit/
│   └── config.toml                 # Streamlit 自身设置：保存代码后自动重跑
├── data/sessions/                  # 聊天记录存这里（点"新建会话"时生成 json）
├── requirements.txt                # 需要安装的库及版本
├── .gitignore
└── README.md
```

四个 Python 文件各管一件事，按 `main.py → chat_api.py / chat_store.py → config.py` 的顺序读最顺，总共约 250 行。

---

## 三、改完代码什么时候生效？

**这是最容易踩的坑**：Streamlit 每次运行都会重新读 `main.py`，但 `import` 进来的模块（`config.py`、`chat_api.py`）会被 Python 缓存在内存里，**浏览器刷新是不会重新加载的**。

本项目已在 `.streamlit/config.toml` 里打开自动重跑：

```toml
[server]
runOnSave = true
```

| 你改了什么 | 需要做什么 |
|---|---|
| `main.py` | 保存即自动重跑 |
| `config.py` / `chat_api.py` / `chat_store.py` | 保存即自动重跑（靠 `runOnSave` 清掉模块缓存） |
| `.streamlit/config.toml` 本身 | ✅ **必须重启**（只在启动时读取） |
| `requirements.txt` / 新装库 | ✅ 必须重启 |
| 新增一个文件并 `import` 它 | ✅ 第一次必须重启 |

两个注意点：

1. 自动重跑会在保存瞬间**打断正在生成的回复**，属正常现象。
2. 手动按 `R` 只对 `main.py` 有效；对 `config.py` 这类被 import 的文件，手动重跑**不清缓存**，还是得靠自动重跑或重启。

> 如果自动重跑没反应：确认启动时的工作目录是项目根目录（`.streamlit/` 按当前目录查找），
> 或在启动命令后加参数 `--server.runOnSave true`。

---

## 四、想改点东西？

全部集中在 `streamlit/main/config.py`：

| 想改什么 | 改哪里 | 当前值 |
|---|---|---|
| 网页标题 | `APP_TITLE` | `"小乌龟助手"` |
| 模型接口地址 | `API_URL` | `http://localhost:11434/v1/chat/completions` |
| 云端密钥 | `API_KEY` | 空（本机 ollama 不需要） |
| 下拉框能选哪些模型 | `MODELS` | `["deepseek-r1:1.5b", "deepseek-flash"]` |
| 默认人设 | `DEFAULT_PROMPT` | 高中语文老师 |
| 超时时间（秒） | `TIMEOUT` | `120` |
| 图标 | `PNG_PATH` | `streamlit/png/logo_transparent.png` |
| 聊天记录存哪 | `SAVE_DIR` | `data/sessions/` |

其他：

- **界面布局、按钮文字** → `main.py`
- **请求参数**（比如加 `temperature`）→ `chat_api.py` 的 `ask_model()` 里的 `json={...}`
- **换图标** → 把新图放进 `streamlit/png/`，改 `config.py` 的 `PNG_PATH`。**要用透明底 PNG**，白底图会在深色侧边栏上显示成一个白方块。

换云端模型（以 DeepSeek 官网为例）：

```python
API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = "sk-你的密钥"
MODELS  = ["deepseek-chat"]
```

---

## 五、聊天记录

- 位置：`data/sessions/`，文件名形如 `session_state_20261102180900.json`
- 时机：点"新建会话"时，**先存盘再清空**
- 内容：`[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`
- 同一秒内点两次不会覆盖，会自动加 `_1`、`_2` 后缀

---

## 六、常见问题

**页面显示"连接模型失败：..."**
→ 多半是 ollama 没启动。另开窗口执行 `ollama serve`，再刷新页面。

**页面显示"模型返回了错误 404"**
→ `MODELS` 里的名字本地没有。执行 `ollama list` 看实际有哪些，照着改 `config.py`。

**第一次回复特别慢**
→ 首次调用要把模型加载进内存，慢是正常的。慢到超时可以调大 `TIMEOUT`。

**侧栏图标是个白方块**
→ 图是白底 JPG/PNG，没有透明通道。`st.logo()` 只负责显示，不会帮你抠背景。

**端口 8501 已被占用**
→ 有另一个 Streamlit 还开着。关掉它，或换端口：`streamlit run streamlit\main\main.py --server.port 8502`。

**改了 `config.py` 页面没变**
→ 见第三节：需要 `runOnSave` 生效或重启。

---

## 七、代码里的两个小坑（已修好，记一下防复发）

1. **`st.session_state.messages` 必须最先初始化**。写在侧边栏后面的话，第一次点"新建会话"就会
   `AttributeError: st.session_state has no attribute "messages"`。
2. **`st.text_area` 留空返回的是 `""`，不是 `None`**。判断"用户没填"要用 `not 内容.strip()`；
   写成 `if 内容 is None` 永远不成立，默认人设就永远不会生效。

另外两个原始版本遗留的问题也已处理：请求写死了模型名（下拉框形同虚设）、`requests.post` 没有 `timeout`。

---

## 八、依赖

| 库 | 版本 | 用途 |
|---|---|---|
| streamlit | 1.66.1 | 网页框架 |
| requests | 2.34.2 | 调模型接口 |

Python 3.10+ 可用，本项目在 3.14.8 上验证。
