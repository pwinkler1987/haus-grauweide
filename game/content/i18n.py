"""Übersetzung der Spielinhalte.

Die Inhalte werden auf Deutsch geschrieben. lang/<sprache>.json ordnet jedem
deutschen Text die Übersetzung zu; translate() ersetzt sie in den Spieldaten.
Neue Texte trägt `python tools/i18n.py` mit leerem Wert in die Datei ein.
"""
import json
import re
from pathlib import Path

LANG_DIR = Path(__file__).resolve().parent / "lang"
LANGUAGES = ["en"]

# Felder, die direkt Text enthalten
TEXT_KEYS = {"title", "name", "role", "ability", "text", "credits"}
# Felder, deren Inhalt Aktionen sind (Strings: Befehl oder gesprochener Text)
ACTION_KEYS = {"actions", "do", "else", "on_enter", "intro"}
COMMANDS = {
    "say", "sayas", "narrate", "set", "unset", "take", "drop", "goto", "party_goto",
    "place", "remove", "choose", "sound", "wait", "dialog", "walk", "face", "codelock", "end",
}
_CMD = re.compile(r"^(\w+):([\s\S]*)$")


def _action(s, fn):
    m = _CMD.match(s)
    if not m or m[1] not in COMMANDS:
        return fn(s)
    cmd, arg = m[1], m[2]
    if cmd in ("say", "narrate"):
        return f"{cmd}:{fn(arg)}"
    if cmd == "sayas":
        who, _, text = arg.partition(":")
        return f"sayas:{who}:{fn(text)}"
    return s


def _walk(o, fn, mode=None):
    """mode: None (nichts übersetzen), 'text' oder 'action'."""
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if mode == "action" and k == "if":
                out[k] = v
            elif k in ACTION_KEYS:
                out[k] = _walk(v, fn, "action") if k != "actions" else {a: _walk(x, fn, "action") for a, x in v.items()}
            elif k in TEXT_KEYS and k != "id":
                out[k] = _walk(v, fn, "text")
            else:
                out[k] = _walk(v, fn, mode if mode == "action" else None)
        return out
    if isinstance(o, (list, tuple)):
        return [_walk(v, fn, mode) for v in o]
    if isinstance(o, str):
        if mode == "text":
            return fn(o)
        if mode == "action":
            return _action(o, fn)
    return o


def texts(data):
    found = []
    _walk(data, lambda s: found.append(s) or s)
    return list(dict.fromkeys(s for s in found if s.strip()))


def load_table(lang):
    path = LANG_DIR / f"{lang}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def translate(data, lang):
    table = load_table(lang)
    missing = []

    def fn(s):
        if not s.strip():
            return s
        t = table.get(s)
        if not t:
            missing.append(s)
            return s
        return t

    return _walk(data, fn), list(dict.fromkeys(missing))
