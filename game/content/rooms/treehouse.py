"""Das Baumhaus – Clubhaus der Freunde. Hier beginnt das Spiel.

Rätselkette:
  Radio einschalten (23:13-Signal) -> Radio öffnen: Batterien
  Kiste öffnen -> Taschenlampe nehmen -> mit Batterien kombinieren
  Fernglas vom Nagel nehmen -> mit Fenster benutzen: Licht in der Villa
  Brief nehmen -> durch die Falltür in den Wald
"""

# --- Farben ----------------------------------------------------------------
WALL, WALL_LINE = "#5a3a22", "#4a2f1b"
FLOOR, FLOOR_LINE = "#6e4a2c", "#5c3d24"
BEAM = "#3a2414"
NIGHT = "#0b1030"
GLOW = "#7fd8ff"


def planks(y0, y1, step, color):
    return [("rect", 0, y, 320, 1, color) for y in range(y0, y1, step)]


# --- Hintergrund -------------------------------------------------------------
# Formen: ("rect", x, y, b, h, farbe) | ("poly", [(x, y), ...], farbe)
#         ("circle", x, y, r, farbe) | ("line", x1, y1, x2, y2, farbe)
#         ("stars", x, y, b, h, anzahl, farbe)
#         {"if": bedingung, "shapes": [...]}  -> nur zeichnen, wenn Bedingung gilt
DRAW = [
    ("rect", 0, 0, 320, 110, WALL),
    *planks(9, 110, 10, WALL_LINE),
    ("rect", 0, 110, 320, 34, FLOOR),
    *planks(116, 144, 7, FLOOR_LINE),
    ("rect", 0, 107, 320, 4, BEAM),
    ("rect", 0, 0, 8, 110, BEAM), ("rect", 312, 0, 8, 110, BEAM),

    # Fenster mit Blick auf den Krähenhügel
    ("rect", 116, 14, 88, 60, BEAM),
    ("rect", 120, 18, 80, 52, NIGHT),
    ("stars", 120, 18, 80, 30, 18, "#c8c8ff"),
    ("circle", 188, 27, 5, "#e8e4c0"),
    ("poly", [(120, 70), (138, 54), (165, 45), (188, 52), (200, 58), (200, 70)], "#141a14"),
    ("rect", 158, 36, 15, 11, "#06080a"),
    ("poly", [(156, 37), (165.5, 29), (175, 37)], "#06080a"),
    ("rect", 169, 28, 3, 6, "#06080a"),
    {"if": "flag:heard_signal", "shapes": [("rect", 161, 39, 2, 2, GLOW)]},
    ("rect", 159, 18, 2, 52, BEAM), ("rect", 120, 43, 80, 2, BEAM),

    # Glühbirne
    ("line", 62, 0, 62, 20, "#222222"),
    ("circle", 62, 24, 12, "rgba(255,210,127,0.12)"),
    ("circle", 62, 23, 3, "#ffd27f"),

    # Fernglas am Nagel
    ("rect", 30, 50, 2, 2, "#999999"),
    {"if": "!flag:got_fernglas", "shapes": [
        ("line", 31, 52, 27, 60, "#222222"), ("line", 31, 52, 35, 60, "#222222"),
        ("rect", 24, 60, 6, 9, "#2b2b2b"), ("rect", 32, 60, 6, 9, "#2b2b2b"),
        ("rect", 25, 67, 4, 2, "#6fa8dc"), ("rect", 33, 67, 4, 2, "#6fa8dc"),
    ]},

    # Filmplakat (erfundener B-Movie)
    ("rect", 234, 18, 44, 56, "#d8c27a"),
    ("rect", 238, 22, 36, 40, "#2d3f5c"),
    ("poly", [(256, 34), (242, 28), (246, 46), (256, 42), (266, 46), (270, 28)], "#cbb9a0"),
    ("rect", 255, 32, 2, 14, "#3a2a20"),
    ("rect", 238, 64, 36, 6, "#8a2a2a"),

    # Tisch mit Radio und Brief
    ("rect", 90, 92, 70, 4, BEAM),
    ("rect", 94, 96, 4, 18, BEAM), ("rect", 152, 96, 4, 18, BEAM),
    ("line", 104, 76, 115, 70, "#222222"), ("line", 115, 70, 126, 76, "#222222"),
    ("rect", 100, 76, 30, 16, "#7a2b2b"),
    ("circle", 108, 84, 5, "#2a1a1a"),
    ("rect", 118, 79, 9, 4, "#d8c890"),
    {"if": "flag:heard_signal", "shapes": [("rect", 121, 79, 1, 4, "#ff3b3b")]},
    {"if": "!flag:got_brief", "shapes": [
        ("rect", 136, 88, 14, 4, "#efe6c8"), ("rect", 141, 89, 3, 2, "#a02020"),
    ]},

    # Kiste
    ("rect", 220, 96, 44, 24, "#7b5530"),
    ("rect", 220, 106, 44, 2, "#5a3d20"),
    {"if": "flag:box_open", "sprite": "treehouse_box_open", "shapes": [
        ("rect", 220, 82, 44, 6, "#5a3d20"),
        ("rect", 222, 96, 40, 4, "#2a1a0e"),
    ]},
    {"if": "!flag:box_open", "sprite": "", "shapes": [("rect", 218, 92, 48, 6, "#8a6238")]},
    {"if": ["flag:box_open", "!flag:got_taschenlampe"], "shapes": [
        ("rect", 232, 92, 14, 4, "#bdbdbd"), ("rect", 246, 91, 3, 6, "#8a8a8a"),
    ]},

    # Falltür mit Leiter
    ("poly", [(30, 124), (80, 124), (86, 140), (24, 140)], "#1e120a"),
    ("rect", 44, 127, 22, 2, "#8a6238"), ("rect", 42, 133, 26, 2, "#8a6238"),
    ("rect", 40, 124, 2, 16, "#8a6238"), ("rect", 68, 124, 2, 16, "#8a6238"),
]

