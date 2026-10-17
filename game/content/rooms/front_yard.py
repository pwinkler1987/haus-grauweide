"""Der Vorgarten der Villa. Ab Etappe 4 gibt es von hier drei Wege ins Haus."""

WALL, ROOF, WOOD = "#1a1820", "#100e14", "#3a2416"
WINDOW, LIT = "#0d1018", "#7fd8ff"


def window(x, y, lit=False):
    return [("rect", x - 2, y - 2, 18, 24, "#2a2630"),
            ("rect", x, y, 14, 20, LIT if lit else WINDOW),
            ("rect", x + 6, y, 2, 20, "#2a2630"), ("rect", x, y + 9, 14, 2, "#2a2630")]


DRAW = [
    ("rect", 0, 0, 320, 144, "#0a0f26"),
    ("stars", 0, 0, 40, 60, 8, "#c8c8ff"),
    ("stars", 280, 0, 40, 60, 8, "#c8c8ff"),
    # Fassade
    ("rect", 40, 0, 240, 100, WALL),
    ("poly", [(30, 8), (160, -20), (290, 8)], ROOF),
    *window(62, 14), *window(98, 14), *window(206, 14), *window(242, 14, lit=True),
    *window(62, 56), *window(98, 56), *window(206, 56), *window(242, 56),
    # Haustür mit Vordach und Stufen
    ("poly", [(136, 44), (160, 34), (184, 44)], ROOF),
    ("rect", 144, 50, 32, 50, "#2a2630"),
    ("rect", 146, 52, 28, 48, WOOD),
    ("rect", 159, 52, 2, 48, "#2a1a10"),
    ("circle", 168, 78, 1.5, "#c8a040"),
    ("rect", 180, 64, 4, 5, "#888888"),  # Klingel
    ("rect", 138, 100, 44, 4, "#3a3a42"), ("rect", 132, 104, 56, 4, "#33333a"),
    # Kohlenschacht-Klappe im Sockel
    ("rect", 84, 92, 18, 8, "#2b2b2b"), ("rect", 85, 93, 16, 1, "#444444"),
    # Boden, Weg, Sonnenuhr
    ("rect", 0, 100, 320, 44, "#1b2414"),
    ("poly", [(140, 108), (180, 108), (200, 144), (120, 144)], "#3b2f22"),
    ("rect", 236, 112, 10, 14, "#5a5a62"),
    ("poly", [(230, 112), (241, 108), (252, 112)], "#6a6a72"),
    ("line", 241, 108, 246, 104, "#8a8a92"),
    # Gärtnerhäuschen
    ("rect", 288, 60, 32, 46, "#3a2a1c"),
    ("poly", [(284, 62), (304, 46), (320, 58), (320, 62)], "#2a1c12"),
    ("rect", 296, 76, 12, 30, "#24170e"),
]

ROOM = {
    "id": "front_yard",
    "name": "Vor dem Haus",
    "draw": DRAW,
    "walkbox": [(0, 112), (320, 112), (320, 143), (0, 143)],
    "start": (60, 130),
    "on_enter": {
        "if": "!flag:yard_reached",
        "do": [
            "set:yard_reached",
            "say:Geschafft, ich bin auf dem Grundstück!",
            "narrate:Ende von Etappe 3.\n\nIn Etappe 4: Dialoge, Zwischensequenzen und drei Wege ins Haus – Kohlenschacht, Gärtnerhaus und die Haustür mit dem Geheimnis der Sonnenuhr.\n\nTipp: Mit Tab holst du die anderen nach.",
        ],
    },
    "hotspots": [
        {"id": "tuer", "name": "Haustür", "rect": (144, 50, 32, 50), "walk_to": (160, 114),
         "actions": {"look": "Eine schwere Eichentür. Kein Schlüsselloch, nur ein Messingrad mit Zahlen.",
                     "open": "Abgeschlossen. Natürlich.",
                     "push": "Die bewegt sich keinen Millimeter.",
                     "talk": "Hallo? ...Niemand macht auf."}},
        {"id": "klingel", "name": "Klingel", "rect": (178, 62, 8, 9), "walk_to": (176, 114),
         "actions": {"look": "Ein alter Klingelknopf aus Messing.",
                     "push": ["sound:click", "wait:600",
                              "say:Ding-dong... Das Echo klingt nach einem sehr großen, sehr leeren Haus."]}},
        {"id": "fenster", "name": "Fenster", "rect": (60, 12, 214, 68), "walk_to": (160, 116),
         "actions": {"look": "Alle Fenster sind dunkel. Bis auf eins ganz rechts oben.",
                     "open": "Viel zu hoch. Und bestimmt verriegelt."}},
        {"id": "schacht", "name": "Klappe im Sockel", "rect": (82, 90, 22, 12), "walk_to": (93, 116),
         "actions": {"look": "Eine kleine Metallklappe. Ein alter Kohlenschacht?",
                     "open": "Die klemmt. Da kümmern wir uns in Etappe 4 drum."}},
        {"id": "sonnenuhr", "name": "Sonnenuhr", "rect": (228, 102, 26, 26), "walk_to": (226, 128),
         "actions": {"look": "Eine Sonnenuhr. Im Mondlicht zeigt ihr Schatten auf... 23:13?"}},
        {"id": "gartenhaus", "name": "Gärtnerhäuschen", "rect": (284, 46, 36, 60), "walk_to": (300, 116),
         "actions": {"look": "Ein kleines Gärtnerhäuschen. Die Tür steht einen Spalt offen.",
                     "open": "Gleich... (kommt in Etappe 4)"}},
        {"id": "zurueck", "name": "Zurück zum Tor", "rect": (0, 100, 20, 44), "walk_to": (4, 128),
         "default": "walk",
         "actions": {"walk": {"if": "flag:gate_open", "do": "goto:gate:160,124",
                              "else": "goto:gate:40,120"}}},
    ],
}
