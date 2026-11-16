"""Rechnet hochaufgelöste Raumbilder auf die Spielauflösung (320×144) herunter.

    python tools/pixelate.py BILD.png [...]   -> static/img/rooms/<name>.png
    python tools/pixelate.py --overlay RAUM.png VARIANTE.png NAME X Y B H
                                              -> static/img/sprites/<NAME>.png

Die Vorlage sollte die Komposition des Raums (Hotspots, Laufbereich) einhalten;
sie wird auf 320×144 verkleinert und auf 64 Farben reduziert. Braucht Pillow.

--overlay vergleicht eine Variante des Raumbilds (z. B. mit offener Tür) mit dem
Original und speichert nur die geänderten Pixel im Rechteck X Y B H (in
Spielkoordinaten) als transparentes Overlay in Raumgröße.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

W, H, COLORS = 320, 144, 64
STATIC = Path(__file__).resolve().parent.parent / "static"
OUT = STATIC / "img" / "rooms"
DIFF_THRESHOLD = 20


def shrink(path):
    return Image.open(path).convert("RGB").resize((W, H), Image.BOX)


def overlay(base, variant, name, x, y, w, h):
    a, b = shrink(base), shrink(variant)
    diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > DIFF_THRESHOLD else 0)
    diff = diff.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.MaxFilter(3))
    box = Image.new("L", (W, H), 0)
    box.paste(255, (x, y, x + w, y + h))
    mask = ImageChops.multiply(diff, box)
    colors = b.quantize(colors=COLORS, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(colors, (0, 0), mask)
    dest = STATIC / "img" / "sprites" / f"{name}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, optimize=True)
    print(f"{variant} -> {dest.relative_to(STATIC.parent)}")


def main(paths):
    OUT.mkdir(parents=True, exist_ok=True)
    for p in map(Path, paths):
        img = Image.open(p).convert("RGB").resize((W, H), Image.BOX)
        img = img.quantize(colors=COLORS, method=Image.MEDIANCUT, dither=Image.NONE)
        img.save(OUT / f"{p.stem}.png", optimize=True)
        print(f"{p.name} -> {(OUT / p.name).relative_to(OUT.parents[2])}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--overlay":
        base, variant, name, *rect = sys.argv[2:]
        overlay(base, variant, name, *map(int, rect))
    else:
        main(sys.argv[1:])
