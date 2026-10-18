// Eine Spielfigur: Position (Füße), Laufen zu einem Ziel, Platzhalter-Sprite.

export class Actor {
  constructor(id, def) {
    this.id = id;
    this.def = def;
    this.room = null;
    this.x = 160;
    this.y = 128;
    this.dir = 1;          // 1 = rechts, -1 = links
    this.speed = 70;       // Pixel pro Sekunde
    this.target = null;
    this.resolve = null;
    this.t = 0;
  }

  get walking() { return this.target !== null; }

  // Liefert ein Promise: true = angekommen, false = unterbrochen.
  walkTo(x, y) {
    this.cancel();
    if (Math.abs(x - this.x) > 0.5) this.dir = Math.sign(x - this.x);
    return new Promise((resolve) => {
      this.target = { x, y };
      this.resolve = resolve;
    });
  }

  cancel() {
    const r = this.resolve;
    this.target = null;
    this.resolve = null;
    if (r) r(false);
  }

  place(x, y) {
    this.cancel();
    this.x = x;
    this.y = y;
  }

  // Klickfläche um die Figur herum
  contains(px, py) {
    return px >= this.x - 7 && px < this.x + 7 && py >= this.y - 36 && py < this.y;
  }

  update(dt) {
    if (!this.target) return;
    this.t += dt;
    const dx = this.target.x - this.x;
    const dy = (this.target.y - this.y);
    const dist = Math.hypot(dx, dy * 1.6); // in die Tiefe läuft man langsamer
    const step = this.speed * dt;
    if (dist <= step) {
      this.x = this.target.x;
      this.y = this.target.y;
      const r = this.resolve;
      this.target = null;
      this.resolve = null;
      if (r) r(true);
      return;
    }
    this.x += (dx / dist) * step;
    this.y += (dy / dist) * step;
  }

  draw(ctx) {
    const s = this.def.sprite;
    const frame = this.walking ? Math.floor(this.t * 8) % 2 : -1;
    const box = (c, x, y, w, h) => { ctx.fillStyle = c; ctx.fillRect(x, y, w, h); };

    ctx.save();
    if (s.ghost) ctx.globalAlpha = 0.45 + 0.15 * Math.sin(performance.now() / 300);
    ctx.translate(Math.round(this.x), Math.round(this.y));
    if (this.dir < 0) ctx.scale(-1, 1);

    box('rgba(0,0,0,0.35)', -7, -1, 14, 2);                 // Schatten
    if (s.long_hair) box(s.hair, -5, -31, 5, 10);           // lange Haare hinter dem Körper
    box(s.pants, -4, -12, 3, frame === 0 ? 10 : 11);        // Beine
    box(s.pants, 1, -12, 3, frame === 1 ? 10 : 11);
    box(s.shoes, frame === 0 ? -6 : -5, -2, 4, 2);          // Schuhe
    box(s.shoes, frame === 1 ? 2 : 1, -2, 4, 2);
    box(s.jacket, -5, -24, 10, 12);                         // Körper
    const swing = frame === -1 ? 0 : frame === 0 ? 1 : -1;
    box(s.jacket, -7, -23 + swing, 2, 8);                   // Arme
    box(s.jacket, 5, -23 - swing, 2, 8);
    box(s.skin, -7, -15 + swing, 2, 2);                     // Hände
    box(s.skin, 5, -15 - swing, 2, 2);
    box(s.skin, -4, -32, 8, 8);                             // Kopf
    box(s.hair, -4, -33, 8, 3);
    box(s.hair, -4, -31, 2, 4);
    box('#222', 2, -29, 1, 1);                              // Auge
    if (s.goggles) box(s.goggles, 0, -30, 5, 2);            // Schutzbrille
    if (s.cap) {                                            // verkehrt herum getragene Kappe
      box(s.cap, -5, -35, 9, 3);
      box(s.cap, -8, -33, 4, 1);
    }
    ctx.restore();
  }
}

// Zeichnet eine Figur stehend auf eine eigene kleine Leinwand (Porträt-Knöpfe, Charakterwahl).
export function drawPortrait(canvas, id, def) {
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const a = new Actor(id, def);
  a.place(canvas.width / 2, canvas.height - 2);
  a.draw(ctx);
}
