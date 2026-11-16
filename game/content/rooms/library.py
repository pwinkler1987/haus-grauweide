"""Die Bibliothek – Tagebuch, Kurzschrift-Lexikon und die Ersatzsicherung.

Ida liest Kurzschrift direkt; alle anderen brauchen das Lexikon vom obersten Regal
(Rollleiter verschieben – oder Lena klettert einfach so hoch).
"""

WALL, BOARD = "#2a1e18", "#4a2f1b"
BOOK_COLORS = ["#7b1f2a", "#1f4a7b", "#2a6a3a", "#7a5a20", "#4a2a6a", "#6a3a1a", "#3a3a3a"]


def books(x0, x1, y, h=10, seed=0):
    """Eine Reihe Buchrücken unterschiedlicher Breite und Höhe."""
    out, x, i = [], x0, seed
    while x < x1 - 3:
        w = 3 + (i * 7) % 3
        hh = h - (i * 5) % 3
        out.append(("rect", x, y + h - hh, w, hh, BOOK_COLORS[i % len(BOOK_COLORS)]))
        x += w + 1
        i += 1
    return out


def ladder(x):
    return [("line", x, 4, x + 6, 106, "#8a6238"), ("line", x + 12, 4, x + 18, 106, "#8a6238"),
            *[("line", x + 1 + i * 0.6, 10 + i * 10, x + 13 + i * 0.6, 10 + i * 10, "#8a6238") for i in range(10)]]


DRAW = [
    ("rect", 0, 0, 320, 104, WALL),
    ("rect", 0, 4, 320, 1, "#888888"),  # Schiene der Rollleiter
    # Regalbretter und Bücher
    *[("rect", 2, y, 316, 2, BOARD) for y in (22, 46)],
    ("rect", 2, 70, 228, 2, BOARD),
    *books(4, 204, 12, seed=1), *books(218, 316, 12, seed=4),
    *books(4, 316, 36, seed=2),
    *books(4, 118, 60, seed=3), *books(196, 228, 60, seed=5),
    {"if": "!flag:got_lexikon", "shapes": [("rect", 207, 12, 8, 10, "#d4a017"),
                                           ("rect", 208, 15, 6, 1, "#7a5a20")]},
    # Rollleiter (zwei mögliche Positionen)
    {"if": "!flag:ladder_moved", "sprite": "library_ladder_left", "shapes": ladder(56)},
    {"if": "flag:ladder_moved", "sprite": "library_ladder_right", "shapes": ladder(200)},
    # Kamin
    ("rect", 240, 66, 60, 38, "#3a3a42"), ("rect", 250, 76, 40, 28, "#0e0e10"),
    ("rect", 236, 62, 68, 5, "#4a4a52"),
    ("poly", [(254, 104), (262, 98), (272, 101), (284, 97), (288, 104)], "#5a5a5a"),
    # Schreibtisch mit Tagebuch
    ("rect", 120, 84, 72, 4, BOARD),
    ("rect", 124, 88, 64, 18, "#3a2414"),
    ("rect", 142, 92, 28, 8, "#4a2f1b"), ("circle", 156, 96, 1.5, "#c8a040"),
    {"if": "!flag:got_tagebuch", "shapes": [("rect", 150, 80, 13, 4, "#5a1a2a"),
                                            ("rect", 151, 80, 11, 1, "#efe6c8")]},
    ("rect", 174, 74, 3, 10, "#c8a040"), ("circle", 175, 72, 2, "#ffd27f"),  # Kerze
    ("circle", 175, 72, 8, "rgba(255,210,127,0.12)"),
    # Boden & Teppich
    ("rect", 0, 104, 320, 40, "#2e1f14"),
    ("rect", 60, 112, 200, 24, "#3a2a4a"), ("rect", 64, 115, 192, 18, "#4a3a5a"),
    # Tür zurück (links)
    ("rect", 0, 50, 10, 54, "#1a1012"),
]

