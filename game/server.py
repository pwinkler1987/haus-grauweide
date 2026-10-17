"""Kleiner HTTP-Server (nur Standardbibliothek, keine Abhängigkeiten).

Routen:
    GET  /                 -> static/index.html (und alle anderen statischen Dateien)
    GET  /api/data         -> alle Spielinhalte als JSON
    POST /api/save         -> {"slot": "...", "state": {...}} speichern
    GET  /api/load?slot=.. -> gespeicherten Zustand laden
"""
import json
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .content import build_game_data
from .validate import validate

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"
SAVE_DIR = Path(__file__).resolve().parent / "saves"
SLOT_RE = re.compile(r"^[a-z0-9_-]{1,20}$")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    # Während der Entwicklung nichts cachen, damit Änderungen sofort sichtbar sind.
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "/api/" in self.path:
            super().log_message(fmt, *args)

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _slot_path(self, slot):
        if not slot or not SLOT_RE.match(slot):
            return None
        return SAVE_DIR / f"{slot}.json"

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/data":
            data = build_game_data()  # bei jedem Aufruf frisch geladen
            for p in validate(data):
                print(f"[Inhalt] WARNUNG: {p}")
            return self._json(data)
        if url.path == "/api/load":
            path = self._slot_path(parse_qs(url.query).get("slot", ["slot1"])[0])
            if path is None:
                return self._json({"error": "Ungültiger Slot"}, 400)
            if not path.exists():
                return self._json({"error": "Kein Spielstand"}, 404)
            return self._json(json.loads(path.read_text(encoding="utf-8")))
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/save":
            return self._json({"error": "Unbekannt"}, 404)
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            path = self._slot_path(payload.get("slot", "slot1"))
            state = payload["state"]
        except (ValueError, KeyError, TypeError):
            return self._json({"error": "Ungültige Daten"}, 400)
        if path is None:
            return self._json({"error": "Ungültiger Slot"}, 400)
        SAVE_DIR.mkdir(exist_ok=True)
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return self._json({"ok": True})


def make_server(port):
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)
