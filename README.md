# Das Haus Grauweide

Ein Retro-Point-and-Click-Adventure im Stil der späten 80er – eigene Story, eigene Figuren.

## Starten

```bash
python main.py            # öffnet http://localhost:8000
python main.py --port 8080 --no-browser
```

Benötigt nur Python 3.10+ (keine Zusatzpakete) und einen modernen Browser.

## iOS- und Android-App

Die Apps verpacken dasselbe Spiel mit [Capacitor](https://capacitorjs.com).
`tools/build_web.py` baut daraus eine statische Seite in `www/`: `static/` plus
die Python-Inhalte als `data.json`. Ein Server wird nicht gebraucht, Spielstände
liegen auf dem Gerät.

```bash
npm install          # einmalig (Node 22+)
npm run sync         # www/ bauen und in android/ und ios/ kopieren
npm run android      # … und Android Studio öffnen
npm run ios          # … und Xcode öffnen (nur macOS)
```

Android-Build ohne Android Studio: `cd android && ./gradlew assembleDebug`
(Windows: `gradlew.bat assembleDebug`, braucht JDK 21).
App-ID: `de.pwinkler.grauweide`, nur Querformat.

## Steuerung

| Eingabe | Wirkung |
|---|---|
| Klick auf Verb, dann Objekt | Aktion ausführen („Schau an Radio“) |
| Benutze/Gib + Gegenstand + Ziel | „Benutze Batterien mit Taschenlampe“ |
| Rechtsklick / lange drücken | Standardaktion (meist „Schau an“) |
| Tasten 1–9 | Verben |
| Tab / Porträt-Knöpfe | Figur wechseln |
| H | Hotspots anzeigen |
| Leertaste / Klick | Text überspringen |
| F5 / F9 | Speichern / Laden |
| ☰ (oben links) | Menü: Speichern, Laden, Hotspots, Neues Spiel (Android: Zurück-Taste) |

## Aufbau

- `game/content/` – **Inhalte in Python**: Figuren, Gegenstände, ein Modul pro Raum.
  Änderungen werden beim Neuladen des Browsers übernommen.
- `game/content/dialogs.py` – Dialogbäume (Knoten, Antworten, Bedingungen).
- `game/content/endings.py` – die drei Enden mit Abspann.
- `game/validate.py` – findet Tippfehler (unbekannte Räume, Gegenstände).
- `game/server.py` – Entwicklungs-Webserver (liefert `data.json` immer frisch).
- `tools/build_web.py` – baut `www/` für die Apps.
- `android/`, `ios/` – native Projekte (Capacitor).
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
| `"dialog:anselm"` | Dialogbaum starten (siehe `game/content/dialogs.py`) |
| `"walk:figur:x,y"` / `"face:figur:left"` | Figur in einer Zwischensequenz bewegen / drehen |
| `"codelock:2313:flag"` | Zahlenschloss; bei richtigem Code wird das Flag gesetzt |
| `"end:befreit"` | Ende-Bildschirm mit Abspann (siehe `game/content/endings.py`) |
| `"sound:name"` / `"wait:ms"` | Klang (static, melody, click, owl, tick) / Pause |

Listen von Aktionen laufen nacheinander. Bedingt: `{"if": …, "do": …, "else": …}` mit
`flag:x`, `has:item`, `char:figur` (wird gespielt), `party:figur` (ist dabei),
`here:2` (mind. 2 aus der Gruppe im Raum) – mit `!` verneint, als Liste UND-verknüpft.

Jede Figur hat ein eigenes Inventar; mit „Gib X an <Figur>“ wandern Gegenstände weiter.

Nicht spielbare Figuren stehen ebenfalls in `characters.py` (mit `"npc": True`);
`"ghost": True` im Sprite macht sie halb durchsichtig. Was ein NPC mit einem
geschenkten Gegenstand macht, steht in seinen Aktionen unter `"give:<gegenstand>"`.

## Die Geschichte (Spoiler!)

Baumhaus → Waldrand (Gruppe wählen) → Waldweg → Tor → Vorgarten → Halle
→ Obergeschoss (Bibliothek, Labor, Butler Tick) → Turmtreppe → Uhrenkammer.

Drei Enden: *Die nächste Sekunde* (gut), *Ohne Abschied* (neutral),
*Zwischen zwei Sekunden* (schlecht). Gefundene Enden merkt sich der Browser.
