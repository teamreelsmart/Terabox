from __future__ import annotations

import logging
import sys

from pyrogram import Client

from app.config import ConfigError, get_settings
from app.services.keep_alive import start_keep_alive_server
from app.utils.logger import setup_logger

# Import handlers to register decorator callbacks.
from app.bot import handlers as _handlers  # noqa: F401


setup_logger()
logger = logging.getLogger(__name__)


def _load_settings_or_exit():
    try:
        return get_settings()
    except ConfigError as exc:
        logger.error("Configuration error: %s", exc)
        logger.error(
            "Set required env vars on Render: API_ID, API_HASH, BOT_TOKEN, XAPIVERSE_KEY"
        )
        sys.exit(1)


settings = _load_settings_or_exit()
start_keep_alive_server()

app = Client(
    "terabox_bot",
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    bot_token=settings.bot_token,
)


if __name__ == "__main__":
    app.run()
