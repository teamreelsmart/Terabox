from __future__ import annotations

import re
from urllib.parse import urlparse

_ALLOWED_HOSTS = {
    "terabox.com",
    "www.terabox.com",
    "1024terabox.com",
    "www.1024terabox.com",
    "teraboxlinke.com",
    "www.teraboxlinke.com",
}

_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{8,}$")


class InvalidTeraboxLink(ValueError):
    pass



def extract_video_id(link: str) -> str:
    """Extract Terabox resource ID from /s/<id> or /v/<id> URLs."""
    parsed = urlparse(link.strip())
    if parsed.scheme not in {"http", "https"}:
        raise InvalidTeraboxLink("Invalid URL scheme")

    host = parsed.netloc.lower()
    if host not in _ALLOWED_HOSTS:
        raise InvalidTeraboxLink("Unsupported Terabox domain")

    chunks = [c for c in parsed.path.split("/") if c]
    if len(chunks) < 2 or chunks[0] not in {"s", "v"}:
        raise InvalidTeraboxLink("URL must be in /s/<id> or /v/<id> format")

    video_id = chunks[1]
    if not _ID_PATTERN.match(video_id):
        raise InvalidTeraboxLink("Invalid Terabox video ID")

    return video_id



def normalize_terabox_url(link: str) -> str:
    """Normalize any supported Terabox link to default https://1024terabox.com/s/<id>"""
    video_id = extract_video_id(link)
    return f"https://1024terabox.com/s/{video_id}"
