import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH, override=False)

STYLE_PROMPTS = {
    "默认": "",
    "电影感": "画面更具电影感，光影层次更丰富，色调克制高级，整体更像精致电影剧照。",
    "清新": "画面明亮、通透、轻盈，色彩自然清新，观感干净舒服。",
    "科技感": "画面更现代、更科技感，质感更锐利，氛围简洁，适合展示型视觉。",
    "海报感": "画面更像高质量宣传海报，主体突出，构图稳定，视觉更有冲击力。"
}

# 前端显示的比例选项
SIZE_OPTIONS = ["1:1", "4:3", "3:4", "16:9", "9:16"]

# 映射到 Seedream 现在接受的 WIDTHxHEIGHT
SIZE_MAP = {
    "1:1": "1024x1024",
    "4:3": "1536x1152",
    "3:4": "1152x1536",
    "16:9": "1792x1024",
    "9:16": "1024x1792",
    "1k": "1k",
    "2k": "2k",
    "4k": "4k",
}

def normalize_size(size: str) -> str:
    if not size:
        return "1024x1024"

    size = str(size).strip().lower()
    return SIZE_MAP.get(size, size)

def get_settings():
    return {
        "ark_api_key": os.getenv("ARK_API_KEY", "").strip(),
        "ark_base_url": os.getenv(
            "ARK_BASE_URL",
            "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        ).strip(),
        "ark_model": os.getenv(
            "ARK_MODEL",
            "doubao-seedream-4-0-250828"
        ).strip(),
        "app_host": os.getenv("APP_HOST", "127.0.0.1").strip(),
        "app_port": int(os.getenv("APP_PORT", "7860")),
        "output_dir": os.getenv("OUTPUT_DIR", "outputs").strip(),
        "request_timeout": int(os.getenv("REQUEST_TIMEOUT", "240"))
    }