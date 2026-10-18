"""Die obere Galerie – Bibliothek, Labor und die Turmtür, bewacht von Tick."""

PAPER, STRIPE, PANEL = "#3a2a3a", "#33243a", "#2a1a12"

TOWER_UP = {
    "if": "flag:tower_open",
    "do": ["sound:tick", "party_goto:tower_stairs"],
    "else": {"if": "flag:tick_awake",
             "do": "sayas:tick:Ohne Losung kein Durchgang. Bedaure.",
             "else": "Abgeschlossen. Und davor steht dieser Blechmann."},
}

DRAW = [
    ("rect", 0, 0, 320, 104, PAPER),
    *[("rect", x, 0, 4, 80, STRIPE) for x in range(6, 320, 14)],
    ("rect", 0, 80, 320, 24, PANEL),
    ("rect", 0, 79, 320, 2, "#4a2f1b"),
    ("rect", 0, 104, 320, 40, "#3a2416"),
    ("rect", 0, 114, 320, 18, "#6a1a22"),
    ("rect", 0, 115, 320, 1, "#a07a30"), ("rect", 0, 130, 320, 1, "#a07a30"),
    # Treppe nach unten (links)
    ("rect", 0, 60, 22, 44, "#1a1012"),
    *[("rect", 0, 64 + i * 8, 22 - i * 3, 2, "#4a2f1b") for i in range(5)],
    # Bibliothekstür
    ("rect", 34, 44, 34, 60, "#1a1012"), ("rect", 36, 46, 30, 58, "#4a2f1b"),
    ("rect", 44, 54, 14, 4, "#d8c890"),
    ("circle", 61, 76, 1.5, "#c8a040"),
    # Wandleuchter
    *[s for x in (100, 220) for s in (("circle", x, 40, 9, "rgba(255,210,127,0.12)"),
                                      ("rect", x - 1, 40, 3, 8, "#c8a040"),
                                      ("circle", x, 38, 2, "#ffd27f"))],
    # Turmtür (rund, Eisen) mit kleiner Uhr darüber
    ("circle", 160, 52, 22, "#1a1a1e"), ("rect", 138, 52, 44, 52, "#1a1a1e"),
    ("circle", 160, 52, 19, "#2e2e34"), ("rect", 141, 52, 38, 52, "#2e2e34"),
    *[("rect", 141, y, 38, 2, "#1a1a1e") for y in (62, 80, 96)],
    *[("circle", x, y, 1, "#5a5a62") for x in (145, 175) for y in (63, 81, 97)],
    ("circle", 160, 20, 8, "#e8e4c0"), ("circle", 160, 20, 9, "rgba(0,0,0,0)"),
    ("line", 160, 20, 160, 14, "#111111"), ("line", 160, 20, 157, 19, "#111111"),
    # Labortür (Metall) mit Kontrolllampe
    ("rect", 262, 44, 36, 60, "#1a1a1e"), ("rect", 264, 46, 32, 58, "#4a4a52"),
    ("rect", 268, 52, 24, 10, "#3a3a42"),
    {"if": "flag:power_on", "shapes": [("circle", 304, 60, 3, "#33ff66"),
                                       ("circle", 304, 60, 6, "rgba(51,255,102,0.2)")]},
    {"if": "!flag:power_on", "shapes": [("circle", 304, 60, 3, "#333333")]},
]

ROOM = {
    "id": "upstairs",
    "name": "Obere Galerie",
    "draw": DRAW,
    "walkbox": [(2, 108), (318, 108), (318, 143), (2, 143)],
    "start": (30, 126),
    "on_enter": {
        "if": "!flag:tick_placed",
        "do": [
            "set:tick_placed",
            "place:tick:upstairs:200,116",
            "face:tick:left",
            "say:Was ist DAS denn?",
            "say:Eine Ritterrüstung? Nein... das ist eine Maschine!",
        ],
    },
    "hotspots": [
        {"id": "treppe", "name": "Treppe nach unten", "rect": (0, 60, 24, 48), "walk_to": (8, 124),
         "default": "walk",
         "actions": {"walk": "goto:hall:160,114"}},
        {"id": "bibliothek", "name": "Bibliothek", "rect": (34, 44, 34, 60), "walk_to": (51, 114),
         "default": "walk",
         "actions": {"look": "Auf dem Messingschild steht \"Bibliothek\".",
                     "walk": "goto:library:40,126", "open": "goto:library:40,126"}},
        {"id": "turmuhr", "name": "Kleine Uhr", "rect": (150, 10, 20, 20), "walk_to": (160, 112),
         "actions": {"look": "Eine kleine Uhr über der Tür. Natürlich: 23:13."}},
        {"id": "turmtuer", "name": "Turmtür", "rect": (138, 30, 44, 74), "walk_to": (160, 112),
         "default": "walk",
         "actions": {"look": "Eine runde Eisentür, vernietet wie ein Tresor. Dahinter muss der Turm sein.",
                     "open": TOWER_UP, "walk": TOWER_UP, "push": "Keinen Millimeter."}},
        {"id": "labor", "name": "Labortür", "rect": (262, 44, 36, 60), "walk_to": (280, 114),
         "default": "walk",
         "actions": {
             "look": {"if": "flag:power_on",
                      "do": "Eine Metalltür mit elektrischem Schloss. Die Lampe leuchtet grün.",
                      "else": "Eine Metalltür mit elektrischem Schloss. Die Kontrolllampe ist aus. Kein Strom?"},
             "walk": {"if": "flag:power_on", "do": ["sound:click", "goto:lab:30,126"],
                      "else": "Zu. Das Schloss braucht Strom."},
             "open": {"if": "flag:power_on", "do": ["sound:click", "goto:lab:30,126"],
                      "else": "Zu. Das Schloss braucht Strom."},
         }},
    ],
}
