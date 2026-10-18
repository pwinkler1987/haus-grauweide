"""Inventar-Gegenstände.

'icon' wird auf eine 24x16-Pixel-Fläche gezeichnet (gleiche Formen wie in Räumen).
'actions' funktioniert wie bei Hotspots. "use:<anderer_gegenstand>" wird ausgelöst,
wenn zwei Gegenstände kombiniert werden – egal in welcher Reihenfolge.
"""

LETTER_TEXT = (
    "Lindenbrück, 31. Oktober 1958\n\n"
    "An wen auch immer dies findet:\n"
    "Ich bin nicht fort. Ich stecke zwischen zwei Sekunden fest.\n"
    "Die große Uhr lässt mich nicht los.\n\n"
    "Wenn die Radios singen, ist die Wand dünn.\n"
    "Kommt zum Haus Grauweide. Bitte.\n\n"
    "– O. G."
)

DIARY_TEXT = (
    "Tagebuch O. G., 30. Oktober 1958\n\n"
    "Die Uhr ist fast fertig. Wenn ich sie im richtigen Moment anhalte, hält sie alles an –\n"
    "die eine Sekunde, bevor etwas verloren geht.\n\n"
    "Tick soll den Turm bewachen. Die Losung muss etwas sein, das es nicht geben kann:\n"
    "Rosen im November.\n\n"
    "PS: Die Sicherungen spinnen wieder. Ersatz liegt im Schreibtisch."
)

READ_DIARY = ["set:diary_read", "narrate:" + DIARY_TEXT, "say:Rosen im November... Das ist die Losung!"]

LIGHT_UP = ["drop:batterien", "drop:taschenlampe", "take:lampe_an", "sound:click",
            "say:Klick! Sie leuchtet. Perfekt."]

