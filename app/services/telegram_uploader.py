from __future__ import annotations

from pyrogram import Client


async def send_video_or_document(client: Client, chat_id: int, file_path: str, caption: str) -> None:
    try:
        await client.send_video(chat_id=chat_id, video=file_path, caption=caption)
    except Exception:
        await client.send_document(chat_id=chat_id, document=file_path, caption=caption)
