"""Am Waldrand – die Freunde treffen sich, der Spieler wählt seine Gruppe."""

SKY, HILL, TREE, TRUNK = "#0a0f26", "#121a12", "#0e2414", "#2a1a10"


def bike(x, y, color):
    """Ein abgestelltes Fahrrad (Platzhalter-Grafik)."""
    return [
        ("circle", x, y, 6, "#777777"), ("circle", x, y, 5, "#16220f"),
        ("circle", x + 16, y, 6, "#777777"), ("circle", x + 16, y, 5, "#16220f"),
        ("line", x, y, x + 6, y - 8, color), ("line", x + 6, y - 8, x + 16, y, color),
        ("line", x + 6, y - 8, x + 14, y - 8, color), ("line", x + 14, y - 8, x + 16, y, color),
        ("line", x + 14, y - 8, x + 13, y - 12, color), ("rect", x + 11, y - 13, 5, 1, "#333333"),
    ]


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
    # Fahrräder der Freunde
    *bike(84, 108, "#c0392b"),
    *bike(108, 106, "#2e86c1"),
    *bike(132, 108, "#27ae60"),
]

ROOM = {
    "id": "forest_edge",
    "name": "Am Waldrand",
    "draw": DRAW,
    "walkbox": [(30, 112), (300, 112), (318, 143), (20, 143)],
    "start": (60, 130),
    "on_enter": {
        "if": "!flag:party_chosen",
        "do": [
            "place:ida:forest_edge:120,124",
            "place:kemal:forest_edge:150,132",
            "place:merle:forest_edge:182,126",
            "place:finn:forest_edge:214,134",
            "place:lena:forest_edge:246,126",
            "sayas:ida:Da bist du ja endlich, Patrick!",
            "say:Ich hab's durchs Fernglas gesehen. Im Haus Grauweide brennt Licht.",
            "sayas:finn:Und das Radiosignal kam auf allen Frequenzen gleichzeitig. Das ist eigentlich unmöglich.",
            "sayas:merle:Ich hab meine Kamera dabei. Wenn es da Geister gibt, will ich ein Foto.",
            "sayas:kemal:Und ich meinen Werkzeugkram. Man weiß ja nie.",
            "sayas:lena:Wir können aber nicht alle gehen. Wenn sechs Kinder nachts fehlen, fällt das auf.",
            "say:Stimmt. Drei gehen rein, die anderen decken uns.",
            "choose:2",
            "set:party_chosen",
            "say:Die Räder lassen wir hier, der Weg ist zu matschig. Los!",
        ],
    },
    "hotspots": [
        {"id": "villa", "name": "Haus Grauweide", "rect": (175, 30, 32, 26), "walk_to": (200, 120),
         "actions": {"look": "Das Haus Grauweide. Das Licht oben brennt immer noch."}},
        {"id": "raeder", "name": "Fahrräder", "rect": (76, 92, 80, 24), "walk_to": (116, 122),
         "actions": {"look": "Unsere Räder. Ab hier geht's zu Fuß weiter.",
                     "take": "Auf dem matschigen Waldweg schiebe ich das Ding nur."}},
        {"id": "weg", "name": "Waldweg", "rect": (170, 88, 70, 30), "walk_to": (200, 116),
         "default": "walk",
         "actions": {"look": "Der Weg durch den Wald zum Krähenhügel.",
                     "walk": "party_goto:forest_path"}},
        {"id": "leiter", "name": "Leiter zum Baumhaus", "rect": (30, 20, 24, 92), "walk_to": (44, 126),
         "default": "walk",
         "actions": {"look": "Die Leiter zu unserem Baumhaus.",
                     "walk": {"if": "char:patrick", "do": "goto:treehouse:55,128",
                              "else": "Im Baumhaus gibt's nichts mehr zu tun."}}},
    ],
}
