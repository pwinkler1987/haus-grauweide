"""Spielinhalte: Figuren, Gegenstände, Räume.

build_game_data() lädt alle Module bei jedem Aufruf neu. Wer einen Raum
ändert, muss deshalb nur den Browser neu laden – kein Server-Neustart nötig.
"""
import importlib
import pkgutil
from pathlib import Path

from . import rooms as rooms_pkg

STATIC = Path(__file__).resolve().parents[2] / "static"


def _fresh(name):
    return importlib.reload(importlib.import_module(name))


def build_game_data():
    characters = _fresh(f"{__name__}.characters")
    items = _fresh(f"{__name__}.items")
    dialogs = _fresh(f"{__name__}.dialogs")
    endings = _fresh(f"{__name__}.endings")
    rooms = {}
    for info in pkgutil.iter_modules(rooms_pkg.__path__):
        room = _fresh(f"{rooms_pkg.__name__}.{info.name}").ROOM
        if "image" not in room and (STATIC / "img" / "rooms" / f"{room['id']}.png").exists():
            room = {**room, "image": f"img/rooms/{room['id']}.png"}
        rooms[room["id"]] = room
    return {
        "title": "Das Haus Grauweide",
        "start": {"room": "treehouse", "character": "patrick"},
        "characters": characters.CHARACTERS,
        "items": items.ITEMS,
        "dialogs": dialogs.DIALOGS,
        "endings": endings.ENDINGS,
        "rooms": rooms,
    }
