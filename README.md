# Das Haus Grauweide

Ein Retro-Point-and-Click-Adventure im Stil der späten 80er – eigene Story, eigene Figuren.

## Starten

```bash
python main.py            # öffnet http://localhost:8000
python main.py --port 8080 --no-browser
```

Benötigt nur Python 3.10+ (keine Zusatzpakete) und einen modernen Browser.

## Steuerung

| Eingabe | Wirkung |
|---|---|
| Klick auf Verb, dann Objekt | Aktion ausführen („Schau an Radio“) |
| Benutze/Gib + Gegenstand + Ziel | „Benutze Batterien mit Taschenlampe“ |
| Rechtsklick | Standardaktion (meist „Schau an“) |
| Tasten 1–9 | Verben |
| H | Hotspots anzeigen |
| Leertaste / Klick | Text überspringen |
| F5 / F9 | Speichern / Laden |

## Aufbau

- `game/content/` – **Inhalte in Python**: Figuren, Gegenstände, ein Modul pro Raum.
  Änderungen werden beim Neuladen des Browsers übernommen.
- `game/validate.py` – findet Tippfehler (unbekannte Räume, Gegenstände).
- `game/server.py` – Webserver + Speicher-API.
- `static/js/engine/` – die Engine im Browser (Zeichnen, Laufen, Verben, Skripte, Sound).

## Einen Raum anlegen

Neue Datei `game/content/rooms/mein_raum.py` mit einer Variable `ROOM`
(siehe `treehouse.py` als Vorlage). Ausgänge: `"goto:mein_raum"` oder `"goto:mein_raum:x,y"`.

Aktionen: `"Text"` (Figur spricht), `"narrate:…"`, `"set:flag"`, `"unset:flag"`,
`"take:item"`, `"drop:item"`, `"goto:raum"`, `"sound:static|melody|click"`, `"wait:ms"`,
Listen davon, oder `{"if": "flag:x" | "has:item" | "!…", "do": …, "else": …}`.
