"""Am Waldrand – hier treffen sich die Freunde (Etappe 3+). Vorerst Platzhalter."""

SKY, HILL, TREE, TRUNK = "#0a0f26", "#121a12", "#0e2414", "#2a1a10"

DRAW = [
    ("rect", 0, 0, 320, 144, SKY),
    ("stars", 0, 0, 320, 60, 45, "#c8c8ff"),
    ("circle", 268, 22, 8, "#e8e4c0"),
    ("circle", 265, 20, 7, SKY),  # Sichelmond
    # Krähenhügel mit Villa am Horizont
    ("poly", [(100, 90), (150, 62), (190, 54), (230, 62), (290, 90)], HILL),
    ("rect", 180, 42, 22, 14, "#05070a"),
    ("poly", [(177, 43), (191, 33), (205, 43)], "#05070a"),
    ("rect", 197, 31, 4, 9, "#05070a"),
    ("rect", 184, 46, 2, 2, "#7fd8ff"),
    # Boden & Weg
    ("rect", 0, 88, 320, 56, "#16220f"),
    ("poly", [(150, 144), (250, 144), (205, 90), (195, 90)], "#3b2f22"),
    # Bäume
    ("poly", [(250, 100), (275, 20), (300, 100)], TREE),
    ("poly", [(290, 110), (312, 30), (334, 110)], TREE),
    ("poly", [(80, 96), (100, 34), (120, 96)], TREE),
    ("rect", 0, 0, 34, 144, TRUNK),  # Baumstamm mit Baumhaus
    ("rect", 34, 0, 40, 20, "#4a2f1b"),
    *[("rect", 36, y, 12, 2, "#8a6238") for y in range(30, 130, 10)],
    ("rect", 36, 26, 2, 104, "#8a6238"), ("rect", 46, 26, 2, 104, "#8a6238"),
]

ROOM = {
    "id": "forest_edge",
    "name": "Am Waldrand",
    "draw": DRAW,
    "walkbox": [(30, 112), (300, 112), (318, 143), (20, 143)],
    "start": (60, 130),
    "on_enter": {
        "if": "!flag:arrived_forest",
        "do": [
            "set:arrived_forest",
            "say:Uff. Ganz schön dunkel hier draußen.",
            "narrate:Ende von Etappe 2.\n\nAls Nächstes: Die Freunde treffen sich am Waldrand, die Charakterwahl und der Weg zum Tor der Villa.",
        ],
    },
    "hotspots": [
        {"id": "villa", "name": "Haus Grauweide", "rect": (175, 30, 32, 26), "walk_to": (200, 120),
         "actions": {"look": "Das Haus Grauweide. Das Licht oben brennt immer noch."}},
        {"id": "weg", "name": "Waldweg", "rect": (170, 88, 70, 30), "walk_to": (200, 116),
         "default": "walk",
         "actions": {"look": "Der Weg zum Krähenhügel.",
                     "walk": "Allein gehe ich da nicht rein. Ich warte auf die anderen."}},
        {"id": "leiter", "name": "Leiter zum Baumhaus", "rect": (30, 20, 24, 112), "walk_to": (44, 126),
         "default": "walk",
         "actions": {"look": "Die Leiter zu unserem Baumhaus.",
                     "walk": "goto:treehouse:55,128", "use": "goto:treehouse:55,128"}},
    ],
}
