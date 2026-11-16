"""Das Tor zum Haus Grauweide.

Wege aufs Grundstück (jede Gruppe schafft es, Fähigkeiten sind Abkürzungen):
  - alle:  Hecke mit eingeschalteter Taschenlampe ansehen -> Lücke
  - Kemal: Vorhängeschloss öffnen -> Tor auf
  - Lena:  klettert übers Tor
Bonus: Ida liest das Schild, Merle fotografiert die Villa, Finn hört das Signal.
"""

SKY, HILL, HOUSE = "#0a0f26", "#111a10", "#0c0f14"
HEDGE, HEDGE_TOP = "#0f2a14", "#133318"
STONE = "#4a4a52"

ENTER_YARD = "goto:front_yard"

DRAW = [
    ("rect", 0, 0, 320, 144, SKY),
    ("stars", 0, 0, 320, 40, 35, "#c8c8ff"),
    ("circle", 40, 18, 7, "#e8e4c0"),
    ("poly", [(0, 70), (80, 40), (240, 36), (320, 64), (320, 100), (0, 100)], HILL),
    # Villa
    ("rect", 110, 18, 100, 32, HOUSE),
    ("poly", [(104, 20), (160, 2), (216, 20)], HOUSE),
    ("rect", 186, 2, 14, 24, HOUSE),
    ("poly", [(184, 3), (193, -8), (202, 3)], HOUSE),
    *[("rect", x, 30, 6, 8, "#151a22") for x in range(118, 206, 14)],
    ("rect", 190, 8, 5, 7, "#7fd8ff"),
    ("poly", [(150, 100), (170, 100), (164, 50), (156, 50)], "#2a241c"),  # Weg zum Haus
    # Boden
    ("rect", 0, 96, 320, 48, "#141d10"),
    ("poly", [(130, 144), (190, 144), (176, 108), (144, 108)], "#3b2f22"),
    # Hecken
    ("rect", 0, 62, 114, 46, HEDGE),
    ("rect", 206, 62, 114, 46, HEDGE),
    *[("circle", x, 62, 7, HEDGE_TOP) for x in range(4, 114, 12)],
    *[("circle", x, 62, 7, HEDGE_TOP) for x in range(212, 320, 12)],
    {"if": "flag:hedge_found", "sprite": "gate_hedge_hole", "shapes": [
        ("poly", [(28, 108), (30, 88), (40, 82), (50, 88), (52, 108)], "#040704"),
    ]},
    # Pfeiler mit Schild
    ("rect", 112, 44, 14, 64, STONE), ("rect", 110, 40, 18, 6, "#5a5a62"),
    ("rect", 194, 44, 14, 64, STONE), ("rect", 192, 40, 18, 6, "#5a5a62"),
    ("rect", 114, 60, 10, 8, "#6b5a2a"),
    # Tor: geschlossen mit Kette, oder offen
    {"if": "!flag:gate_open", "sprite": "gate_closed", "shapes": [
        *[("rect", x, 52, 2, 56, "#1d1d22") for x in range(129, 194, 6)],
        ("rect", 126, 56, 68, 2, "#1d1d22"), ("rect", 126, 100, 68, 2, "#1d1d22"),
        ("rect", 148, 78, 24, 2, "#777777"),
        ("rect", 157, 80, 7, 7, "#8a7a3a"),
    ]},
    {"if": "flag:gate_open", "sprite": "gate_open", "shapes": [
        *[("rect", x, 52, 2, 56, "#1d1d22") for x in range(129, 140, 5)],
        *[("rect", x, 52, 2, 56, "#1d1d22") for x in range(182, 194, 5)],
    ]},
]

