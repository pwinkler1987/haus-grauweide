"""Die drei Enden. {party} wird durch die Namen der Gruppe ersetzt."""

ENDINGS = {
    "befreit": {
        "title": "Die nächste Sekunde",
        "kind": "gut",
        "text": (
            "Das Pendel schwingt. Unten im Gärtnerhäuschen stellt Anselm Brack seine Gießkanne ab "
            "und betritt zum ersten Mal seit neunundzwanzig Jahren das Haus. "
            "Tick kocht Tee für alle – viel zu starken Tee.\n\n"
            "Im Morgengrauen geht Professorin Ottilie Grauweide mit {party} hinunter nach Lindenbrück. "
            "In der Jackentasche tickt Konrads Uhr.\n\n"
            "Am nächsten Tag steht in der Zeitung: \"Rätselhaftes Radiosignal verstummt\"."
        ),
        "credits": [
            "Das Haus Grauweide",
            "Idee & Hauptfigur: Patrick",
            "Mit dabei: {party}",
            "Gärtner: Anselm Brack · Butler: Tick",
            "Danke fürs Spielen!",
        ],
    },
    "ohne_abschied": {
        "title": "Ohne Abschied",
        "kind": "neutral",
        "text": (
            "Die Zeit reißt los wie ein Gummiband. Neunundzwanzig Jahre fallen auf einmal "
            "auf das Haus Grauweide herab.\n\n"
            "Als der Staub sich legt, sitzt im Turm eine sehr alte Frau und weint. "
            "Die Rosen im Gärtnerhäuschen sind verwelkt, Tick steht still.\n\n"
            "Sie ist frei. Aber sie hat nie Abschied genommen."
        ),
        "credits": ["Vielleicht hätte sie noch etwas gebraucht, um loszulassen..."],
    },
    "stillstand": {
        "title": "Zwischen zwei Sekunden",
        "kind": "schlecht",
        "text": (
            "Der Kristall ist warm. Dann wird alles sehr, sehr langsam.\n\n"
            "Draußen in Lindenbrück spielen die Radios jede Nacht um 23:13 eine Melodie. "
            "Und seit kurzem hört man darin eine zweite Stimme."
        ),
        "credits": ["Manche Dinge sollte man nicht anfassen."],
    },
}
