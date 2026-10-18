"""Die Turmtreppe – hier steht die Zeit schon still. Konrads Taschenuhr hängt mitten im Fall."""

STONE, STONE_LINE = "#22222a", "#1a1a20"
STEP, STEP_EDGE = "#3a3530", "#4a4540"
FROZEN = "#9fb0d0"


def spiral_steps():
    """Wendeltreppe von links unten nach rechts oben."""
    out = []
    for i in range(11):
        x = 40 + i * 24
        y = 104 - i * 9
        out += [("poly", [(x, y), (x + 30, y - 4), (x + 30, y + 2), (x, y + 8)], STEP),
                ("line", x, y, x + 30, y - 4, STEP_EDGE)]
    return out


DRAW = [
    ("rect", 0, 0, 320, 144, STONE),
    *[("rect", 0, y, 320, 1, STONE_LINE) for y in range(8, 112, 10)],
    *[("rect", x + (y // 10 % 2) * 10, y, 1, 10, STONE_LINE)
      for y in range(8, 112, 10) for x in range(0, 320, 20)],
    # Rundung der Turmwand: dunkle Ränder
    ("rect", 0, 0, 16, 144, "rgba(0,0,0,0.35)"), ("rect", 304, 0, 16, 144, "rgba(0,0,0,0.35)"),
    ("rect", 0, 112, 320, 32, "#2a2620"),
    *spiral_steps(),
    # Fensterschlitz mit Mondlicht und erstarrten Regentropfen
    ("rect", 58, 24, 10, 30, "#0b1030"), ("circle", 63, 32, 2, "#e8e4c0"),
    ("poly", [(58, 54), (68, 54), (110, 104), (60, 104)], "rgba(200,216,255,0.06)"),
    *[("rect", x, y, 1, 3, FROZEN) for x, y in
      ((72, 36), (80, 44), (76, 58), (88, 50), (94, 66), (84, 72), (100, 60), (70, 80), (92, 84))],
    # Motte, mitten im Flug erstarrt
    ("poly", [(226, 34), (214, 28), (218, 42), (226, 38), (234, 42), (238, 28)], "#cbb9a0"),
    ("rect", 225, 30, 2, 10, "#3a2a20"),
    # Taschenuhr: schwebend oder auf der Stufe
    {"if": "!flag:watch_fallen", "shapes": [
        ("circle", 150, 58, 10, "rgba(127,216,255,0.15)"),
        ("line", 150, 52, 146, 44, "#c8a040"),
        ("circle", 150, 58, 4, "#c8a040"), ("circle", 150, 58, 2.5, "#f4ecd0"),
    ]},
    {"if": ["flag:watch_fallen", "!flag:got_taschenuhr"], "shapes": [
        ("line", 156, 83, 162, 82, "#c8a040"),
        ("circle", 152, 84, 4, "#c8a040"), ("circle", 152, 84, 2.5, "#f4ecd0"),
    ]},
]

ROOM = {
    "id": "tower_stairs",
    "name": "Turmtreppe",
    "draw": DRAW,
    "walkbox": [(2, 114), (318, 114), (318, 143), (2, 143)],
    "start": (40, 128),
    "on_enter": {
        "if": "!flag:stairs_intro",
        "do": ["set:stairs_intro",
               "say:Hier drin ist es eiskalt.",
               "say:Und still. Als hätte jemand die ganze Welt angehalten."],
    },
    "hotspots": [
        {"id": "runter", "name": "Zur Galerie", "rect": (0, 60, 20, 84), "walk_to": (8, 128),
         "default": "walk", "actions": {"walk": "party_goto:upstairs"}},
        {"id": "fenster", "name": "Fensterschlitz", "rect": (56, 22, 14, 34), "walk_to": (70, 124),
         "actions": {"look": "Draußen der Mond. Er bewegt sich nicht, die Wolken auch nicht."}},
        {"id": "tropfen", "name": "Regentropfen", "rect": (68, 32, 36, 56), "walk_to": (86, 124),
         "actions": {"look": "Regentropfen, die einfach in der Luft hängen. Wie Perlen an unsichtbaren Fäden.",
                     "take": "Meine Finger gehen durch, als wär da nichts. Aber sie bleiben hängen.",
                     "push": "Sie rühren sich nicht."}},
        {"id": "motte", "name": "Motte", "rect": (212, 26, 28, 18), "walk_to": (226, 124),
         "actions": {"look": {"if": "party:finn",
                              "do": ["say:Eine Motte, mitten im Flügelschlag eingefroren.",
                                     "say:Finn würde jetzt was von \"Nacht der Riesenmotte\" erzählen."],
                              "else": "Eine Motte, mitten im Flügelschlag eingefroren."},
                     "take": "Die will ich nicht anfassen."}},
        {"id": "uhr_schwebend", "name": "Taschenuhr", "rect": (140, 42, 20, 26), "walk_to": (150, 124),
         "if": "!flag:watch_fallen",
         "actions": {"look": "Eine goldene Taschenuhr, mitten im Fall erstarrt. Sie schwebt über der Stufe.",
                     "take": "Ich komm nicht dran. Sie steckt in der Zeit fest wie in Glas.",
                     "push": "Sie bewegt sich keinen Millimeter."}},
        {"id": "uhr_liegend", "name": "Taschenuhr", "rect": (144, 76, 22, 14), "walk_to": (156, 124),
         "if": ["flag:watch_fallen", "!flag:got_taschenuhr"],
         "actions": {"look": "Die Taschenuhr ist auf die Stufe gefallen. Sie tickt!",
                     "take": ["take:taschenuhr", "say:Sie tickt... als einziges Ding hier im Turm."]}},
        {"id": "hoch", "name": "Treppe nach oben", "rect": (266, 0, 54, 60), "walk_to": (300, 120),
         "default": "walk",
         "actions": {"look": "Die Treppe führt hinauf in die Uhrenkammer.",
                     "walk": "party_goto:clock_room"}},
    ],
}
