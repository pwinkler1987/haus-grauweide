"""Das Haus Grauweide – Startpunkt.

Startet einen lokalen Webserver und öffnet das Spiel im Browser:

    python main.py            # http://localhost:8000
    python main.py --port 8080 --no-browser
"""
import argparse
import threading
import webbrowser

from game.content import build_game_data
from game.server import make_server
from game.validate import validate


def main():
    parser = argparse.ArgumentParser(description="Das Haus Grauweide")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true", help="Browser nicht automatisch öffnen")
    args = parser.parse_args()

    problems = validate(build_game_data())
    for p in problems:
        print(f"[Inhalt] WARNUNG: {p}")
    if not problems:
        print("[Inhalt] Alle Räume und Gegenstände sind in Ordnung.")

    server = make_server(args.port)
    url = f"http://localhost:{args.port}/"
    print(f"Das Haus Grauweide läuft auf {url}  (Beenden mit Strg+C)")
    if not args.no_browser:
        threading.Timer(0.6, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBis zum nächsten Mal!")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
