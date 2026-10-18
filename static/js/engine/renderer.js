// Zeichnet Form-Listen aus den Python-Inhalten (Räume und Inventar-Icons).
// Räume mit Pixel-Art-Bild zeichnen hier nur noch die zustandsabhängigen Formen.

function starField(ctx, x, y, w, h, count, color) {
  let seed = (x * 73 + y * 151 + count) | 0; // deterministisch: Sterne flackern nicht
  const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
  ctx.fillStyle = color;
  for (let i = 0; i < count; i++) {
    ctx.globalAlpha = 0.4 + rnd() * 0.6;
    ctx.fillRect(Math.floor(x + rnd() * w), Math.floor(y + rnd() * h), 1, 1);
  }
  ctx.globalAlpha = 1;
}

// pixelArt: der Raum hat ein Hintergrundbild, Blöcke mit "sprite" zeigen dann ihr Overlay.
export function drawShapes(ctx, shapes, check, pixelArt = false) {
  for (const s of shapes ?? []) {
    if (!Array.isArray(s)) {
      if (!check(s.if)) continue;
      if (pixelArt && s.sprite === '') continue;
      if (pixelArt && s.img) ctx.drawImage(s.img, 0, 0);
      else drawShapes(ctx, s.shapes, check);
      continue;
    }
    const [type, ...a] = s;
    switch (type) {
      case 'rect':
        ctx.fillStyle = a[4];
        ctx.fillRect(a[0], a[1], a[2], a[3]);
        break;
      case 'poly':
        ctx.fillStyle = a[1];
        ctx.beginPath();
        a[0].forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
        ctx.closePath();
        ctx.fill();
        break;
      case 'circle':
        ctx.fillStyle = a[3];
        ctx.beginPath();
        ctx.arc(a[0], a[1], a[2], 0, Math.PI * 2);
        ctx.fill();
        break;
      case 'line':
        ctx.strokeStyle = a[4];
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(a[0] + 0.5, a[1] + 0.5);
        ctx.lineTo(a[2] + 0.5, a[3] + 0.5);
        ctx.stroke();
        break;
      case 'stars':
        starField(ctx, ...a);
        break;
      default:
        console.warn('Unbekannte Form:', type);
    }
  }
}

export function drawHotspotOutlines(ctx, hotspots) {
  ctx.strokeStyle = 'rgba(255,216,102,0.8)';
  ctx.fillStyle = 'rgba(255,216,102,0.9)';
  ctx.font = '6px monospace';
  for (const hs of hotspots) {
    const [x, y, w, h] = hs.rect;
    ctx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
    ctx.fillText(hs.name, x + 1, y + 6);
  }
}
