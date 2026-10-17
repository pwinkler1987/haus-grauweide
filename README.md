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
| Tab / Porträt-Knöpfe | Figur wechseln |
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

### Aktionen

| Befehl | Wirkung |
|---|---|
| `"Text"` / `"say:Text"` | aktive Figur spricht |
| `"sayas:ida:Text"` | eine bestimmte Figur spricht |
| `"narrate:Text"` | Erzähltext-Box (Klick zum Weiter) |
| `"set:flag"` / `"unset:flag"` | Flag setzen/löschen |
| `"take:item"` / `"drop:item"` | Gegenstand ins/aus dem Inventar der aktiven Figur |
| `"goto:raum[:x,y]"` | aktive Figur wechselt den Raum |
| `"party_goto:raum"` | alle Gruppenmitglieder im Raum ziehen gemeinsam weiter |
| `"place:figur:raum[:x,y]"` / `"remove:figur"` | Figur platzieren / entfernen |
| `"choose:2"` | Charakterwahl-Bildschirm |
| `"sound:name"` / `"wait:ms"` | Klang (static, melody, click, owl) / Pause |

Listen von Aktionen laufen nacheinander. Bedingt: `{"if": …, "do": …, "else": …}` mit
`flag:x`, `has:item`, `char:figur` (wird gespielt), `party:figur` (ist dabei),
`here:2` (mind. 2 aus der Gruppe im Raum) – mit `!` verneint, als Liste UND-verknüpft.

Jede Figur hat ein eigenes Inventar; mit „Gib X an <Figur>“ wandern Gegenstände weiter.