# --- Aktionen ----------------------------------------------------------------
RADIO_ON = {
    "if": "flag:heard_signal",
    "do": "Nur noch Rauschen. Das Signal kommt immer nur um 23:13.",
    "else": [
        "say:Noch ein paar Sekunden...",
        "sound:static",
        "set:heard_signal",
        "narrate:23:13 Uhr.\n\nDas Rauschen bricht ab. Dann, ganz leise: eine Spieluhr.",
        "sound:melody",
        "say:Da ist sie wieder! Jede Nacht dieselbe Melodie.",
        "say:Und jetzt gerade... hat da drüben am Hügel etwas aufgeleuchtet?",
    ],
}

LEAVE = {
    "if": "!has:lampe_an",
    "do": "Ohne funktionierende Taschenlampe gehe ich nachts nicht in den Wald.",
    "else": {
        "if": "!has:brief",
        "do": "Idas Brief sollte ich mitnehmen. Der ist unser einziger Hinweis.",
        "else": {
            "if": "!flag:saw_light",
            "do": "Ich will erst sicher sein, dass am Haus wirklich was los ist. Mit einem Fernglas vielleicht...",
            "else": [
                "say:Los geht's. Die anderen warten am Waldrand.",
                "goto:forest_edge",
            ],
        },
    },
}

