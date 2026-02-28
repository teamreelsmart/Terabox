from __future__ import annotations

from pyrogram import Client

from app.config import get_settings
from app.utils.logger import setup_logger
from app.services.keep_alive import start_keep_alive_server

# Import handlers to register decorator callbacks.
from app.bot import handlers as _handlers  # noqa: F401


settings = get_settings()
setup_logger()
start_keep_alive_server()

app = Client(
    "terabox_bot",
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    bot_token=settings.bot_token,
)


if __name__ == "__main__":
    app.run()
