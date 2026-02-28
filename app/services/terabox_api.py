from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

from app.config import Settings


@dataclass
class StreamInfo:
    title: str
    m3u8_url: str
    quality: str
    size_formatted: str | None = None
    duration: str | None = None


class TeraboxApiError(RuntimeError):
    pass


class TeraboxApiClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def resolve(self, normalized_url: str, preferred_quality: str) -> StreamInfo:
        payload = {"url": normalized_url}
        headers = {
            "Content-Type": "application/json",
            "xAPIverse-Key": self._settings.xapiverse_key,
        }

        response = requests.post(
            self._settings.xapiverse_api_url,
            json=payload,
            headers=headers,
            timeout=self._settings.request_timeout,
        )
        response.raise_for_status()

        data: dict[str, Any] = response.json()
        if data.get("status") != "success":
            raise TeraboxApiError("API returned non-success status")

        files = data.get("list")
        if not isinstance(files, list) or not files:
            raise TeraboxApiError("No media file found in API response")

        item = files[0]
        if not isinstance(item, dict):
            raise TeraboxApiError("Invalid media file format")

        m3u8_url, quality = self._select_stream(item, preferred_quality)
        title = str(item.get("name") or "terabox_video.mp4")

        return StreamInfo(
            title=title,
            m3u8_url=m3u8_url,
            quality=quality,
            size_formatted=item.get("size_formatted"),
            duration=item.get("duration"),
        )

    def _select_stream(self, item: dict[str, Any], preferred_quality: str) -> tuple[str, str]:
        fast_streams = item.get("fast_stream_url")
        if isinstance(fast_streams, dict) and fast_streams:
            if preferred_quality in fast_streams:
                return str(fast_streams[preferred_quality]), preferred_quality

            ranked = sorted(
                (
                    (key, str(url))
                    for key, url in fast_streams.items()
                    if isinstance(url, str)
                ),
                key=lambda x: _quality_rank(x[0]),
                reverse=True,
            )
            if ranked:
                return ranked[0][1], ranked[0][0]

        stream_url = item.get("stream_url")
        if isinstance(stream_url, str) and stream_url:
            return stream_url, "stream_url"

        raise TeraboxApiError("No playable stream URL available")


def _quality_rank(label: str) -> int:
    digits = "".join(ch for ch in label if ch.isdigit())
    return int(digits) if digits else 0
