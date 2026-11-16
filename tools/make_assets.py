"""Erzeugt App-Icons, Splash-Screens und Store-Grafiken aus assets/icon.png (128×128)
und assets/feature.png (512×250), beide Pixel-Art in Spielauflösung.

    python3 tools/make_assets.py          -> android/…/res, ios/…/Assets.xcassets, store/
Braucht Pillow.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "android" / "app" / "src" / "main" / "res"
XCASSETS = ROOT / "ios" / "App" / "App" / "Assets.xcassets"
STORE = ROOT / "store"
FONT = ROOT / "static" / "fonts" / "VT323-Regular.ttf"
BG = (11, 10, 30)
TITLE = "Das Haus Grauweide"
SUBTITLE = "Ein Spukhaus-Mysterium"

ICON = Image.open(ROOT / "assets" / "icon.png").convert("RGB")
FEATURE = Image.open(ROOT / "assets" / "feature.png").convert("RGB")
DENSITIES = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}


def scaled(img, size):
    """Pixel-Art auf `size` bringen: erst ganzzahlig hoch (scharf), dann glatt auf Zielmaß."""
    w, h = size
    k = max(1, max(w // img.width, h // img.height))
    big = img.resize((img.width * k, img.height * k), Image.NEAREST)
    return big if big.size == (w, h) else big.resize((w, h), Image.LANCZOS)


def text(draw, xy, s, size, fill, anchor="la"):
    font = ImageFont.truetype(str(FONT), size)
    x, y = xy
    off = max(1, size // 16)
    draw.text((x + off, y + off), s, font=font, fill=(0, 0, 0), anchor=anchor)
    draw.text((x, y), s, font=font, fill=fill, anchor=anchor)


def circle(img):
    mask = Image.new("L", (img.width * 4, img.height * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, mask.width - 1, mask.height - 1), fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask.resize(img.size, Image.LANCZOS))
    return out


def adaptive_layer(px):
    """108-dp-Ebene: Motiv auf 88 dp, damit der sichtbare 72-dp-Ausschnitt nur Motiv zeigt."""
    layer = Image.new("RGB", (px, px), BG)
    inner = round(px * 88 / 108)
    layer.paste(scaled(ICON, (inner, inner)), ((px - inner) // 2, (px - inner) // 2))
    return layer


def splash(w, h):
    img = Image.new("RGB", (w, h), BG)
    side = min(w, h)
    icon = side * 45 // 100
    y = (h - icon) // 2 - side // 14
    img.paste(scaled(ICON, (icon, icon)), ((w - icon) // 2, y))
    text(ImageDraw.Draw(img), (w // 2, y + icon + side // 40), TITLE, side // 11, (240, 214, 140), "ma")
    return img


def android():
    for name, d in DENSITIES.items():
        folder = RES / f"mipmap-{name}"
        legacy = scaled(ICON, (round(48 * d),) * 2)
        legacy.save(folder / "ic_launcher.png")
        circle(legacy).save(folder / "ic_launcher_round.png")
        adaptive_layer(round(108 * d)).save(folder / "ic_launcher_foreground.png")
    for folder in RES.glob("drawable*"):
        f = folder / "splash.png"
        if f.exists():
            splash(*Image.open(f).size).save(f, optimize=True)
    (RES / "values" / "ic_launcher_background.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        f'    <color name="ic_launcher_background">#{BG[0]:02X}{BG[1]:02X}{BG[2]:02X}</color>\n</resources>\n',
        encoding="utf-8")


def ios():
    scaled(ICON, (1024, 1024)).save(XCASSETS / "AppIcon.appiconset" / "AppIcon-512@2x.png")
    s = splash(2732, 2732)
    for n in ("splash-2732x2732.png", "splash-2732x2732-1.png", "splash-2732x2732-2.png"):
        s.save(XCASSETS / "Splash.imageset" / n, optimize=True)


def store():
    STORE.mkdir(exist_ok=True)
    scaled(ICON, (512, 512)).save(STORE / "play-icon-512.png")
    scaled(ICON, (1024, 1024)).save(STORE / "appstore-icon-1024.png")
    img = scaled(FEATURE, (1024, 500))
    d = ImageDraw.Draw(img)
    text(d, (48, 150), "Das Haus", 92, (240, 214, 140))
    text(d, (48, 232), "Grauweide", 118, (240, 214, 140))
    text(d, (52, 358), SUBTITLE, 44, (205, 200, 230))
    img.save(STORE / "play-feature-1024x500.png")


if __name__ == "__main__":
    android()
    ios()
    store()
    print("Icons, Splash und Store-Grafiken erzeugt.")
