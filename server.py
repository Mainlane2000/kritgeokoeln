#!/usr/bin/env python3
"""Small local static-file server for the KritGeo Köln website."""

from __future__ import annotations

import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))


class WebsiteRequestHandler(BaseHTTPRequestHandler):
    """Serve files below the project root without allowing path traversal."""

    server_version = "KritGeoLocalServer/1.0"

    def do_GET(self) -> None:
        self._handle_request(send_body=True)

    def do_HEAD(self) -> None:
        self._handle_request(send_body=False)

    def _handle_request(self, send_body: bool) -> None:
        path = urlsplit(self.path).path
        if path == "/healthz":
            self._send_health_response(send_body)
            return

        file_path = self._safe_file_path(path)
        if file_path is None or not file_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Datei nicht gefunden")
            return

        try:
            content = file_path.read_bytes()
        except OSError:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Datei konnte nicht gelesen werden")
            return

        content_type, _ = mimetypes.guess_type(file_path.name)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if send_body:
            self.wfile.write(content)

    @staticmethod
    def _safe_file_path(request_path: str) -> Optional[Path]:
        relative_path = unquote(request_path).lstrip("/")
        if not relative_path:
            relative_path = "index.html"

        candidate = (ROOT / relative_path).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            return None
        return candidate

    def _send_health_response(self, send_body: bool) -> None:
        content = json.dumps({"status": "ok"}, ensure_ascii=False).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        if send_body:
            self.wfile.write(content)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), WebsiteRequestHandler)
    print(f"Website läuft unter http://{HOST}:{PORT}")
    print(f"Health-Check: http://{HOST}:{PORT}/healthz")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer wird beendet.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