ROOM = {
    "id": "treehouse",
    "name": "Das Baumhaus",
    "draw": DRAW,
    "walkbox": [(12, 113), (308, 113), (318, 143), (2, 143)],
    "start": (160, 128),
    "on_enter": {
        "if": "!flag:intro_done",
        "do": [
            "set:intro_done",
            "narrate:Lindenbrück, Herbst 1987.\n\n23:12 Uhr. Im Baumhaus hinter Patricks Elternhaus.",
            "say:Noch eine Minute bis 23:13.",
            "say:Mal sehen, ob das Radio heute Nacht wieder verrückt spielt.",
        ],
    },
    # Spätere Einträge liegen "oben": bei Überlappung gewinnt der letzte.
    "hotspots": [
        {"id": "lampe", "name": "Glühbirne", "rect": (56, 14, 13, 14), "walk_to": (62, 120),
         "actions": {"look": "Die Glühbirne flackert. Passt irgendwie zur Stimmung.",
                     "take": "Dann sitze ich im Dunkeln."}},
        {"id": "fenster", "name": "Fenster", "rect": (116, 14, 88, 60), "walk_to": (160, 118),
         "actions": {
             "look": {"if": "flag:saw_light",
                      "do": "Ganz oben im Haus Grauweide brennt ein bläuliches Licht. Nach dreißig Jahren!",
                      "else": "Ganz hinten auf dem Krähenhügel steht das Haus Grauweide. Mit bloßem Auge sehe ich nicht viel."},
             "open": "Lieber nicht. Es zieht schon genug.",
             "use:fernglas": {"if": "flag:saw_light",
                              "do": "Das Licht brennt immer noch.",
                              "else": ["set:saw_light",
                                       "narrate:Durch das Fernglas:\n\nDas Haus Grauweide. Im obersten Fenster flackert ein bläuliches Licht.\nUnd für einen Moment steht dort eine Gestalt.",
                                       "say:Da ist jemand drin. Oder etwas."]},
         }},
        {"id": "plakat", "name": "Filmplakat", "rect": (234, 18, 44, 56), "walk_to": (256, 120),
         "actions": {"look": "\"Die Nacht der Riesenmotte\". Bester Film aller Zeiten. Finn hat ihn elfmal gesehen.",
                     "take": "Das bleibt hängen. Clubhaus-Regel Nummer eins."}},
        {"id": "fernglas", "name": "Fernglas", "rect": (22, 48, 18, 24), "walk_to": (36, 118),
         "if": "!flag:got_fernglas",
         "actions": {"look": "Opas altes Fernglas hängt am Nagel.",
                     "take": ["take:fernglas", "say:Das könnte nützlich sein."]}},
        {"id": "radio", "name": "Radio", "rect": (100, 70, 30, 22), "walk_to": (115, 120),
         "actions": {
             "look": "Ein altes Kofferradio. Seit einer Woche spielt es jede Nacht um 23:13 eine seltsame Melodie.",
             "push": RADIO_ON,
             "use": RADIO_ON,
             "take": "Das ist zu schwer zum Mitschleppen.",
             "open": {"if": "flag:got_batterien",
                      "do": "Das Batteriefach ist leer.",
                      "else": {"if": "flag:heard_signal",
                               "do": ["take:batterien", "sound:click",
                                      "say:Ich leih mir die Batterien. Das Radio braucht heute keiner mehr."],
                               "else": "Erst will ich hören, ob heute Nacht wieder etwas kommt."}},
             "talk": "Hallo? Ist da jemand? ...Nur Rauschen.",
         }},
        {"id": "brief", "name": "Brief", "rect": (134, 84, 18, 9), "walk_to": (142, 120),
         "if": "!flag:got_brief",
         "actions": {"look": "Der Brief, den Ida gefunden hat. Von 1958!",
                     "take": ["take:brief", "say:Den nehme ich mit."]}},
        {"id": "tisch", "name": "Tisch", "rect": (90, 92, 70, 22), "walk_to": (125, 120),
         "actions": {"look": "Unser Clubtisch. Voller Kerben und Kakaoflecken."}},
        {"id": "kiste", "name": "Kiste", "rect": (216, 84, 52, 36), "walk_to": (242, 124),
         "actions": {
             "look": {"if": ["flag:box_open", "!flag:got_taschenlampe"],
                      "do": "Da liegt ja meine Taschenlampe!",
                      "else": "Unsere Schatzkiste. Comics, Kaugummis und alter Krempel."},
             "open": {"if": "flag:box_open", "do": "Die ist schon offen.",
                      "else": ["set:box_open", "sound:click", "say:Mal sehen, was da drin ist..."]},
             "close": {"if": "flag:box_open", "do": ["unset:box_open", "sound:click"],
                       "else": "Die ist schon zu."},
             "take": "Viel zu schwer.",
         }},
        {"id": "taschenlampe", "name": "Taschenlampe", "rect": (228, 88, 24, 10), "walk_to": (242, 124),
         "if": ["flag:box_open", "!flag:got_taschenlampe"],
         "actions": {"look": "Meine Taschenlampe!",
                     "take": ["take:taschenlampe", "say:Hoffentlich geht die noch."]}},
        {"id": "falltuer", "name": "Falltür", "rect": (24, 122, 62, 20), "walk_to": (55, 128),
         "default": "walk",
         "actions": {"look": "Die Falltür. Darunter führt die Leiter hinunter in den Garten.",
                     "walk": LEAVE, "open": LEAVE, "use": LEAVE}},
    ],
}
