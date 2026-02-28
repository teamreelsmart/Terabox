from __future__ import annotations

import logging
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

logger = logging.getLogger(__name__)


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/", "/health", "/ping"}:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def _start_http_server(port: int) -> None:
    server = HTTPServer(("0.0.0.0", port), _HealthHandler)
    logger.info("Keep-alive health server started on port %s", port)
    server.serve_forever()


def _self_ping_loop(url: str, interval_seconds: int) -> None:
    logger.info("Self-ping started for URL: %s", url)
    while True:
        try:
            requests.get(url, timeout=20)
            logger.info("Self-ping success")
        except Exception as exc:
            logger.warning("Self-ping failed: %s", exc)
        time.sleep(interval_seconds)


def start_keep_alive_server() -> None:
    port = int(os.getenv("PORT", "8080"))
    server_thread = threading.Thread(target=_start_http_server, args=(port,), daemon=True)
    server_thread.start()

    keep_alive_url = os.getenv("KEEP_ALIVE_URL", "").strip()
    if keep_alive_url:
        interval = int(os.getenv("KEEP_ALIVE_INTERVAL", "300"))
        ping_thread = threading.Thread(
            target=_self_ping_loop,
            args=(keep_alive_url, interval),
            daemon=True,
        )
        ping_thread.start()
