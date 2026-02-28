from __future__ import annotations

import os
import subprocess
from pathlib import Path

from app.config import Settings


class DownloadError(RuntimeError):
    pass


class Downloader:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def download_m3u8_to_mp4(self, m3u8_url: str, output_name: str) -> Path:
        os.makedirs(self._settings.temp_dir, exist_ok=True)
        output_path = Path(self._settings.temp_dir) / output_name

        copy_cmd = [
            self._settings.ffmpeg_bin,
            "-y",
            "-i",
            m3u8_url,
            "-c",
            "copy",
            str(output_path),
        ]
        if self._run(copy_cmd):
            return output_path

        transcode_cmd = [
            self._settings.ffmpeg_bin,
            "-y",
            "-i",
            m3u8_url,
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-preset",
            "veryfast",
            str(output_path),
        ]
        if self._run(transcode_cmd):
            return output_path

        raise DownloadError("ffmpeg failed for both remux and transcode modes")

    @staticmethod
    def _run(cmd: list[str]) -> bool:
        process = subprocess.run(cmd, capture_output=True, text=True)
        return process.returncode == 0
