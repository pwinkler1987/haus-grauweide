"""Trägt neue Spieltexte in die Übersetzungsdateien ein.

    python tools/i18n.py

Für jede Sprache in game/content/i18n.LANGUAGES werden fehlende deutsche Texte
mit leerem Wert in game/content/lang/<sprache>.json ergänzt und nicht mehr
verwendete Einträge entfernt. Leere Werte meldet tools/build_web.py als Fehler.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from game.content import build_game_data  # noqa: E402
from game.content.i18n import LANG_DIR, LANGUAGES, load_table, texts  # noqa: E402


def main():
    found = texts(build_game_data())
    for lang in LANGUAGES:
        old = load_table(lang)
        table = {s: old.get(s, "") for s in found}
        path = LANG_DIR / f"{lang}.json"
        path.write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        todo = sum(1 for v in table.values() if not v)
        print(f"{path.relative_to(ROOT)}: {len(table)} Texte, {todo} ohne Übersetzung, {len(set(old) - set(table))} entfernt")


if __name__ == "__main__":
    main()
