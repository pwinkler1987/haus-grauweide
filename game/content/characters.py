"""Die spielbaren Figuren. 'sprite' enthält die Farben für die Platzhalter-Grafik."""

CHARACTERS = {
    "patrick": {
        "name": "Patrick",
        "role": "Anführer",
        "ability": "Mutig – kann Erwachsene ablenken",
        "text_color": "#ffd866",
        "sprite": {"skin": "#f1c27d", "hair": "#6b3e1f", "cap": "#c0392b",
                   "jacket": "#2e6f9e", "pants": "#34405e", "shoes": "#eeeeee"},
    },
    "ida": {
        "name": "Ida", "role": "Bücherwurm",
        "ability": "Entziffert alte Schriften und Formeln",
        "text_color": "#ff9ecb",
        "sprite": {"skin": "#e0ac69", "hair": "#2b1b10", "cap": None,
                   "jacket": "#7d3c98", "pants": "#3b3b3b", "shoes": "#6b4226"},
    },
    "kemal": {
        "name": "Kemal", "role": "Technikfreak",
        "ability": "Repariert Geräte und Stromkreise",
        "text_color": "#9be7ff",
        "sprite": {"skin": "#c68642", "hair": "#111111", "cap": None,
                   "jacket": "#d35400", "pants": "#2c3e50", "shoes": "#222222"},
    },
    "merle": {
        "name": "Merle", "role": "Fotografin",
        "ability": "Ihre Sofortbildkamera zeigt Unsichtbares",
        "text_color": "#b6ff8a",
        "sprite": {"skin": "#f5d0a9", "hair": "#d4a017", "cap": None,
                   "jacket": "#16a085", "pants": "#5d4037", "shoes": "#a33"},
    },
    "finn": {
        "name": "Finn", "role": "Funker",
        "ability": "Walkie-Talkies und Radiofrequenzen",
        "text_color": "#ffb366",
        "sprite": {"skin": "#f1c27d", "hair": "#c0601a", "cap": "#27ae60",
                   "jacket": "#7f8c8d", "pants": "#1f3a5f", "shoes": "#333333"},
    },
    "lena": {
        "name": "Lena", "role": "Turnerin",
        "ability": "Klettert und passt durch enge Stellen",
        "text_color": "#c9a0ff",
        "sprite": {"skin": "#8d5524", "hair": "#1a1a1a", "cap": None,
                   "jacket": "#e74c3c", "pants": "#222244", "shoes": "#ffffff"},
    },
}
