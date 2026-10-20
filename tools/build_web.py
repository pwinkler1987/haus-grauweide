"""Baut das Spiel als statische Seite nach www/ (für die iOS- und Android-App).

    python tools/build_web.py [--release]

Kopiert static/ und schreibt die Python-Inhalte als www/data.json (Deutsch)
sowie www/data.<sprache>.json für jede Übersetzung in game/content/lang/.
Ohne --release zeigt die App nur Test-Werbung von Google.
Bricht ab, wenn validate() Probleme findet.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from game.content import build_game_data  # noqa: E402
from game.content.i18n import LANGUAGES, translate  # noqa: E402
from game.validate import validate  # noqa: E402

OUT = ROOT / "www"


def main():
    data = build_game_data()
    problems = validate(data)
    for p in problems:
        print(f"[Inhalt] FEHLER: {p}")
    translations = {}
    for lang in LANGUAGES:
        translations[lang], missing = translate(data, lang)
        for text in missing:
            problems.append(f"Übersetzung ({lang}) fehlt: {text[:70]!r}")
            print(f"[Inhalt] FEHLER: {problems[-1]}")
    if problems:
        sys.exit(1)
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)
    if "--release" in sys.argv[1:]:
        (OUT / "js" / "engine" / "ads-config.js").write_text("export const TEST_ADS = false;\n", encoding="utf-8")
    for name, content in [("data.json", data)] + [(f"data.{k}.json", v) for k, v in translations.items()]:
        (OUT / name).write_text(json.dumps(content, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    kind = "Release" if "--release" in sys.argv[1:] else "Test-Werbung"
    print(f"Gebaut: {OUT.relative_to(ROOT)}/ ({len(data['rooms'])} Räume, {kind})")


if __name__ == "__main__":
    main()
