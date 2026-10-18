"""Dialogbäume.

Ein Dialog besteht aus Knoten; jeder Knoten hat Antwortmöglichkeiten:
  "text"  – was die aktive Figur sagt (wird automatisch gesprochen)
  "if"    – nur anzeigen, wenn die Bedingung gilt
  "once"  – nach einmaliger Wahl ausblenden
  "do"    – Aktion danach (meist die Antwort des Gegenübers)
  "goto"  – zu einem anderen Knoten wechseln (sonst bleibt man im Knoten)
  "end"   – Gespräch beenden
"intro" eines Knotens läuft jedes Mal, wenn der Knoten betreten wird.
"""

DIALOGS = {
    "anselm": {
        "start": "hallo",
        "nodes": {
            "hallo": {
                "intro": {"if": "!flag:anselm_met",
                          "do": ["set:anselm_met",
                                 "sayas:anselm:Oh. Besuch. Das hatten wir lange nicht.",
                                 "sayas:anselm:Passt auf die Rosen auf, die sind gerade frisch gegossen."]},
                "options": [
                    {"text": "Wer sind Sie?", "once": True,
                     "do": ["sayas:anselm:Anselm Brack. Gärtner im Hause Grauweide, seit 1952.",
                            "sayas:anselm:Morgen ist der 1. November 1958. Dann sind es schon sechs Jahre.",
                            "Äh... wir haben 1987.",
                            "sayas:anselm:Unsinn. Die Frau Professor sagt, die Uhr ist gleich fertig. Nur noch eine Sekunde.",
                            "set:anselm_who"]},
                    {"text": "Was ist mit Professorin Grauweide?", "if": "flag:anselm_who",
                     "goto": "professorin"},
                    {"text": "Wie kommen wir ins Haus?", "goto": "haus"},
                    {"text": "Dürfen wir uns Ihre Leiter leihen?", "if": "!flag:anselm_ladder",
                     "do": {"if": "flag:anselm_hint",
                            "do": ["sayas:anselm:Für das Fenster? Nehmt sie ruhig.",
                                   "sayas:anselm:Ich brauch sie nicht. Die Rosen sind jeden Tag gleich hoch.",
                                   "set:anselm_ladder"],
                            "else": "sayas:anselm:Wozu denn? Erst sagt ihr mir, was ihr vorhabt."}},
                    {"text": "Sie sind ein bisschen... durchsichtig.", "if": "flag:anselm_who", "once": True,
                     "do": ["sayas:anselm:Das ist die Nachtluft. Da sieht jeder blass aus.",
                            "sayas:anselm:...Oder?"]},
                    {"text": "Tschüss, Herr Brack.", "end": True,
                     "do": "sayas:anselm:Kommt wieder vorbei. Ich bin immer hier. Immer."},
                ],
            },
            "professorin": {
                "options": [
                    {"text": "Woran arbeitet sie?", "once": True,
                     "do": ["sayas:anselm:An der großen Uhr oben im Turm.",
                            "sayas:anselm:Sie sagt, wenn die fertig ist, muss nie wieder jemand Abschied nehmen."]},
                    {"text": "Abschied von wem?", "once": True,
                     "do": ["sayas:anselm:Ihr Bruder ist im Frühjahr gestorben. Seitdem schläft sie kaum noch.",
                            "sayas:anselm:Das sollte ich euch wohl gar nicht erzählen."]},
                    {"text": "Haben Sie sie heute gesehen?", "once": True,
                     "do": ["sayas:anselm:Gerade eben. Sie hat aus dem Turmfenster gewunken.",
                            "sayas:anselm:Das macht sie jeden Abend um dieselbe Zeit."]},
                    {"text": "Etwas anderes...", "goto": "hallo"},
                ],
            },
            "haus": {
                "intro": "sayas:anselm:Die Haustür hat kein Schlüsselloch. Die Frau Professor mag Rätsel.",
                "options": [
                    {"text": "Was für ein Rätsel?",
                     "do": ["sayas:anselm:Sie sagt immer: Die Tür öffnet sich zu der Stunde, die nie vergeht.",
                            "sayas:anselm:Fragt mich nicht, was das heißt. Ich bin Gärtner."]},
                    {"text": "Gibt es noch einen anderen Weg?",
                     "do": ["sayas:anselm:Das Fenster rechts neben der Tür klemmt seit Jahren und geht nie ganz zu.",
                            "sayas:anselm:Aber ohne Leiter kommt da keiner hoch.",
                            "sayas:anselm:Und der alte Kohlenschacht... da passt höchstens ein Eichhörnchen durch.",
                            "set:anselm_hint"]},
                    {"text": "Danke.", "goto": "hallo"},
                ],
            },
        },
    },
}
