# 小乌龟助手（ShelledTurtle）

小乌龟助手是一个基于 [Streamlit](https://streamlit.io/) 的轻量 AI 聊天网页。它通过 OpenAI 兼容的 Chat Completions 接口调用模型，默认连接本机的 Ollama；支持选择模型、设置 system prompt，并以流式方式显示回复。点击“新建会话”时，当前非空对话会保存为 JSON 文件。

## 功能

- 选择配置好的模型，并与模型进行多轮对话
- 自定义 system prompt；留空时使用默认人设
- 流式显示模型回复
- 将当前对话保存到本地 JSON 文件
- 通过配置文件修改模型服务、模型列表和应用设置

## 环境要求

- Python 3.10 或更高版本
- Ollama，或其他兼容 OpenAI Chat Completions API 的模型服务

## 快速开始（本机 Ollama）

### 1. 获取项目并安装依赖

```bash
git clone <仓库地址>
cd educational-administration
python -m venv .venv
```

激活虚拟环境：

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

安装依赖：

```bash
python -m pip install -r requirements.txt
```

### 2. 启动 Ollama 并准备模型

确保 Ollama 已安装并正在运行，然后下载一个模型。例如：

```bash
ollama pull qwen3:8b
```

默认模型列表在 `streamlit/main/config.py` 的 `MODELS` 中配置。请确保列表里的模型已下载，并且当前 Ollama 服务支持它们。

### 3. 启动网页

在项目根目录运行：

```bash
python -m streamlit run streamlit/main/main.py
```

Streamlit 会在终端显示本地地址，通常是 <http://localhost:8501>。打开该地址即可开始聊天。

## 配置

应用配置集中在 [`streamlit/main/config.py`](streamlit/main/config.py)：

| 配置项 | 用途 |
| --- | --- |
| `APP_TITLE` | 页面标题 |
| `API_URL` | 模型服务的 Chat Completions 接口地址，默认是本机 Ollama 地址 |
| `API_KEY` | 可选的 Bearer API key；本机 Ollama 通常留空 |
| `MODELS` | 页面模型选择框中的模型名称 |
| `DEFAULT_PROMPT` | 用户没有填写自定义 system prompt 时使用的默认提示词 |
| `TIMEOUT` | HTTP 请求超时时间（秒） |
| `PNG_PATH` | 应用图标文件路径 |
| `SAVE_DIR` | 会话 JSON 文件的保存目录 |

使用云端或其他兼容服务时，请将 `API_URL` 设置为服务提供的接口地址，按需填写 `API_KEY`，并将 `MODELS` 改成服务支持的模型名称。请勿将真实密钥提交到公开仓库；建议在本地配置并确认 Git 不会跟踪包含密钥的文件。

## 项目结构

```text
.
├── .streamlit/
│   └── config.toml          # Streamlit 设置（包含保存后自动重跑）
├── data/
│   └── sessions/            # 会话 JSON 文件的默认保存目录
├── streamlit/
│   ├── main/
│   │   ├── main.py          # 页面布局、输入处理和聊天流程
│   │   ├── chat_api.py      # 构造请求并读取流式模型回复
│   │   ├── chat_store.py    # 保存会话记录
│   │   └── config.py        # 应用配置
│   └── png/                 # 应用图标
├── requirements.txt         # Python 运行依赖
└── README.md
```

## 会话保存说明

点击“新建会话”时，如果当前对话有消息，应用会将消息列表写入 `data/sessions/` 下的 JSON 文件，然后清空当前页面会话。空会话不会生成文件。文件名带有保存时间；如果同一秒内发生重名，会自动添加序号以避免覆盖。

这些文件保存在本地，当前应用没有提供历史会话浏览或重新载入界面。请根据自己的需要管理或备份 `data/sessions/` 中的文件。

## 开发说明

项目根目录的 `.streamlit/config.toml` 设置了 `server.runOnSave = true`，保存代码后 Streamlit 会自动重跑。修改配置文件或依赖后，如果页面没有反映变化，请停止并重新启动应用。

主要代码阅读顺序：

1. `streamlit/main/main.py`：了解页面如何处理输入、会话状态和回复显示。
2. `streamlit/main/chat_api.py`：了解请求消息格式和流式响应解析。
3. `streamlit/main/chat_store.py`：了解 JSON 会话文件的保存方式。
4. `streamlit/main/config.py`：查看可调整的应用配置。

## 常见问题

**无法连接模型服务**

确认 Ollama 或其他模型服务已启动，并检查 `API_URL` 是否正确。

**模型返回 404 或提示模型不存在**

检查 `MODELS` 中的名称是否与模型服务中的名称一致。使用 Ollama 时，可以运行 `ollama list` 查看已下载的模型。

**回复超时**

首次调用模型可能需要加载模型。若服务响应时间较长，可在 `config.py` 中增加 `TIMEOUT`。

**端口 8501 已被占用**

使用其他端口启动，例如：

```bash
python -m streamlit run streamlit/main/main.py --server.port 8502
```

## 依赖

项目运行依赖见 [`requirements.txt`](requirements.txt)：Streamlit 和 Requests。
