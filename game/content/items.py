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
}
