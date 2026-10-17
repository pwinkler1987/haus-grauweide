"""Prüft die Spielinhalte auf typische Fehler (Tippfehler bei Räumen/Gegenständen)."""


def _strings(action):
    """Alle Befehls-Strings aus einer (verschachtelten) Aktion sammeln."""
    if action is None:
        return
    if isinstance(action, str):
        yield action
    elif isinstance(action, list):
        for a in action:
            yield from _strings(a)
    elif isinstance(action, dict):
        cond = action.get("if")
        for c in ([cond] if isinstance(cond, str) else cond or []):
            yield "?" + c
        yield from _strings(action.get("do"))
        yield from _strings(action.get("else"))


def _conditions(cond):
    return [cond] if isinstance(cond, str) else list(cond or [])


def validate(data):
    rooms, items = data["rooms"], data["items"]
    problems = []

    def check(where, action):
        for s in _strings(action):
            if s.startswith("?"):
                cmd, _, arg = s[1:].lstrip("!").partition(":")
                if cmd == "has" and arg not in items:
                    problems.append(f"{where}: Bedingung kennt Gegenstand '{arg}' nicht")
                continue
            cmd, _, arg = s.partition(":")
            if cmd == "goto" and arg.split(":")[0] not in rooms:
                problems.append(f"{where}: Raum '{arg}' existiert nicht")
            if cmd in ("take", "drop") and arg not in items:
                problems.append(f"{where}: Gegenstand '{arg}' existiert nicht")

    if data["start"]["room"] not in rooms:
        problems.append(f"Startraum '{data['start']['room']}' existiert nicht")

    for rid, room in rooms.items():
        check(f"Raum {rid} (on_enter)", room.get("on_enter"))
        seen = set()
        for hs in room.get("hotspots", []):
            hid = hs.get("id")
            if hid in seen:
                problems.append(f"Raum {rid}: Hotspot-ID '{hid}' doppelt")
            seen.add(hid)
            if len(hs.get("rect", [])) != 4:
                problems.append(f"Raum {rid}/{hid}: 'rect' braucht [x, y, breite, höhe]")
            for c in _conditions(hs.get("if")):
                check(f"Raum {rid}/{hid}", {"if": c})
            for verb, action in hs.get("actions", {}).items():
                check(f"Raum {rid}/{hid}/{verb}", action)

    for iid, item in items.items():
        for verb, action in item.get("actions", {}).items():
            check(f"Gegenstand {iid}/{verb}", action)

    return problems
