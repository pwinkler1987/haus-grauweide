"""Der Vorgarten der Villa – drei Wege ins Haus:

  1. Haustür:      Zahlenrad auf die "Stunde, die nie vergeht" stellen (Sonnenuhr: 23:13)
  2. Fenster:      Leiter aus dem Gärtnerhaus (Anselm muss sie erst verleihen)
  3. Kohlenschacht: Klappe mit Spaten (oder Kemal) öffnen, nur Lena passt durch – mit Licht
"""

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
    {"if": "flag:door_open", "sprite": "front_yard_door_open", "shapes": [("rect", 146, 52, 28, 48, "#05060a"), ("rect", 146, 52, 6, 48, WOOD)]},
    # Kohlenschacht-Klappe im Sockel
    {"if": "!flag:chute_open", "sprite": "front_yard_chute_closed", "shapes": [("rect", 84, 92, 18, 8, "#2b2b2b"), ("rect", 85, 93, 16, 1, "#444444")]},
    {"if": "flag:chute_open", "sprite": "front_yard_chute_open", "shapes": [("rect", 84, 92, 18, 8, "#050505"), ("rect", 84, 86, 18, 6, "#2b2b2b")]},
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
    # angelehnte Leiter am Fenster rechts neben der Tür
    {"if": "flag:ladder_placed", "sprite": "front_yard_ladder", "shapes": [
        ("line", 204, 116, 206, 66, "#8a6238"), ("line", 222, 116, 220, 66, "#8a6238"),
        *[("line", 205, y, 221, y, "#8a6238") for y in range(72, 116, 8)],
    ]},
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
            "say:Irgendwie muss man da doch reinkommen...",
        ],
    },
    "hotspots": [
        {"id": "fenster", "name": "Fenster", "rect": (60, 12, 214, 68), "walk_to": (160, 116),
         "actions": {"look": "Alle Fenster sind dunkel. Bis auf eins ganz rechts oben.",
                     "open": "Die sind alle verriegelt. Bis auf vielleicht eins..."}},
        {"id": "fenster_spalt", "name": "Klemmendes Fenster", "rect": (204, 54, 18, 24), "walk_to": (213, 118),
         "default": "walk",
         "actions": {
             "look": {"if": "flag:ladder_placed", "do": "Die Leiter lehnt am Fenster. Ich kann rein.",
                      "else": "Dieses Fenster steht einen Spalt offen! Aber der Sockel ist so hoch, da komm ich nicht ran."},
             "open": "Zu hoch.",
             "use:leiter": ["drop:leiter", "set:ladder_placed", "sound:click",
                            "say:Leiter angelehnt. Passt genau."],
             "walk": {"if": "flag:ladder_placed",
                      "do": ["say:Hoch und durch den Spalt...", "goto:hall:54,120"],
                      "else": "Zu hoch. Ich bräuchte eine Leiter."},
         }},
        {"id": "tuer", "name": "Haustür", "rect": (144, 50, 32, 50), "walk_to": (160, 114),
         "default": "walk",
         "actions": {
             "look": {"if": "flag:door_open", "do": "Die Haustür steht offen.",
                      "else": {"if": "char:ida",
                               "do": ["say:Statt Schlüsselloch ein Messingrad mit vier Ziffern.",
                                      "say:Darum ist etwas eingraviert: \"Zur Stunde, die nie vergeht.\""],
                               "else": "Eine schwere Eichentür. Statt Schlüsselloch ein Messingrad mit vier Ziffern."}},
             "open": {"if": "flag:door_open", "do": "Die ist schon offen.",
                      "else": "Abgeschlossen. Vielleicht muss man das Zahlenrad benutzen?"},
             "use": {"if": "flag:door_open", "do": "goto:hall:30,124",
                     "else": ["codelock:2313:door_open",
                              {"if": "flag:door_open",
                               "do": ["sound:click", "wait:300", "sound:tick",
                                      "say:Klack! Die Tür schwingt von alleine auf."],
                               "else": "Nichts passiert."}]},
             "walk": {"if": "flag:door_open", "do": "goto:hall:30,124",
                      "else": "Abgeschlossen."},
             "push": "Die bewegt sich keinen Millimeter.",
             "talk": "Hallo? ...Niemand macht auf.",
         }},
        {"id": "klingel", "name": "Klingel", "rect": (178, 62, 8, 9), "walk_to": (176, 114),
         "actions": {"look": "Ein alter Klingelknopf aus Messing.",
                     "push": ["sound:click", "wait:600",
                              "say:Ding-dong... Das Echo klingt nach einem sehr großen, sehr leeren Haus."]}},
        {"id": "schacht", "name": "Klappe im Sockel", "rect": (82, 86, 22, 16), "walk_to": (93, 116),
         "default": "walk",
         "actions": {
             "look": {"if": "flag:chute_open",
                      "do": "Ein schmaler Kohlenschacht. Ganz schön eng da drin.",
                      "else": "Eine kleine Metallklappe. Ein alter Kohlenschacht? Sie klemmt."},
             "open": {"if": "flag:chute_open", "do": "Die ist schon offen.",
                      "else": {"if": "char:kemal",
                               "do": ["say:Ein bisschen Kriechöl, ein Schraubenzieher...", "sound:click",
                                      "set:chute_open", "say:...und auf!"],
                               "else": "Die klemmt total. Ich bräuchte einen Hebel."}},
             "use:spaten": {"if": "flag:chute_open", "do": "Die ist schon offen.",
                            "else": ["say:Hau ruck!", "sound:click", "set:chute_open",
                                     "say:Offen! Der Spaten ist ein super Hebel."]},
             "walk": {"if": "!flag:chute_open", "do": "Die Klappe ist zu.",
                      "else": {"if": "!char:lena",
                               "do": {"if": "party:lena",
                                      "do": "Da passe ich niemals durch. Lena vielleicht...",
                                      "else": "Viel zu eng. Da passe ich nicht durch."},
                               "else": {"if": "!has:lampe_an",
                                        "do": "Da unten ist es stockdunkel. Ohne Licht rutsche ich da nicht rein.",
                                        "else": ["say:Ich bin dünn genug. Bis gleich!", "goto:cellar"]}}},
         }},
        {"id": "sonnenuhr", "name": "Sonnenuhr", "rect": (228, 102, 26, 26), "walk_to": (226, 128),
         "actions": {"look": ["say:Eine Sonnenuhr. Aber der Schatten fällt im Mondlicht...",
                              "say:...genau auf 23:13. Und er bewegt sich nicht."],
                     "push": "Die ist fest einbetoniert."}},
        {"id": "gartenhaus", "name": "Gärtnerhäuschen", "rect": (284, 46, 36, 60), "walk_to": (300, 116),
         "default": "walk",
         "actions": {"look": "Ein kleines Gärtnerhäuschen. Drinnen brennt eine Laterne.",
                     "walk": "goto:garden_shed", "open": "goto:garden_shed"}},
        {"id": "zurueck", "name": "Zurück zum Tor", "rect": (0, 100, 20, 44), "walk_to": (4, 128),
         "default": "walk",
         "actions": {"walk": {"if": "flag:gate_open", "do": "goto:gate:160,124",
                              "else": "goto:gate:40,120"}}},
    ],
}