ROOM = {
    "id": "gate",
    "name": "Am Tor",
    "draw": DRAW,
    "walkbox": [(0, 112), (320, 112), (320, 143), (0, 143)],
    "start": (240, 128),
    "on_enter": {
        "if": "!flag:gate_intro",
        "do": [
            "set:gate_intro",
            "say:Da ist es. Das Haus Grauweide.",
            "say:Von Nahem sieht es noch viel größer aus.",
        ],
    },
    "hotspots": [
        {"id": "villa", "name": "Haus Grauweide", "rect": (104, 0, 112, 46), "walk_to": (160, 116),
         "actions": {"look": {
             "if": ["char:merle", "!flag:ghost_photo"],
             "do": ["say:Ich mach ein Foto!", "sound:click", "set:ghost_photo",
                    "narrate:Das Sofortbild entwickelt sich langsam...\n\nIm leuchtenden Turmfenster steht eine Frau mit Schutzbrille.\nIn echt ist da niemand.",
                    "say:Das... war eben noch nicht da."],
             "else": {
                 "if": ["char:finn", "!flag:finn_signal"],
                 "do": ["say:Mein Walkie-Talkie rauscht...", "set:finn_signal", "sound:melody",
                        "say:Die Melodie aus dem Radio! Das Signal kommt direkt aus dem Haus."],
                 "else": "Ein Turm, viele dunkle Fenster und ein einziges Licht.",
             },
         }}},
        {"id": "hecke", "name": "Hecke", "rect": (0, 56, 110, 52), "walk_to": (40, 116),
         "actions": {"look": {
             "if": "flag:hedge_found", "do": "Da ist die Lücke. Eng, aber machbar.",
             "else": {"if": "has:lampe_an",
                      "do": ["set:hedge_found", "say:Moment... im Lichtkegel sehe ich eine Lücke in der Hecke!"],
                      "else": {"if": "party:patrick",
                               "do": "Eine dichte, dunkle Hecke. Ohne Licht sehe ich gar nichts. Patrick hat doch die Taschenlampe...",
                               "else": "Eine dichte, dunkle Hecke. Ohne Licht sehe ich gar nichts."}},
         }}},
        {"id": "luecke", "name": "Lücke in der Hecke", "rect": (26, 80, 28, 28), "walk_to": (40, 114),
         "if": "flag:hedge_found", "default": "walk",
         "actions": {"look": "Eng, aber da passe ich durch.", "walk": ENTER_YARD, "use": ENTER_YARD}},
        {"id": "schild", "name": "Schild", "rect": (112, 58, 14, 12), "walk_to": (119, 116),
         "actions": {"look": {
             "if": "char:ida",
             "do": ["say:Das ist alte deutsche Schreibschrift. Da steht:",
                    "say:\"Hier ruht die Zeit. Wer eintritt, bringe Geduld mit.\"",
                    "say:Na, das ist ja beruhigend."],
             "else": {"if": "party:ida",
                      "do": "Verschnörkelte alte Schrift. Ida könnte das bestimmt lesen.",
                      "else": "Verschnörkelte alte Schrift. Kann ich nicht lesen."},
         }}},
        {"id": "schloss", "name": "Vorhängeschloss", "rect": (154, 76, 12, 12), "walk_to": (160, 116),
         "if": "!flag:gate_open",
         "actions": {
             "look": "Ein altes Vorhängeschloss an einer schweren Kette. Total verrostet.",
             "open": {"if": "char:kemal",
                      "do": ["say:Moment, ich hab da was im Rucksack...", "sound:click", "wait:500",
                             "sound:click", "set:gate_open", "say:Offen! Rost ist auch nur Physik."],
                      "else": {"if": "party:kemal",
                               "do": "Ohne Werkzeug krieg ich das nicht auf. Kemal hat doch immer Werkzeug dabei...",
                               "else": "Ohne Werkzeug krieg ich das nicht auf."}},
             "take": "Das hängt fest an der Kette.",
         }},
        {"id": "tor", "name": "Tor", "rect": (126, 48, 68, 60), "walk_to": (160, 116),
         "actions": {
             "look": {"if": "flag:gate_open", "do": "Das Tor steht offen.",
                      "else": "Ein schmiedeeisernes Tor, mit einer Kette verschlossen."},
             "open": {"if": "flag:gate_open", "do": "Ist schon offen.",
                      "else": "Die Kette hält es zu."},
             "walk": {"if": "flag:gate_open", "do": ENTER_YARD,
                      "else": {"if": "char:lena",
                               "do": ["say:Ein Tor? Für eine Turnerin ist das ein Klettergerüst.", ENTER_YARD],
                               "else": "Verschlossen. Zum Drüberklettern ist es zu hoch."}},
         }},
        {"id": "zurueck", "name": "Zurück in den Wald", "rect": (296, 100, 24, 44), "walk_to": (314, 128),
         "default": "walk",
         "actions": {"walk": "party_goto:forest_path"}},
    ],
}