ROOM = {
    "id": "library",
    "name": "Bibliothek",
    "draw": DRAW,
    "walkbox": [(4, 108), (316, 108), (318, 143), (2, 143)],
    "start": (40, 126),
    "on_enter": {
        "if": "!flag:library_intro",
        "do": ["set:library_intro",
               "say:Bücher bis unter die Decke...",
               {"if": "char:ida", "do": "say:Das ist das Paradies.", "else": "say:Ida würde hier einziehen."}],
    },
    "hotspots": [
        {"id": "tuer", "name": "Tür zur Galerie", "rect": (0, 50, 14, 58), "walk_to": (6, 124),
         "default": "walk", "actions": {"walk": "goto:upstairs:51,116"}},
        {"id": "regale", "name": "Bücherregale", "rect": (2, 8, 316, 66), "walk_to": (100, 116),
         "actions": {"look": {"if": "char:ida",
                              "do": ["say:Physik, Uhrmacherei, Gedichte...",
                                     "say:...und ein ganzes Regal nur über Zeit. Sie hat alles darüber gelesen."],
                              "else": "Hunderte Bücher. Ganz oben glänzt ein goldener Buchrücken."},
                     "take": "Ich such mir nicht wahllos eins raus. Das dauert ja Jahre."}},
        {"id": "leiter_links", "name": "Rollleiter", "rect": (52, 4, 26, 102), "walk_to": (66, 116),
         "if": "!flag:ladder_moved",
         "actions": {"look": "Eine Bibliotheksleiter auf einer Schiene.",
                     "push": ["set:ladder_moved", "say:Hau ruck... sie rollt ganz leicht!"],
                     "use": "Hier oben steht nichts Interessantes. Vielleicht woanders hinschieben?"}},
        {"id": "leiter_rechts", "name": "Rollleiter", "rect": (196, 24, 26, 82), "walk_to": (212, 116),
         "if": "flag:ladder_moved",
         "actions": {"look": "Die Leiter steht jetzt direkt unter dem goldenen Buch.",
                     "push": ["unset:ladder_moved", "say:Und wieder zurück."]}},
        {"id": "lexikon", "name": "Goldenes Buch", "rect": (204, 8, 14, 16), "walk_to": (212, 116),
         "if": "!flag:got_lexikon",
         "actions": {
             "look": "Ganz oben: ein Buch mit goldenem Rücken. \"Lehrbuch der Kurzschrift\".",
             "take": {"if": "char:lena",
                      "do": ["say:Wer braucht schon eine Leiter?", "take:lexikon"],
                      "else": {"if": "flag:ladder_moved",
                               "do": ["say:Die Leiter hoch... vorsichtig... hab's!", "take:lexikon"],
                               "else": "Viel zu hoch. Ganz oben im Regal."}},
         }},
        {"id": "kamin", "name": "Kamin", "rect": (236, 62, 68, 42), "walk_to": (270, 116),
         "actions": {"look": ["say:Kalte Asche. Darin ein halb verbrannter Zettel:",
                              "say:\"...nur eine Sekunde, Konrad. Eine einzige Sekunde mehr...\"",
                              "say:Wer ist Konrad?"]}},
        {"id": "tagebuch", "name": "Tagebuch", "rect": (148, 76, 17, 9), "walk_to": (156, 116),
         "if": "!flag:got_tagebuch",
         "actions": {"look": "Ein Notizbuch mit Ledereinband. Auf dem Deckel: \"O. G. – privat\".",
                     "take": ["take:tagebuch", "say:Privat... aber es ist ein Notfall."]}},
        {"id": "schreibtisch", "name": "Schreibtisch", "rect": (120, 84, 72, 22), "walk_to": (156, 116),
         "actions": {"look": "Ein schwerer Schreibtisch mit einer Schublade.",
                     "open": {"if": "flag:got_sicherung", "do": "Die Schublade ist leer.",
                              "else": ["sound:click", "take:sicherung",
                                       "say:In der Schublade liegt eine Sicherung aus Porzellan. Die nehm ich mit."]},
                     "close": "Ist schon zu."}},
        {"id": "kerze", "name": "Kerze", "rect": (170, 66, 10, 18), "walk_to": (176, 116),
         "actions": {"look": "Die Kerze brennt. Aber sie wird nicht kürzer.",
                     "take": "Die bleibt schön hier, bei den ganzen Büchern."}},
    ],
}
