"""Baut das Spiel als statische Seite nach www/ (für die iOS- und Android-App).

    python tools/build_web.py

Kopiert static/ und schreibt die Python-Inhalte als www/data.json.
Bricht ab, wenn validate() Probleme findet.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from game.content import build_game_data  # noqa: E402
from game.validate import validate  # noqa: E402

OUT = ROOT / "www"


def main():
    data = build_game_data()
    problems = validate(data)
    for p in problems:
        print(f"[Inhalt] FEHLER: {p}")
    if problems:
        sys.exit(1)
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)
    (OUT / "data.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Gebaut: {OUT.relative_to(ROOT)}/ ({len(data['rooms'])} Räume)")


if __name__ == "__main__":
    main()
