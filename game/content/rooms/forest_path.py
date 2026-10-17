"""Der Waldweg – Nebel, eine Eule und ein umgestürzter Baum.

Rätsel: Über den Baumstamm kommt man nur zu zweit (Räuberleiter),
Lena schafft es auch allein und hilft dann den anderen.
"""

TRUNK, NEEDLES, PATH = "#24170e", "#0b1a0f", "#3b2f22"
FOG = "rgba(200,210,235,0.07)"

CLIMB = {
    "if": "char:lena",
    "do": [
        "say:Kein Problem für mich!",
        "say:Kommt, ich zieh euch hoch.",
        "party_goto:gate",
    ],
    "else": {
        "if": "here:2",
        "do": [
            "say:Räuberleiter! Einer hilft dem anderen hoch.",
            "party_goto:gate",
        ],
        "else": "Allein komme ich da nicht rüber. Ich brauche jemanden, der mir hilft.",
    },
}

DRAW = [
    ("rect", 0, 0, 320, 70, "#070b1c"),
    ("stars", 0, 0, 320, 40, 25, "#a0a0d0"),
    *[("poly", [(x, 92), (x + 22, 18 + (x * 7) % 30), (x + 44, 92)], NEEDLES)
      for x in range(-20, 330, 30)],
    ("rect", 0, 84, 320, 60, "#121c0e"),
    ("poly", [(0, 144), (0, 110), (120, 100), (320, 94), (320, 122), (140, 128), (70, 144)], PATH),
    ("rect", 0, 104, 320, 12, FOG),
    # Bäume im Vordergrund
    ("rect", 36, 0, 14, 112, TRUNK),
    ("rect", 270, 0, 16, 100, TRUNK),
    ("rect", 196, 40, 76, 4, TRUNK),  # Ast mit Eule
    # Eule
    ("circle", 225, 34, 6, "#6b5a44"),
    ("poly", [(219, 30), (220, 25), (223, 29)], "#6b5a44"),
    ("poly", [(231, 30), (230, 25), (227, 29)], "#6b5a44"),
    ("circle", 222, 32, 2, "#ffd84a"), ("circle", 228, 32, 2, "#ffd84a"),
    ("rect", 222, 32, 1, 1, "#000000"), ("rect", 228, 32, 1, 1, "#000000"),
    # umgestürzter Baum quer über dem Weg
    ("poly", [(206, 126), (216, 116), (318, 86), (320, 98), (226, 132)], "#3a2616"),
    ("line", 240, 116, 248, 104, "#3a2616"), ("line", 270, 108, 282, 94, "#3a2616"),
    ("line", 290, 100, 300, 112, "#3a2616"),
    ("circle", 212, 124, 9, "#2d1d10"),  # Wurzelteller
    ("rect", 0, 120, 320, 10, FOG),
]

ROOM = {
    "id": "forest_path",
    "name": "Auf dem Waldweg",
    "draw": DRAW,
    "walkbox": [(0, 112), (200, 104), (214, 122), (140, 143), (0, 143)],
    "start": (40, 130),
    "on_enter": {
        "if": "!flag:path_intro",
        "do": [
            "set:path_intro",
            "say:Nebel. Natürlich ist hier Nebel.",
            "sound:owl",
            "say:Und eine Eule. Fehlt nur noch die Gruselmusik.",
        ],
    },
    "hotspots": [
        {"id": "zurueck", "name": "Zurück zum Waldrand", "rect": (0, 96, 24, 48), "walk_to": (6, 128),
         "default": "walk",
         "actions": {"walk": "party_goto:forest_edge"}},
        {"id": "eule", "name": "Eule", "rect": (216, 22, 20, 20), "walk_to": (196, 112),
         "actions": {
             "look": "Eine Eule. Sie starrt mich an, ohne zu blinzeln.",
             "talk": {"if": "char:finn",
                      "do": ["say:Uhu?", "sound:owl", "say:Sie antwortet auf Kanal Eule. Ich hab's ja immer gesagt."],
                      "else": ["say:Äh... hallo?", "sound:owl"]},
             "take": "Die hat Krallen. Nein danke.",
         }},
        {"id": "weiter", "name": "Weg zum Krähenhügel", "rect": (250, 70, 70, 20), "walk_to": (205, 110),
         "default": "walk",
         "actions": {"look": "Hinter dem Baumstamm geht der Weg weiter bergauf.", "walk": CLIMB}},
        {"id": "baum", "name": "Umgestürzter Baum", "rect": (204, 86, 116, 48), "walk_to": (200, 120),
         "default": "walk",
         "actions": {
             "look": "Ein riesiger Baum liegt quer über dem Weg. Zu hoch, um einfach drüberzusteigen.",
             "push": "Der rührt sich keinen Millimeter.",
             "walk": CLIMB, "use": CLIMB,
         }},
    ],
}
