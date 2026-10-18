"""Die Uhrenkammer – das Finale.

  Pendel anstoßen   -> eine Sekunde läuft: Professorin erwacht, Taschenuhr fällt (Treppe)
  Taschenuhr geben  -> sie ist bereit, die Sekunde loszulassen
  Hebel auf LAUFEN  -> mit Zustimmung: gutes Ende; ohne: neutrales Ende (nach Warnung)
  Zeitkern berühren -> schlechtes Ende (nach Warnung)
"""
import math

STONE, BRASS, BRASS_DARK = "#1e1e26", "#8a6a2a", "#5a4418"


def gear(cx, cy, r, teeth, color=BRASS, hub=BRASS_DARK):
    """Ein Zahnrad als Polygon: abwechselnd Zahnspitze und Zahnlücke."""
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        rr = r if i % 4 in (1, 2) else r - 4
        pts.append((round(cx + rr * math.cos(a), 1), round(cy + rr * math.sin(a), 1)))
    return [("poly", pts, color), ("circle", cx, cy, r * 0.55, hub), ("circle", cx, cy, 3, color)]


def clock_face(cx, cy, r):
    marks = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        x, y = cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a)
        marks.append(("rect", round(x) - 1, round(y) - 1, 3, 3, "#1a1a24"))
    return [
        ("circle", cx, cy, r + 8, "rgba(200,216,255,0.10)"),
        ("circle", cx, cy, r, "#3a4660"),
        ("circle", cx, cy, r - 3, "#9fb0d0"),
        *marks,
        # von hinten gesehen: Zeiger gespiegelt – 23:13
        ("line", cx, cy, cx - 1, cy - 26, "#1a1a24"),
        ("line", cx, cy, cx - 12, cy - 12, "#1a1a24"),
    ]


DRAW = [
    ("rect", 0, 0, 320, 144, STONE),
    *[("rect", 0, y, 320, 1, "#18181e") for y in range(10, 104, 12)],
    ("rect", 0, 104, 320, 40, "#2a2018"),
    *[("rect", 0, y, 320, 1, "#221a12") for y in range(110, 144, 7)],
    *clock_face(160, 50, 44),
    *gear(58, 38, 26, 10),
    *gear(98, 82, 12, 6),
    *gear(262, 32, 20, 8),
    *gear(226, 80, 14, 7, "#7a5a22"),
    # Pendel, schräg erstarrt
    ("rect", 150, 0, 20, 6, BRASS_DARK),
    ("line", 160, 6, 186, 92, "#c8a040"), ("line", 161, 6, 187, 92, "#c8a040"),
    ("circle", 188, 96, 9, "#c8a040"), ("circle", 188, 96, 5, "#e0c060"),
    # Hebel-Pult
    ("rect", 22, 72, 32, 32, "#4a4a52"), ("rect", 24, 74, 28, 6, "#3a3a42"),
    ("rect", 25, 75, 12, 4, "#33aa55"), ("rect", 39, 75, 12, 4, "#aa3333"),
    {"if": "!flag:clock_running", "shapes": [("line", 38, 88, 48, 64, "#9a9aa2"), ("circle", 48, 63, 3, "#aa3333")]},
    {"if": "flag:clock_running", "shapes": [("line", 38, 88, 28, 64, "#9a9aa2"), ("circle", 28, 63, 3, "#33aa55")]},
    ("circle", 38, 88, 4, "#2a2a30"),
    # Zeitkern
    ("rect", 268, 86, 24, 18, "#3a3a42"), ("rect", 264, 84, 32, 4, "#4a4a52"),
    ("circle", 280, 70, 16, "rgba(127,216,255,0.18)"),
    ("poly", [(280, 56), (288, 70), (280, 84), (272, 70)], "#7fd8ff"),
    ("poly", [(280, 60), (284, 70), (280, 78), (277, 70)], "#d8f4ff"),
]

