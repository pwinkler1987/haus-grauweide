"""Das Labor der Professorin – hier kommt das 23:13-Signal her."""

TILE, LINE = "#2a3a3a", "#223030"

DRAW = [
    ("rect", 0, 0, 320, 104, TILE),
    *[("rect", 0, y, 320, 1, LINE) for y in range(8, 104, 8)],
    *[("rect", x, 0, 1, 104, LINE) for x in range(8, 320, 8)],
    ("rect", 0, 104, 320, 40, "#1e2626"),
    *[("rect", x + (r % 2) * 16, 104 + r * 8, 16, 8, "#243030") for r in range(5) for x in range(0, 320, 32)],
    # Tür zurück
    ("rect", 2, 46, 26, 58, "#4a4a52"), ("rect", 4, 48, 22, 56, "#5a5a62"),
    # Tafel mit Formeln
    ("rect", 40, 16, 74, 44, "#5a3a20"), ("rect", 43, 19, 68, 38, "#1e3a2a"),
    *[("line", 47, y, 47 + w, y, "#cfd8cf") for y, w in ((24, 40), (30, 56), (36, 22), (42, 48), (48, 34))],
    ("circle", 98, 38, 6, "rgba(207,216,207,0.5)"), ("circle", 98, 38, 5, "#1e3a2a"),
    # Werkbank
    ("rect", 36, 80, 84, 4, "#4a3220"), ("rect", 40, 84, 4, 20, "#4a3220"), ("rect", 112, 84, 4, 20, "#4a3220"),
    ("rect", 50, 74, 10, 6, "#7a7a82"), ("rect", 70, 76, 16, 4, "#b87333"), ("circle", 100, 77, 3, "#9aa"),
    # Die Apparatur
    ("rect", 130, 76, 60, 28, "#4a4a52"), ("rect", 134, 80, 52, 4, "#3a3a42"),
    ("rect", 152, 24, 16, 52, "#b87333"),
    *[("rect", 152, y, 16, 1, "#8a5323") for y in range(28, 76, 4)],
    ("circle", 160, 20, 10, "#9aaab0"),
    {"if": "flag:power_on", "shapes": [("circle", 160, 20, 18, "rgba(127,216,255,0.25)"),
                                       ("line", 152, 14, 144, 6, "#7fd8ff"), ("line", 168, 14, 178, 4, "#7fd8ff")]},
    # Sender mit Antenne
    ("line", 254, 0, 254, 60, "#7a7a82"),
    ("rect", 228, 60, 54, 30, "#3a3a3a"), ("rect", 228, 90, 54, 14, "#2a2a2a"),
    ("circle", 240, 72, 5, "#1a1a1a"), ("circle", 256, 72, 5, "#1a1a1a"),
    ("rect", 266, 66, 10, 4, "#d8c890"),
    {"if": "flag:power_on", "shapes": [("rect", 268, 76, 3, 3, "#ff3b3b"), ("rect", 273, 76, 3, 3, "#33ff66")]},
    # Haken mit Aufziehschlüssel
    ("rect", 298, 26, 3, 3, "#888888"),
    {"if": "!flag:got_schluessel", "shapes": [
        ("rect", 298, 29, 2, 12, "#c8a040"), ("circle", 299, 44, 4, "#c8a040"), ("circle", 299, 44, 2, TILE),
    ]},
]

ROOM = {
    "id": "lab",
    "name": "Labor",
    "draw": DRAW,
    "walkbox": [(30, 108), (316, 108), (318, 143), (2, 143)],
    "start": (30, 126),
    "on_enter": {
        "if": "!flag:lab_intro",
        "do": ["set:lab_intro",
               "say:Ein Labor! Alles sieht aus, als wäre sie nur kurz rausgegangen.",
               "sound:static",
               "say:Und da rauscht etwas."],
    },
    "hotspots": [
        {"id": "tuer", "name": "Tür zur Galerie", "rect": (2, 46, 26, 58), "walk_to": (16, 122),
         "default": "walk", "actions": {"walk": "goto:upstairs:280,116"}},
        {"id": "tafel", "name": "Tafel", "rect": (40, 16, 74, 44), "walk_to": (76, 116),
         "actions": {"look": {"if": "char:ida",
                              "do": ["say:Das ist keine normale Physik. Das ist fast ein Gedicht.",
                                     "say:Sie wollte eine einzige Sekunde unendlich lang machen."],
                              "else": "Formeln über Formeln. Und ganz unten, dick unterstrichen: \"1 Sekunde = für immer?\""}}},
        {"id": "werkbank", "name": "Werkbank", "rect": (36, 72, 84, 32), "walk_to": (78, 118),
         "actions": {"look": {"if": "char:kemal",
                              "do": ["say:Zahnräder, Federn, Röhren... Alles handgemacht.",
                                     "say:Die Frau war ein Genie. Ein bisschen ein verrücktes."],
                              "else": "Zahnräder, Federn und Werkzeug. Fein sortiert."},
                     "take": "Da ist nichts, was ich brauche."}},
        {"id": "apparatur", "name": "Apparatur", "rect": (128, 8, 64, 96), "walk_to": (160, 116),
         "actions": {
             "look": {"if": ["char:merle", "!flag:lab_photo"],
                      "do": ["say:Davon brauch ich ein Foto.", "sound:click", "set:lab_photo",
                             "narrate:Auf dem Sofortbild steht die Professorin an der Apparatur.\nSie schaut direkt in die Kamera. Ihr Mund formt ein Wort:\n\n„Hilfe.“",
                             "say:Sie weiß, dass wir hier sind."],
                      "else": "Eine Kupferspule, so groß wie ein Mensch. Oben drauf eine Glaskugel, in der es knistert."},
             "push": "Ganz sicher nicht.",
             "use": "Ich drücke nicht wahllos auf Knöpfe an einer Zeitmaschine.",
         }},
        {"id": "sender", "name": "Sender", "rect": (226, 58, 58, 46), "walk_to": (254, 116),
         "actions": {
             "look": {"if": "char:finn",
                      "do": ["say:Ein Kurzwellensender! Selbstgebaut, Röhrentechnik.",
                             "say:Der sendet auf allen Frequenzen gleichzeitig... DAS ist das 23:13-Signal!",
                             "say:Sie ruft um Hilfe. Jede Nacht. Seit dreißig Jahren."],
                      "else": "Ein großer Kasten mit Röhren und Knöpfen. Eine Antenne führt durch die Decke."},
             "push": {"if": "char:finn", "do": "Lieber nicht abschalten. Das ist ihr einziger Draht nach draußen.",
                      "else": "Ich lass da lieber die Finger von."},
         }},
        {"id": "schluessel", "name": "Aufziehschlüssel", "rect": (292, 24, 14, 26), "walk_to": (296, 116),
         "if": "!flag:got_schluessel",
         "actions": {"look": "Ein großer Messingschlüssel an einem Haken. Wie für ein Uhrwerk, nur riesig.",
                     "take": ["take:schluessel", "say:Wofür der wohl ist?"]}},
    ],
}
