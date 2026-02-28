from __future__ import annotations

import uuid
from functools import lru_cache

from pyrogram import Client, filters
from pyrogram.types import Message

from app.config import get_settings
from app.services.cleanup import safe_remove
from app.services.downloader import DownloadError, Downloader
from app.services.telegram_uploader import send_video_or_document
from app.services.terabox_api import TeraboxApiClient, TeraboxApiError
from app.utils.validators import InvalidTeraboxLink, normalize_terabox_url


@lru_cache(maxsize=1)
def _runtime() -> tuple:
    settings = get_settings()
    return settings, TeraboxApiClient(settings), Downloader(settings)


@Client.on_message(filters.private & filters.command("start"))
async def start_handler(_: Client, message: Message) -> None:
    from app.bot.messages import START_TEXT

    await message.reply_text(START_TEXT)


@Client.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def link_handler(client: Client, message: Message) -> None:
    text = (message.text or "").strip()

    try:
        normalized_url = normalize_terabox_url(text)
    except InvalidTeraboxLink:
        await message.reply_text("❌ Invalid Terabox link. Send /s/<id> ya /v/<id> format link.")
        return

    settings, api_client, downloader = _runtime()
    status = await message.reply_text("⏳ Link resolve ho raha hai...")
    output_path = None

    try:
        stream = api_client.resolve(normalized_url, settings.default_quality)
        await status.edit_text(f"📥 Downloading ({stream.quality})...")

        output_name = f"{uuid.uuid4().hex}.mp4"
        output_path = downloader.download_m3u8_to_mp4(stream.m3u8_url, output_name)

        await status.edit_text("📤 Upload ho raha hai Telegram par...")
        caption = f"{stream.title}\nQuality: {stream.quality}"
        await send_video_or_document(client, message.chat.id, str(output_path), caption)
        await status.edit_text("✅ Done")
    except (TeraboxApiError, DownloadError) as err:
        await status.edit_text(f"❌ Failed: {err}")
    except Exception:
        await status.edit_text("❌ Unexpected error. Please retry.")
    finally:
        if output_path:
            safe_remove(output_path)
