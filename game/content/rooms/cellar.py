"""Der Keller – nur durch den Kohlenschacht erreichbar (Lena)."""

STONE, STONE_LINE, FLOOR = "#24242a", "#1a1a20", "#1a1814"

DRAW = [
    ("rect", 0, 0, 320, 144, STONE),
    *[("rect", 0, y, 320, 1, STONE_LINE) for y in range(10, 104, 12)],
    *[("rect", x + (y // 12 % 2) * 12, y, 1, 12, STONE_LINE) for y in range(10, 104, 12) for x in range(0, 320, 24)],
    ("rect", 0, 104, 320, 40, FLOOR),
    # Lichtschein der Taschenlampe
    ("circle", 160, 90, 90, "rgba(255,230,150,0.06)"),
    # Schachtöffnung oben links mit Kohlehaufen
    ("rect", 20, 0, 30, 16, "#0a0a0c"),
    ("poly", [(4, 110), (20, 70), (40, 64), (64, 80), (78, 110)], "#0e0e10"),
    *[("circle", x, y, 2, "#1c1c22") for x, y in ((24, 84), (36, 74), (48, 82), (30, 98), (60, 96), (44, 92))],
    # Heizkessel
    ("rect", 120, 40, 50, 64, "#3a2a20"),
    ("circle", 145, 60, 10, "#2a1a10"),
    ("circle", 145, 60, 6, "rgba(255,120,40,0.5)"),
    ("rect", 140, 0, 10, 40, "#2e2e34"),
    # Regal mit Einmachgläsern
    ("rect", 196, 40, 50, 3, "#4a3220"), ("rect", 196, 64, 50, 3, "#4a3220"),
    *[("rect", x, 30, 7, 10, "#7b1f4a") for x in range(200, 244, 10)],
    *[("rect", x, 54, 7, 10, "#c79a2a") for x in range(200, 244, 10)],
    # Sicherungskasten
    ("rect", 88, 26, 22, 30, "#5a5a62"), ("rect", 90, 28, 18, 26, "#3a3a42"),
    *[("rect", 92 + i * 6, 32, 4, 6, "#efefef") for i in range(3)],
    ("rect", 92, 42, 4, 6, "#efefef"), ("rect", 104, 42, 4, 6, "#efefef"),
    {"if": "flag:power_on", "shapes": [("rect", 98, 42, 4, 6, "#efefef"), ("rect", 99, 44, 2, 2, "#33ff66")]},
    {"if": "!flag:power_on", "shapes": [("rect", 98, 42, 4, 6, "#6a5a4a"), ("rect", 99, 44, 2, 1, "#1a1a1a")]},
    # Treppe nach oben (rechts)
    *[("rect", 262 + i * 6, 104 - i * 12, 60, 12, "#2e2a24") for i in range(8)],
    ("rect", 296, 0, 24, 20, "#3a3020"),
]

ROOM = {
    "id": "cellar",
    "name": "Im Keller",
    "draw": DRAW,
    "walkbox": [(76, 110), (300, 110), (318, 143), (40, 143)],
    "start": (90, 128),
    "on_enter": {
        "if": "!flag:cellar_intro",
        "do": ["set:cellar_intro",
               "say:Igitt, Kohlenstaub! Aber ich bin drin.",
               "say:Und ... es ist warm hier unten. Viel zu warm für ein leeres Haus."],
    },
    "hotspots": [
        {"id": "schacht", "name": "Kohlenschacht", "rect": (4, 0, 76, 110), "walk_to": (84, 124),
         "default": "walk",
         "actions": {"look": "Da bin ich runtergerutscht. Hoch geht's auch wieder, wenn ich mich strecke.",
                     "walk": "goto:front_yard:93,124"}},
        {"id": "sicherungen", "name": "Sicherungskasten", "rect": (86, 24, 26, 34), "walk_to": (99, 118),
         "actions": {
             "look": {"if": "flag:power_on", "do": "Alle Sicherungen sitzen. Es summt leise.",
                      "else": "Ein Sicherungskasten. In der Mitte ist eine kaputte Sicherung, darüber steht \"Labor\"."},
             "open": {"if": ["char:kemal", "!flag:power_on"],
                      "do": ["say:Die alte Sicherung ist gar nicht kaputt, nur locker.",
                             "say:Einmal festdrehen...", "sound:click", "set:power_on",
                             "say:...und Strom! Oben ist was angesprungen."],
                      "else": "Ich seh nur, dass die Sicherung für das Labor kaputt ist."},
             "use:sicherung": {"if": "flag:power_on", "do": "Es ist schon Strom da.",
                               "else": ["drop:sicherung", "sound:click", "set:power_on",
                                        "say:Rein damit... Es summt! Irgendwo oben springt etwas an."]},
         }},
        {"id": "kessel", "name": "Heizkessel", "rect": (118, 38, 54, 66), "walk_to": (145, 118),
         "actions": {"look": "Ein uralter Heizkessel. Er glüht. Aber da liegt seit Jahrzehnten keine Kohle drin.",
                     "open": "Autsch, heiß! Lieber nicht.",
                     "push": "Der brummt leise. Fast wie ein Ticken."}},
        {"id": "glaeser", "name": "Einmachgläser", "rect": (196, 26, 50, 42), "walk_to": (220, 118),
         "actions": {"look": "Eingemachtes. Auf dem Etikett: \"Pflaumen, Oktober 1958\". Die sehen ganz frisch aus.",
                     "take": "Pflaumen von 1958? Nein danke."}},
        {"id": "treppe", "name": "Treppe nach oben", "rect": (260, 0, 60, 108), "walk_to": (296, 122),
         "default": "walk",
         "actions": {"look": "Eine steile Steintreppe. Oben ist eine Tür.",
                     "walk": "goto:hall:290,126"}},
    ],
}
