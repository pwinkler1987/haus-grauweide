// Eine Spielfigur: Position (Füße), Laufen zu einem Ziel, Pixel-Sprite.

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
    this.frames ??= {};
    const img = (this.frames[frame] ??= buildSprite(s, frame));

    ctx.save();
    if (s.ghost) ctx.globalAlpha = 0.45 + 0.15 * Math.sin(performance.now() / 300);
    ctx.translate(Math.round(this.x), Math.round(this.y));
    if (this.dir < 0) ctx.scale(-1, 1);
    ctx.fillStyle = 'rgba(0,0,0,0.35)';                     // Schatten
    ctx.fillRect(-7, -1, 14, 2);
    ctx.fillRect(-5, 0, 10, 1);
    ctx.drawImage(img, -SPRITE_W / 2 - 1, -SPRITE_H - 1);
    ctx.restore();
  }
}

// --- Pixel-Sprite --------------------------------------------------------
// Figuren sind 12×33 Pixel (Blick nach rechts), bekommen einen dunklen Umriss
// und werden aus den Farben in characters.py eingefärbt. frame: -1 = stehen,
// 0 = Schritt, 1 = Beine beisammen.

const SPRITE_W = 12;
const SPRITE_H = 33;
const OUTLINE = '#120e16';

const HEAD = [
  '...hhhhhh...',
  '..hhhhhhhh..',
  '.hhhhhhhhhh.',
  '.hhhhhhhsss.',
  '.hhhhSsssess',
  '.hhhSSsssss.',
  '..hhSssssss.',
  '...SSsssmss.',
  '....SSssss..',
  '.....SSss...',
];
const CAP = [
  '...cccccc...',
  '..cccccccc..',
  'CCCcccccccc.',
];
const TORSO = [
  '...jjjjjj...',
  '..jjjjjjjjj.',
  '..jjjjjjjjj.',
  '..jjjjjjjjj.',
  '..jjjjjjjjj.',
  '..Jjjjjjjjj.',
  '..Jjjjjjjjj.',
  '..Jjjjjjjjj.',
  '..JJJJJJJJJ.',
  '...JJJJJJJ..',
];

function shade(hex, f) {
  const n = parseInt(hex.slice(1), 16);
  const c = (v) => Math.max(0, Math.min(255, Math.round(v * f)));
  return `rgb(${c(n >> 16)},${c((n >> 8) & 255)},${c(n & 255)})`;
}

function buildSprite(s, frame) {
  const px = Array.from({ length: SPRITE_H }, () => Array(SPRITE_W).fill(null));
  const set = (x, y, c) => { if (x >= 0 && x < SPRITE_W && y >= 0 && y < SPRITE_H) px[y][x] = c; };
  const pal = {
    h: s.hair, H: shade(s.hair, 0.7), s: s.skin, S: shade(s.skin, 0.8), e: '#1a1418',
    m: shade(s.skin, 0.62), c: s.cap, C: s.cap && shade(s.cap, 0.7),
    j: s.jacket, J: shade(s.jacket, 0.72), p: s.pants, P: shade(s.pants, 0.7),
  };
  const paint = (rows, y0) => rows.forEach((row, y) => [...row].forEach((k, x) => {
    if (k !== '.') set(x, y0 + y, pal[k]);
  }));
  const bob = frame === 1 ? 1 : 0;   // Beine beisammen: Oberkörper 1 Pixel tiefer

  // Beine und Schuhe (hinteres Bein dunkler)
  const spread = frame === 0 ? 3 : 0;
  for (let y = 20; y <= 30; y++) {
    const t = Math.max(0, (y - 21) / 9);
    const back = 4 - Math.round(t * spread);
    const front = 6 + Math.round(t * spread);
    for (const [x, c] of [[back, pal.P], [back + 1, pal.P], [front, pal.p], [front + 1, pal.p]]) set(x, y, c);
    if (y <= 21) for (let x = 3; x <= 8; x++) set(x, y, x < 6 ? pal.P : pal.p);
  }
  const shoe = (x, c) => { for (let i = 0; i < 3; i++) { set(x + i, 31, c); set(x + i, 32, c); } set(x + 3, 32, c); };
  shoe(4 - spread - 1 + 1, shade(s.shoes, 0.75));
  shoe(6 + spread, s.shoes);

  paint(TORSO, 10 + bob);
  if (s.long_hair) for (let y = 3; y <= 13; y++) { set(1, y + bob, pal.H); set(2, y + bob, pal.h); if (y < 11) set(3, y + bob, pal.h); }
  paint(HEAD, bob);
  if (s.cap) paint(CAP, bob);
  if (s.goggles) {
    for (let x = 6; x <= 10; x++) set(x, 4 + bob, shade(s.goggles, 0.6));
    set(8, 4 + bob, s.goggles); set(9, 4 + bob, s.goggles);
  }

  // Arm vorn: schwingt beim Gehen
  const swing = frame === 0 ? 2 : frame === 1 ? -1 : 0;
  for (let y = 11; y <= 16; y++) {
    const x = 5 + Math.round(((y - 11) / 5) * swing);
    set(x, y + bob, pal.J); set(x + 1, y + bob, pal.J);
  }
  const hx = 5 + swing;
  set(hx, 17 + bob, pal.s); set(hx + 1, 17 + bob, pal.S);

  // Umriss um alle gefüllten Pixel
  const canvas = document.createElement('canvas');
  canvas.width = SPRITE_W + 2;
  canvas.height = SPRITE_H + 2;
  const g = canvas.getContext('2d');
  const filled = (x, y) => x >= 0 && x < SPRITE_W && y >= 0 && y < SPRITE_H && px[y][x];
  g.fillStyle = OUTLINE;
  for (let y = -1; y <= SPRITE_H; y++) {
    for (let x = -1; x <= SPRITE_W; x++) {
      if (!filled(x, y) && (filled(x - 1, y) || filled(x + 1, y) || filled(x, y - 1) || filled(x, y + 1))) {
        g.fillRect(x + 1, y + 1, 1, 1);
      }
    }
  }
  for (let y = 0; y < SPRITE_H; y++) {
    for (let x = 0; x < SPRITE_W; x++) {
      if (px[y][x]) { g.fillStyle = px[y][x]; g.fillRect(x + 1, y + 1, 1, 1); }
    }
  }
  return canvas;
}

// Zeichnet eine Figur stehend auf eine eigene kleine Leinwand (Porträt-Knöpfe, Charakterwahl).
export function drawPortrait(canvas, id, def) {
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const a = new Actor(id, def);
  a.place(canvas.width / 2, canvas.height - 2);
  a.draw(ctx);
}
