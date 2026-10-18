"""Die spielbaren Figuren.

'sprite'  – Farben für die Platzhalter-Grafik ('long_hair' für lange Haare).
'actions' – was passiert, wenn eine *andere* Figur diese Figur anschaut,
            anspricht usw. (gleiches Format wie bei Hotspots).
"""

CHARACTERS = {
    "patrick": {
        "name": "Patrick",
        "role": "Anführer",
        "ability": "Mutig – geht vor, wenn alle anderen zögern",
        "text_color": "#ffd866",
        "sprite": {"skin": "#f1c27d", "hair": "#6b3e1f", "cap": "#c0392b",
                   "jacket": "#2e6f9e", "pants": "#34405e", "shoes": "#eeeeee"},
        "actions": {
            "look": "Patrick. Unser Anführer. Sagt er jedenfalls.",
            "talk": "sayas:patrick:Bleibt dicht zusammen, okay?",
        },
    },
    "ida": {
        "name": "Ida", "role": "Bücherwurm",
        "ability": "Liest alte Schriften und Formeln",
        "text_color": "#ff9ecb",
        "sprite": {"skin": "#e0ac69", "hair": "#2b1b10", "cap": None, "long_hair": True,
                   "jacket": "#7d3c98", "pants": "#3b3b3b", "shoes": "#6b4226"},
        "actions": {
            "look": "Ida. Hat jedes Buch der Stadtbücherei gelesen. Angeblich zweimal.",
            "talk": "sayas:ida:Weißt du, was mich stört? Der Brief ist von 1958, aber die Tinte sieht ganz frisch aus.",
        },
    },
    "kemal": {
        "name": "Kemal", "role": "Technikfreak",
        "ability": "Repariert Geräte und knackt Schlösser",
        "text_color": "#9be7ff",
        "sprite": {"skin": "#c68642", "hair": "#111111", "cap": None,
                   "jacket": "#d35400", "pants": "#2c3e50", "shoes": "#222222"},
        "actions": {
            "look": "Kemal. Hat immer einen Schraubenzieher im Rucksack.",
            "talk": "sayas:kemal:Wenn da drin Licht brennt, will ich wissen, woher der Strom kommt. Die Leitung ist seit Jahrzehnten tot.",
        },
    },
    "merle": {
        "name": "Merle", "role": "Fotografin",
        "ability": "Ihre Sofortbildkamera zeigt Unsichtbares",
        "text_color": "#b6ff8a",
        "sprite": {"skin": "#f5d0a9", "hair": "#d4a017", "cap": None, "long_hair": True,
                   "jacket": "#16a085", "pants": "#5d4037", "shoes": "#aa3333"},
        "actions": {
            "look": "Merle. Ihre Sofortbildkamera hängt ihr immer um den Hals.",
            "talk": "sayas:merle:Noch neun Bilder im Film. Ich muss sparsam sein.",
        },
    },
    "finn": {
        "name": "Finn", "role": "Funker",
        "ability": "Hört mit dem Walkie-Talkie, was andere nicht hören",
        "text_color": "#ffb366",
        "sprite": {"skin": "#f1c27d", "hair": "#c0601a", "cap": "#27ae60",
                   "jacket": "#7f8c8d", "pants": "#1f3a5f", "shoes": "#333333"},
        "actions": {
            "look": "Finn. Zwei Walkie-Talkies und einen Kopf voller Frequenzen.",
            "talk": "sayas:finn:Kanal 9 rauscht komisch. Fast wie... ein Ticken.",
        },
    },
    "lena": {
        "name": "Lena", "role": "Turnerin",
        "ability": "Klettert über alles und passt durch enge Stellen",
        "text_color": "#c9a0ff",
        "sprite": {"skin": "#8d5524", "hair": "#1a1a1a", "cap": None, "long_hair": True,
                   "jacket": "#e74c3c", "pants": "#222244", "shoes": "#ffffff"},
        "actions": {
            "look": "Lena. Turnt im Verein und klettert auf alles, was nicht wegläuft.",
            "talk": "sayas:lena:Wenn's brenzlig wird: Ich bin schneller weg als ihr alle.",
        },
    },

    # --- Nicht spielbare Figuren (npc) -----------------------------------
    "anselm": {
        "name": "Herr Brack", "npc": True,
        "text_color": "#c8e6c9",
        "sprite": {"skin": "#e8d5c0", "hair": "#bbbbbb", "cap": "#4a5a3a", "ghost": True,
                   "jacket": "#5d6b4a", "pants": "#4a3a2a", "shoes": "#2a2a2a"},
        "actions": {
            "look": "Ein alter Mann mit grüner Schürze. Er ist... ein kleines bisschen durchsichtig.",
            "talk": "dialog:anselm",
            "take": "Lieber nicht anfassen.",
        },
    },
    "ottilie": {
        "name": "Gestalt", "npc": True,
        "text_color": "#a8e8ff",
        "sprite": {"skin": "#f0dcc8", "hair": "#eeeeee", "cap": None, "long_hair": True,
                   "ghost": True, "goggles": "#7fd8ff",
                   "jacket": "#e8e8e8", "pants": "#555566", "shoes": "#333333"},
        "actions": {"look": "Sie flimmert wie ein schlecht eingestellter Fernseher."},
    },
    "tick": {
        "name": "Tick", "npc": True,
        "text_color": "#ffcc66",
        "sprite": {"skin": "#c8a040", "hair": "#a08030", "cap": None, "goggles": "#ff6040",
                   "jacket": "#1a1a1a", "pants": "#1a1a1a", "shoes": "#c8a040"},
        "actions": {
            "look": {"if": "flag:tick_awake",
                     "do": "Tick, der mechanische Butler. Er tickt leise vor sich hin.",
                     "else": "Ein Butler aus Messing, im Frack. Er steht völlig still. Im Rücken ist ein Schlitz."},
            "talk": {"if": "flag:tick_awake", "do": "dialog:tick",
                     "else": "Hallo? ...Nichts. Der ist abgelaufen wie ein Wecker."},
            "push": "Puh! Der wiegt bestimmt zwei Zentner.",
            "use:schluessel": {"if": "flag:tick_awake", "do": "Der läuft schon.",
                               "else": ["say:Mal sehen, ob der passt...", "drop:schluessel",
                                        "sound:tick", "set:tick_awake", "dialog:tick"]},
        },
    },
}
