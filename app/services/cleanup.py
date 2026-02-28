from __future__ import annotations

from pathlib import Path


def safe_remove(path: str | Path) -> None:
    p = Path(path)
    if p.exists() and p.is_file():
        p.unlink(missing_ok=True)
