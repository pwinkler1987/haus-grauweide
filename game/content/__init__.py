"""Spielinhalte: Figuren, Gegenstände, Räume.

build_game_data() lädt alle Module bei jedem Aufruf neu. Wer einen Raum
ändert, muss deshalb nur den Browser neu laden – kein Server-Neustart nötig.
"""
import importlib
import pkgutil

from . import rooms as rooms_pkg


def _fresh(name):
    return importlib.reload(importlib.import_module(name))


def build_game_data():
    characters = _fresh(f"{__name__}.characters")
    items = _fresh(f"{__name__}.items")
    dialogs = _fresh(f"{__name__}.dialogs")
    rooms = {}
    for info in pkgutil.iter_modules(rooms_pkg.__path__):
        room = _fresh(f"{rooms_pkg.__name__}.{info.name}").ROOM
        rooms[room["id"]] = room
    return {
        "title": "Das Haus Grauweide",
        "start": {"room": "treehouse", "character": "patrick"},
        "characters": characters.CHARACTERS,
        "items": items.ITEMS,
        "dialogs": dialogs.DIALOGS,
        "rooms": rooms,
    }
