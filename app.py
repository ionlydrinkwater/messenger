#!/usr/bin/env python3
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
MESSAGES = []


def send_json(handler, payload, status=200):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self.serve_file("templates/index.html")
            return

        if path == "/messages":
            send_json(self, {"messages": MESSAGES})
            return

        if path.startswith("/static/"):
            self.serve_file(str(BASE_DIR / path.lstrip("/")))
            return

        if path == "/health":
            send_json(self, {"status": "ok"})
            return

        self.send_error(404, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/send":
            self.send_error(404, "Not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0

        raw = self.rfile.read(length) if length > 0 else b""
        try:
            data = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError:
            send_json(self, {"error": "Invalid JSON body"}, 400)
            return

        name = str(data.get("name", "")).strip()
        message = str(data.get("message", "")).strip()

        if not name or not message:
            send_json(self, {"error": "Name and message are required"}, 400)
            return

        if len(name) > 50 or len(message) > 500:
            send_json(self, {"error": "Name or message is too long"}, 400)
            return

        MESSAGES.append(
            {
                "id": len(MESSAGES) + 1,
                "name": name,
                "message": message,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            }
        )

        send_json(self, {"ok": True, "messages": MESSAGES})

    def serve_file(self, relative_path):
        file_path = Path(relative_path)
        if not file_path.is_absolute():
            file_path = BASE_DIR / file_path

        if not file_path.exists():
            self.send_error(404, "Not found")
            return

        content = file_path.read_bytes()
        mime = self.get_content_type(file_path)

        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def get_content_type(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
        }
        return types.get(suffix, "application/octet-stream")

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    print(f"Chat app running at http://{host}:{port}")
    print("Open the URL in a browser to use it.")
    server = ThreadingHTTPServer((host, port), ChatHandler)
    server.serve_forever()
