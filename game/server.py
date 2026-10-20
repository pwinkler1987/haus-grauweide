"""Kleiner HTTP-Server für die Entwicklung (nur Standardbibliothek).

Routen:
    GET /           -> static/index.html (und alle anderen statischen Dateien)
    GET /data.json  -> alle Spielinhalte als JSON, bei jedem Aufruf frisch gebaut
    GET /data.en.json -> dieselben Inhalte übersetzt (game/content/lang/en.json)

Spielstände liegen im Browser bzw. in der App auf dem Gerät, nicht hier.
Für die Apps schreibt tools/build_web.py dieselben Daten als Datei nach www/.
"""
import json
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .content import build_game_data
from .content.i18n import LANGUAGES, translate
from .validate import validate

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    # Während der Entwicklung nichts cachen, damit Änderungen sofort sichtbar sind.
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "data." in self.path:
            super().log_message(fmt, *args)

    def do_GET(self):
        m = re.fullmatch(r"/data(?:\.(\w+))?\.json", urlparse(self.path).path)
        if m and (m[1] is None or m[1] in LANGUAGES):
            data = build_game_data()
            for p in validate(data):
                print(f"[Inhalt] WARNUNG: {p}")
            if m[1]:
                data, missing = translate(data, m[1])
                for text in missing:
                    print(f"[Inhalt] WARNUNG: Übersetzung ({m[1]}) fehlt: {text[:70]!r}")
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


def make_server(port):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)