LEVER = {
    "if": "flag:ottilie_agrees",
    "do": [
        "say:Okay. Auf LAUFEN.",
        "sound:click", "set:clock_running",
        "sound:tick",
        "sayas:ottilie:Tick...",
        "sayas:ottilie:...tack.",
        "walk:ottilie:150,124",
        "sayas:ottilie:Die nächste Sekunde. Ich hatte vergessen, wie sie sich anfühlt.",
        "sound:melody",
        "end:befreit",
    ],
    "else": {
        "if": "!flag:lever_warned",
        "do": ["set:lever_warned",
               "say:Wenn ich den umlege, läuft die Zeit wieder.",
               "say:Aber was passiert dann mit ihr? Vielleicht sollte ich sie erst fragen."],
        "else": ["say:Egal. Irgendwer muss es ja tun.",
                 "sound:click", "set:clock_running", "sound:static",
                 "sayas:ottilie:Nein! Wartet! Ich bin noch nicht...",
                 "end:ohne_abschied"],
    },
}

CORE = {
    "if": "!flag:core_warned",
    "do": ["set:core_warned",
           "say:Als ich die Hand ausstrecke, wird alles ganz zäh und langsam...",
           "say:Lieber nicht. Das fühlt sich falsch an."],
    "else": ["say:Nur ganz kurz...", "sound:static", "end:stillstand"],
}

ROOM = {
    "id": "clock_room",
    "name": "Uhrenkammer",
    "draw": DRAW,
    "walkbox": [(18, 108), (302, 108), (318, 143), (2, 143)],
    "start": (290, 126),
    "on_enter": {
        "if": "!flag:clock_intro",
        "do": [
            "set:clock_intro",
            "place:ottilie:clock_room:70,122",
            "face:ottilie:right",
            "say:Die große Uhr...",
            "say:Und da! Das ist sie. Professorin Grauweide!",
            "say:Sie bewegt sich nicht. Nicht mal ein Atemzug.",
        ],
    },
    "hotspots": [
        {"id": "runter", "name": "Treppe nach unten", "rect": (302, 70, 18, 74), "walk_to": (312, 128),
         "default": "walk", "actions": {"walk": "party_goto:tower_stairs"}},
        {"id": "zifferblatt", "name": "Zifferblatt", "rect": (116, 6, 88, 88), "walk_to": (160, 118),
         "actions": {"look": "Das Zifferblatt von hinten, im Mondlicht. Spiegelverkehrt steht da: 23:13."}},
        {"id": "zahnraeder", "name": "Zahnräder", "rect": (30, 10, 84, 86), "walk_to": (80, 118),
         "actions": {"look": {"if": "char:kemal",
                              "do": ["say:Die greifen alle perfekt ineinander. Da klemmt nichts.",
                                     "say:Das Ding steht nicht, weil es kaputt ist. Es steht, weil der Hebel es festhält."],
                              "else": "Riesige Messingzahnräder. Sie stehen alle still."},
                     "push": "Viel zu schwer. Und sie hängen alle am Pendel."}},
        {"id": "pendel", "name": "Pendel", "rect": (156, 6, 44, 100), "walk_to": (176, 118),
         "actions": {
             "look": "Ein riesiges Pendel, mitten im Schwung erstarrt.",
             "push": {"if": "!flag:ottilie_awake",
                      "do": ["say:Hau... ruck!", "sound:tick", "set:ottilie_awake", "set:watch_fallen",
                             "narrate:Für eine einzige Sekunde läuft die Zeit.\n\nDas Pendel schwingt. Unten auf der Treppe klirrt etwas.\nUnd die Frau am Hebel blinzelt.",
                             "sayas:ottilie:Wer... wer hat das Pendel bewegt?"],
                      "else": ["sound:tick", "say:Es schwingt einmal und bleibt wieder stehen. Der Hebel hält es fest."]},
         }},
        {"id": "hebel", "name": "Hebel", "rect": (20, 58, 36, 46), "walk_to": (48, 120),
         "actions": {"look": "Ein Messinghebel mit zwei Stellungen: LAUFEN und ANHALTEN. Er steht auf ANHALTEN.",
                     "push": LEVER, "use": LEVER, "open": LEVER}},
        {"id": "zeitkern", "name": "Zeitkern", "rect": (262, 52, 36, 52), "walk_to": (262, 120),
         "actions": {"look": {"if": "char:ida",
                              "do": ["say:Das muss der Kern der Maschine sein.",
                                     "say:In diesem Kristall steckt die eine Sekunde. Ich würde ihn nicht anfassen."],
                              "else": "Ein Kristall, der leise pulsiert. Darin flimmert etwas, das aussieht wie... ein Augenblick."},
                     "take": CORE, "use": CORE, "push": CORE}},
    ],
}
