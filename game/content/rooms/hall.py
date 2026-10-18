"""Die Eingangshalle – erster Raum im Haus. Hier zeigt sich zum ersten Mal die Gestalt."""

WALL, WALL_DARK, WOOD = "#2a2230", "#201a26", "#3a2416"
TILE_A, TILE_B = "#2c2c34", "#1c1c22"

DRAW = [
    ("rect", 0, 0, 320, 104, WALL),
    *[("rect", x, 0, 2, 104, WALL_DARK) for x in range(20, 320, 40)],
    # Schachbrett-Boden
    ("rect", 0, 104, 320, 40, TILE_B),
    *[("rect", x + (r % 2) * 16, 104 + r * 8, 16, 8, TILE_A) for r in range(5) for x in range(0, 320, 32)],
    # Galerie mit Geländer
    ("rect", 60, 60, 200, 4, WOOD),
    *[("rect", x, 44, 2, 16, WOOD) for x in range(64, 258, 8)],
    ("rect", 60, 42, 200, 3, WOOD),
    # Freitreppe
    *[("rect", 120 - i * 4, 64 + i * 5, 80 + i * 8, 5, "#4a2f1b" if i % 2 else "#3a2416") for i in range(8)],
    # Kronleuchter
    ("line", 160, 0, 160, 12, "#888888"),
    ("rect", 146, 12, 28, 3, "#9a8a50"),
    *[("circle", x, 11, 1.5, "#ffe08a") for x in (148, 156, 164, 172)],
    # Gemälde
    ("rect", 214, 10, 32, 28, "#7a5a20"),
    ("rect", 217, 13, 26, 22, "#2a3a4a"),
    ("rect", 226, 18, 8, 8, "#f0dcc8"), ("rect", 225, 16, 10, 3, "#eeeeee"),
    ("rect", 226, 20, 8, 2, "#7fd8ff"),
    ("rect", 224, 26, 12, 9, "#e8e8e8"),
    # Standuhr (Pendel steht schräg still)
    ("rect", 74, 38, 22, 66, "#4a2a18"),
    ("circle", 85, 48, 8, "#e8e4c0"),
    ("line", 85, 48, 85, 43, "#111111"), ("line", 85, 48, 82, 47, "#111111"),
    ("rect", 79, 60, 12, 38, "#1a1008"),
    ("line", 85, 60, 90, 88, "#c8a040"), ("circle", 90, 89, 3, "#c8a040"),
    # Haustür (links) – offen oder zu
    ("rect", 6, 48, 32, 56, "#2a2630"),
    {"if": "!flag:door_open", "shapes": [("rect", 8, 50, 28, 54, WOOD), ("rect", 21, 50, 2, 54, "#2a1a10")]},
    {"if": "flag:door_open", "shapes": [("rect", 8, 50, 28, 54, "#0a0f26"), ("rect", 8, 50, 6, 54, WOOD)]},
    # Fenster neben der Tür (hier kommt man mit der Leiter rein)
    ("rect", 44, 30, 18, 24, "#2a2630"), ("rect", 46, 32, 14, 20, "#0b1030"),
    # Kellertür (rechts)
    ("rect", 284, 54, 26, 50, "#2a2630"), ("rect", 286, 56, 22, 48, "#2e1e12"),
    ("circle", 290, 80, 1.5, "#c8a040"),
]

ROOM = {
    "id": "hall",
    "name": "Eingangshalle",
    "draw": DRAW,
    "walkbox": [(4, 108), (316, 108), (318, 143), (2, 143)],
    "start": (60, 124),
    "on_enter": {
        "if": "!flag:hall_intro",
        "do": [
            "set:hall_intro",
            "say:Wow...",
            "sound:tick",
            "say:Hört ihr das? Da tickt doch was.",
            "place:ottilie:hall:250,60",
            "face:ottilie:left",
            "wait:400",
            "walk:ottilie:110,60",
            "sayas:ottilie:Noch eine Sekunde... nur noch eine einzige Sekunde.",
            "sound:static",
            "remove:ottilie",
            "say:Da war jemand! Oben auf der Galerie!",
            "say:Und sie war... durchsichtig.",
            "say:Ich glaube, sie wollte nach oben.",
        ],
    },
    "hotspots": [
        {"id": "haustuer", "name": "Haustür", "rect": (6, 48, 32, 56), "walk_to": (24, 116),
         "default": "walk",
         "actions": {
             "look": {"if": "flag:door_open", "do": "Die Haustür steht offen.",
                      "else": "Von innen hat die Tür einen ganz normalen Riegel."},
             "open": {"if": "flag:door_open", "do": "Die ist schon offen.",
                      "else": ["sound:click", "set:door_open", "say:So. Jetzt kommen die anderen auch rein."]},
             "close": {"if": "flag:door_open", "do": ["sound:click", "unset:door_open"],
                       "else": "Die ist schon zu."},
             "walk": {"if": "flag:door_open", "do": "goto:front_yard:160,118",
                      "else": "Die ist zu. Aber von innen kann ich sie öffnen."},
         }},
        {"id": "fenster", "name": "Fenster", "rect": (44, 30, 18, 24), "walk_to": (54, 116),
         "actions": {"look": {"if": "flag:ladder_placed", "do": "Draußen lehnt die Leiter.",
                              "else": "Das Fenster klemmt und steht einen Spalt offen."},
                     "walk": {"if": "flag:ladder_placed", "do": "goto:front_yard:214,122",
                              "else": "Ohne Leiter springe ich da nicht raus."}}},
        {"id": "standuhr", "name": "Standuhr", "rect": (72, 36, 26, 68), "walk_to": (86, 116),
         "actions": {"look": "Eine riesige Standuhr. Sie zeigt 23:13. Das Pendel hängt schräg in der Luft, mitten im Schwung.",
                     "push": "Das Pendel bewegt sich keinen Millimeter. Als wäre es eingefroren.",
                     "open": "Das Gehäuse ist verschlossen. Da ist ein winziges Schlüsselloch."}},
        {"id": "gemaelde", "name": "Gemälde", "rect": (214, 10, 32, 28), "walk_to": (230, 116),
         "actions": {"look": {"if": "char:ida",
                              "do": ["say:Auf dem Messingschild steht: \"Prof. Dr. Ottilie Grauweide, 1956\".",
                                     "say:Die Frau auf der Galerie... das war sie!"],
                              "else": "Eine Frau mit Schutzbrille und wilden grauen Haaren. Darunter ein Messingschild."}}},
        {"id": "treppe", "name": "Treppe", "rect": (88, 62, 144, 42), "walk_to": (160, 112),
         "default": "walk",
         "actions": {"look": "Eine breite Freitreppe hinauf zur Galerie.",
                     "walk": "goto:upstairs:30,126"}},
        {"id": "kellertuer", "name": "Kellertür", "rect": (284, 54, 26, 50), "walk_to": (296, 118),
         "default": "walk",
         "actions": {"look": "Eine schmale Tür. Dahinter geht es in den Keller.",
                     "walk": "goto:cellar:280,124", "open": "goto:cellar:280,124"}},
    ],
}
