// Geometrie-Helfer für Räume: Walkbox (begehbare Fläche) und Hotspot-Suche.

export function pointInPolygon(x, y, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i];
    const [xj, yj] = poly[j];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

function nearestOnSegment(px, py, [ax, ay], [bx, by]) {
  const dx = bx - ax, dy = by - ay;
  const len = dx * dx + dy * dy || 1;
  const t = Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / len));
  return [ax + t * dx, ay + t * dy];
}

// Liegt der Punkt außerhalb der Walkbox, wird der nächste Randpunkt genommen.
export function clampToPolygon(x, y, poly) {
  if (!poly || pointInPolygon(x, y, poly)) return [x, y];
  let best = [x, y], bestDist = Infinity;
  for (let i = 0; i < poly.length; i++) {
    const [nx, ny] = nearestOnSegment(x, y, poly[i], poly[(i + 1) % poly.length]);
    const d = (nx - x) ** 2 + (ny - y) ** 2;
    if (d < bestDist) { bestDist = d; best = [nx, ny]; }
  }
  return best;
}

// Später definierte Hotspots liegen oben – daher rückwärts suchen.
export function hotspotAt(hotspots, x, y) {
  for (let i = hotspots.length - 1; i >= 0; i--) {
    const [hx, hy, hw, hh] = hotspots[i].rect;
    if (x >= hx && x < hx + hw && y >= hy && y < hy + hh) return hotspots[i];
  }
  return null;
}
