from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    bot_token: str
    xapiverse_api_url: str
    xapiverse_key: str
    temp_dir: str = "./temp"
    default_quality: str = "480p"
    request_timeout: int = 45
    ffmpeg_bin: str = "ffmpeg"
    max_concurrent_jobs: int = 2



def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value



def get_settings() -> Settings:
    return Settings(
        api_id=int(_require("API_ID")),
        api_hash=_require("API_HASH"),
        bot_token=_require("BOT_TOKEN"),
        xapiverse_api_url=os.getenv("XAPIVERSE_API_URL", "https://xapiverse.com/api/terabox-pro"),
        xapiverse_key=_require("XAPIVERSE_KEY"),
        temp_dir=os.getenv("TEMP_DIR", "./temp"),
        default_quality=os.getenv("DEFAULT_QUALITY", "480p"),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "45")),
        ffmpeg_bin=os.getenv("FFMPEG_BIN", "ffmpeg"),
        max_concurrent_jobs=int(os.getenv("MAX_CONCURRENT_JOBS", "2")),
    )
