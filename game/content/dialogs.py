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
    "tick": {
        "start": "wach",
        "nodes": {
            "wach": {
                "intro": {"if": "!flag:tick_met",
                          "do": ["set:tick_met",
                                 "sayas:tick:Tick. Tack. Systeme... bereit.",
                                 "sayas:tick:Guten Abend. Ich bin Tick, Butler des Hauses Grauweide.",
                                 "sayas:tick:Die Frau Professor wünscht nicht gestört zu werden."]},
                "options": [
                    {"text": "Wo ist die Professorin?", "once": True,
                     "do": ["sayas:tick:Im Turm. Seit 23 Uhr, 12 Minuten und 59 Sekunden.",
                            "sayas:tick:Sie sagte, es dauert nur eine Sekunde. Ich warte seither."]},
                    {"text": "Wer hat dich gebaut?", "once": True,
                     "do": ["sayas:tick:Die Frau Professor. 1951.",
                            "sayas:tick:Ich koche Tee, ich staube ab, ich zähle Sekunden. Sehr viele Sekunden."]},
                    {"text": "Wer ist Konrad?", "if": "flag:library_intro", "once": True,
                     "do": ["sayas:tick:Konrad Grauweide. Ihr Bruder. Er hat mir das Schachspielen beigebracht.",
                            "sayas:tick:Er ist im Frühling gegangen. Seitdem baut sie an der Uhr."]},
                    {"text": "Lass uns in den Turm.", "goto": "losung", "if": "!flag:tower_open"},
                    {"text": "Ist der Turm offen?", "if": "flag:tower_open",
                     "do": "sayas:tick:Bitte sehr. Aber gehen Sie leise. Die Zeit ist dort oben... dünn."},
                    {"text": "Bis später, Tick.", "end": True, "do": "sayas:tick:Tick. Tack."},
                ],
            },
            "losung": {
                "intro": "sayas:tick:Nur mit der Losung der Frau Professor.",
                "options": [
                    {"text": "Abrakadabra?", "goto": "wach", "do": "sayas:tick:Falsch."},
                    {"text": "Lass uns einfach durch!", "goto": "wach", "do": "sayas:tick:Falsch. Und unhöflich."},
                    {"text": "Rosen im November.", "if": "flag:diary_read", "end": True,
                     "do": ["sayas:tick:...Korrekt.", "walk:tick:236,118", "sound:click", "set:tower_open",
                            "sayas:tick:Die Tür ist offen. Gehen Sie leise. Die Zeit ist dort oben... dünn."]},
                    {"text": "Äh... die weiß ich gerade nicht.", "goto": "wach",
                     "do": "sayas:tick:Dann kann ich leider nicht helfen. Tick."},
                ],
            },
        },
    },
    "ottilie": {
        "start": "erwacht",
        "nodes": {
            "erwacht": {
                "intro": {"if": "!flag:ottilie_met",
                          "do": ["set:ottilie_met",
                                 "sayas:ottilie:Kinder? Wie seid ihr an Tick vorbeigekommen?",
                                 "sayas:ottilie:Habt ihr meinen Ruf gehört? Ich dachte, den hört nie jemand."]},
                "options": [
                    {"text": "Wir haben Ihren Brief gefunden.", "once": True,
                     "do": ["sayas:ottilie:Den habe ich vor einer Sekunde geschrieben. Oder vor einer Ewigkeit.",
                            "sayas:ottilie:Hier oben ist das dasselbe."]},
                    {"text": "Was ist hier passiert?", "once": True,
                     "do": ["sayas:ottilie:Ich wollte eine Sekunde festhalten.",
                            "sayas:ottilie:Die letzte, in der ich an Konrads Stimme denken konnte, ohne dass es wehtut.",
                            "sayas:ottilie:Die Uhr hat sie festgehalten. Und mich gleich mit."]},
                    {"text": "Wir haben 1987.", "once": True,
                     "do": ["sayas:ottilie:Neunundzwanzig Jahre...",
                            "sayas:ottilie:Und Anselm gießt immer noch die Rosen, nicht wahr? Der Gute."]},
                    {"text": "Kommen Sie mit uns!",
                     "do": {"if": "flag:ottilie_agrees",
                            "do": "sayas:ottilie:Ja. Stellt den Hebel auf LAUFEN. Ich bin bereit.",
                            "else": ["sayas:ottilie:Wenn die Uhr wieder läuft, ist diese Sekunde vorbei.",
                                     "sayas:ottilie:Und mit ihr das Letzte, was ich von Konrad noch habe.",
                                     "sayas:ottilie:Nein. Das kann ich nicht."]}},
                    {"text": "Wer war Konrad?", "once": True,
                     "do": ["sayas:ottilie:Mein kleiner Bruder. Er kam immer zu spät, zu allem.",
                            "sayas:ottilie:Deshalb hab ich ihm eine Taschenuhr geschenkt. Er hat sie nie abgelegt.",
                            "sayas:ottilie:Als ich hier hochgerannt bin, hatte ich sie in der Hand..."]},
                    {"text": "Auf Wiedersehen.", "end": True,
                     "do": "sayas:ottilie:Ich bin hier. Zwischen tick und tack."},
                ],
            },
        },
    },
}
