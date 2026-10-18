"""Das Gärtnerhäuschen – hier gießt Anselm Brack seit 1958 dieselben Rosen."""

WALL, WALL_LINE, FLOOR = "#3a3020", "#2e2618", "#2a2218"
WOOD, DARK = "#6e4a2c", "#1e160e"

DRAW = [
    ("rect", 0, 0, 320, 112, WALL),
    *[("rect", x, 0, 1, 112, WALL_LINE) for x in range(12, 320, 16)],
    ("rect", 0, 108, 320, 36, FLOOR),
    ("rect", 0, 106, 320, 3, DARK),
    # Tür nach draußen (links)
    ("rect", 8, 40, 30, 68, DARK),
    ("rect", 10, 42, 26, 66, "#0a0f26"),
    ("stars", 10, 42, 26, 30, 4, "#c8c8ff"),
    # Fenster mit Mond
    ("rect", 196, 18, 44, 34, DARK),
    ("rect", 199, 21, 38, 28, "#0b1030"),
    ("circle", 228, 30, 4, "#e8e4c0"),
    ("rect", 217, 21, 2, 28, DARK),
    # Regal mit Blumentöpfen
    ("rect", 60, 30, 90, 3, WOOD), ("rect", 60, 56, 90, 3, WOOD),
    *[("poly", [(x, 30), (x + 2, 22), (x + 10, 22), (x + 12, 30)], "#b5651d") for x in range(64, 146, 20)],
    *[("poly", [(x, 56), (x + 2, 48), (x + 10, 48), (x + 12, 56)], "#b5651d") for x in range(74, 146, 24)],
    # Werkbank mit frischen Rosen
    ("rect", 110, 84, 90, 4, WOOD),
    ("rect", 114, 88, 4, 20, WOOD), ("rect", 192, 88, 4, 20, WOOD),
    *[("rect", x, 72, 1, 12, "#2e7d32") for x in (128, 134, 140, 146)],
    *[("circle", x, 71, 3, "#c62828") for x in (128, 134, 140, 146)],
    ("rect", 124, 78, 26, 6, "#795548"),
    ("poly", [(160, 84), (162, 76), (172, 76), (174, 84)], "#9e9e9e"),  # Gießkanne
    ("line", 172, 78, 180, 74, "#9e9e9e"),
    # Spaten an der Wand
    {"if": "!flag:got_spaten", "shapes": [
        ("rect", 52, 66, 2, 34, WOOD), ("rect", 49, 64, 8, 3, WOOD),
        ("poly", [(48, 100), (58, 100), (57, 110), (49, 110)], "#9a9aa2"),
    ]},
    # Leiter an der rechten Wand
    {"if": "!flag:got_leiter", "shapes": [
        ("line", 262, 20, 272, 108, WOOD), ("line", 282, 20, 292, 108, WOOD),
        *[("line", 263 + i, 28 + i * 10, 283 + i, 28 + i * 10, WOOD) for i in range(8)],
    ]},
]

ROOM = {
    "id": "garden_shed",
    "name": "Im Gärtnerhäuschen",
    "draw": DRAW,
    "walkbox": [(10, 112), (310, 112), (318, 143), (2, 143)],
    "start": (40, 126),
    "on_enter": {
        "if": "!flag:anselm_placed",
        "do": [
            "set:anselm_placed",
            "place:anselm:garden_shed:166,118",
            "face:anselm:left",
            "say:Oh! Hier ist ja jemand.",
            "sayas:anselm:Psst. Nicht so laut, die Rosen schlafen.",
        ],
    },
    "hotspots": [
        {"id": "tuer", "name": "Tür nach draußen", "rect": (8, 40, 30, 68), "walk_to": (24, 120),
         "default": "walk",
         "actions": {"walk": "goto:front_yard:300,122"}},
        {"id": "regal", "name": "Regal", "rect": (60, 20, 90, 40), "walk_to": (104, 120),
         "actions": {"look": "Leere Blumentöpfe. Fein säuberlich aufgereiht. Kein Staubkorn."}},
        {"id": "rosen", "name": "Rosen", "rect": (122, 66, 30, 18), "walk_to": (136, 120),
         "actions": {"look": "Rosen. Ende Oktober. Und sie sehen aus, als wären sie eben erst aufgeblüht.",
                     "take": "sayas:anselm:Finger weg von meinen Rosen!"}},
        {"id": "giesskanne", "name": "Gießkanne", "rect": (158, 72, 24, 13), "walk_to": (150, 120),
         "actions": {"look": "Randvoll. Obwohl hier nirgends ein Wasserhahn ist.",
                     "take": "Die braucht Herr Brack bestimmt."}},
        {"id": "fenster", "name": "Fenster", "rect": (196, 18, 44, 34), "walk_to": (218, 118),
         "actions": {"look": "Von hier sieht man den Turm der Villa. Das Licht flackert."}},
        {"id": "spaten", "name": "Spaten", "rect": (46, 62, 14, 48), "walk_to": (60, 122),
         "if": "!flag:got_spaten",
         "actions": {"look": "Ein alter Spaten mit Holzstiel.",
                     "take": ["take:spaten", "say:Den leih ich mir mal."]}},
        {"id": "leiter", "name": "Leiter", "rect": (258, 18, 38, 92), "walk_to": (272, 122),
         "if": "!flag:got_leiter",
         "actions": {"look": "Eine lange Holzleiter.",
                     "take": {"if": "flag:anselm_ladder",
                              "do": ["take:leiter", "sayas:anselm:Bringt sie wieder, wenn ihr fertig seid."],
                              "else": "sayas:anselm:Die Leiter gehört dem Haus. Erst fragen, dann nehmen."}}},
    ],
}
