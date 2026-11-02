"""
配置文件：程序里所有"你可能想改的地方"都集中在这里。
改完保存，重启程序（Ctrl+C 后重新 streamlit run）就生效。

新手提示：这个文件里没有任何逻辑，只是把常量和路径集中声明，方便查找。
"""

from pathlib import Path

# ---------- 路径 ----------
# __file__ 是当前文件；parents[0] 是 main/ 目录，parents[1] 是 streamlit/，parents[2] 是项目根目录
# 用这种写法，项目复制到别的电脑、别的盘符也能找到文件，不用改代码
BASE_DIR = Path(__file__).resolve().parents[2]
PNG_PATH = BASE_DIR / "streamlit" / "png" / "logo_transparent.png"
SAVE_DIR = BASE_DIR / "data" / "sessions"

# ---------- 界面文字 ----------
APP_TITLE = "小乌龟助手"

# ---------- 模型接口 ----------
# 本机 ollama 的地址（先装 ollama，再 ollama pull deepseek-r1:1.5b，然后 ollama serve）
API_URL = "http://localhost:11434/v1/chat/completions"

# 如果用云端（比如 DeepSeek 官网），把 API_URL 改成 "https://api.deepseek.com/v1/chat/completions"
# 再把 API_KEY 填上；本机 ollama 不需要 key，留空即可
API_KEY = ""

# 下拉框里能选的模型。要和上面 API_URL 支持的名字对上
MODELS = ["deepseek-r1:1.5b", "deepseek-flash"]

# 用户不填"模型参数"时用的默认人设
DEFAULT_PROMPT = (
    "你是一个有10年教学经验的高中语文老师，擅长教授高中语文课程，"
    "擅长使用深度求索的模型进行教学。"
)

# 超时时间（秒）。不设置的话，模型服务卡住时页面会一直转圈，只能杀进程
TIMEOUT = 120