ITEMS = {
    "brief": {
        "name": "Brief",
        "icon": [("rect", 3, 3, 18, 11, "#efe6c8"),
                 ("poly", [(3, 3), (12, 9), (21, 3)], "#cfc3a0"),
                 ("circle", 12, 9, 2, "#a02020")],
        "actions": {
            "look": ["say:Den hat Ida in einem Bibliotheksbuch gefunden.",
                     "narrate:" + LETTER_TEXT,
                     "say:Zwischen zwei Sekunden... was soll das heißen?"],
            "open": "narrate:" + LETTER_TEXT,
        },
    },
    "fernglas": {
        "name": "Fernglas",
        "icon": [("rect", 5, 4, 6, 10, "#2b2b2b"), ("rect", 13, 4, 6, 10, "#2b2b2b"),
                 ("rect", 11, 7, 2, 3, "#555555"),
                 ("rect", 6, 12, 4, 2, "#6fa8dc"), ("rect", 14, 12, 4, 2, "#6fa8dc")],
        "actions": {
            "look": "Opas altes Fernglas. Damit sieht man bis zum Krähenhügel.",
        },
    },
    "taschenlampe": {
        "name": "Taschenlampe",
        "icon": [("rect", 3, 6, 14, 5, "#9a9a9a"), ("rect", 17, 4, 4, 9, "#7a7a7a"),
                 ("rect", 21, 5, 1, 7, "#444444")],
        "actions": {
            "look": "Meine Taschenlampe. Die Batterien sind leider leer.",
            "use": "Klick. Klick. Nichts. Die Batterien sind leer.",
            "use:batterien": LIGHT_UP,
        },
    },
    "batterien": {
        "name": "Batterien",
        "icon": [("rect", 4, 4, 6, 10, "#2a9d55"), ("rect", 5, 3, 4, 1, "#cccccc"),
                 ("rect", 13, 4, 6, 10, "#2a9d55"), ("rect", 14, 3, 4, 1, "#cccccc"),
                 ("rect", 4, 11, 6, 3, "#111111"), ("rect", 13, 11, 6, 3, "#111111")],
        "actions": {
            "look": "Zwei dicke Batterien aus dem Radio. Die sind noch gut.",
        },
    },
    "lampe_an": {
        "name": "Taschenlampe (an)",
        "icon": [("poly", [(21, 6), (24, 2), (24, 14), (21, 11)], "#ffe680"),
                 ("rect", 3, 6, 14, 5, "#9a9a9a"), ("rect", 17, 4, 4, 9, "#7a7a7a")],
        "actions": {
            "look": "Sie leuchtet hell. Jetzt kann es losgehen.",
            "use": "Die ist schon an.",
        },
    },
    "spaten": {
        "name": "Spaten",
        "icon": [("rect", 2, 7, 14, 2, "#8a6238"), ("rect", 1, 5, 3, 6, "#8a6238"),
                 ("poly", [(16, 4), (23, 5), (23, 11), (16, 12)], "#9a9aa2")],
        "actions": {"look": "Ein alter Spaten. Taugt bestimmt auch als Hebel."},
    },
    "leiter": {
        "name": "Leiter",
        "icon": [("rect", 1, 4, 22, 2, "#8a6238"), ("rect", 1, 11, 22, 2, "#8a6238"),
                 *[("rect", x, 6, 2, 5, "#6e4a2c") for x in range(3, 22, 4)]],
        "actions": {"look": "Eine lange Holzleiter. Frag nicht, wie die in meine Jackentasche passt."},
    },
    "tagebuch": {
        "name": "Tagebuch",
        "icon": [("rect", 5, 2, 14, 12, "#5a1a2a"), ("rect", 6, 3, 1, 10, "#3a0a1a"),
                 ("rect", 17, 3, 1, 10, "#efe6c8")],
        "actions": {
            "look": {"if": "char:ida",
                     "do": ["say:Das ist Kurzschrift. Zum Glück hab ich die mal aus Spaß gelernt."] + READ_DIARY,
                     "else": {"if": "party:ida",
                              "do": "Lauter Häkchen und Kringel – Kurzschrift. Ida könnte das lesen. Oder jemand mit einem Lehrbuch.",
                              "else": "Lauter Häkchen und Kringel – Kurzschrift. Mit einem Lehrbuch könnte ich das entziffern."}},
            "open": "Lauter Häkchen und Kringel.",
            "use:lexikon": ["say:Mit dem Lehrbuch... Zeichen für Zeichen... puh."] + READ_DIARY,
        },
    },
    "lexikon": {
        "name": "Kurzschrift-Lehrbuch",
        "icon": [("rect", 5, 2, 14, 12, "#d4a017"), ("rect", 5, 2, 2, 12, "#7a5a20"),
                 ("rect", 9, 6, 8, 1, "#7a5a20"), ("rect", 9, 8, 6, 1, "#7a5a20")],
        "actions": {"look": "\"Lehrbuch der Kurzschrift\", 1949. Damit kann man Kurzschrift entziffern.",
                    "open": "Alle Zeichen, schön erklärt. Jetzt bräuchte ich nur noch etwas zum Entziffern."},
    },
    "sicherung": {
        "name": "Sicherung",
        "icon": [("rect", 7, 3, 10, 10, "#efefef"), ("rect", 9, 1, 6, 2, "#9a9a9a"),
                 ("rect", 9, 13, 6, 2, "#9a9a9a"), ("circle", 12, 8, 2, "#c62828")],
        "actions": {"look": "Eine Porzellansicherung. Darauf steht \"Labor\"."},
    },
    "schluessel": {
        "name": "Aufziehschlüssel",
        "icon": [("rect", 3, 7, 13, 2, "#c8a040"), ("circle", 19, 8, 4, "#c8a040"),
                 ("circle", 19, 8, 2, "#15152a"), ("rect", 3, 5, 2, 6, "#c8a040")],
        "actions": {"look": "Ein großer Messingschlüssel. Wie für ein Uhrwerk – nur riesig."},
    },
    "taschenuhr": {
        "name": "Taschenuhr",
        "icon": [("line", 12, 1, 16, 4, "#c8a040"), ("circle", 12, 9, 6, "#c8a040"),
                 ("circle", 12, 9, 4.5, "#f4ecd0"), ("line", 12, 9, 12, 6, "#222222"),
                 ("line", 12, 9, 14, 10, "#222222")],
        "actions": {"look": ["say:Eine goldene Taschenuhr. Auf dem Deckel eine Gravur:",
                             "say:\"Für Konrad – damit du nie wieder zu spät kommst. Deine O.\""],
                    "open": "Sie tickt. Als einziges Ding im ganzen Turm."},
    },
}
