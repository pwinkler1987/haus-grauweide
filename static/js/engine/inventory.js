// Inventar-Anzeige: ein Feld pro Gegenstand mit gezeichnetem Icon.
import { drawShapes } from './renderer.js';
import { onPress } from './press.js';

export class InventoryView {
  constructor(el, items, { onClick, onContext, onHover }) {
    this.el = el;
    this.items = items;
    this.handlers = { onClick, onContext, onHover };
  }

  render(ids, pendingId = null) {
    this.el.innerHTML = '';
    for (const id of ids) {
      const item = this.items[id];
      const b = document.createElement('button');
      b.title = item.name;
      b.classList.toggle('pending', id === pendingId);
      const c = document.createElement('canvas');
      c.width = 24;
      c.height = 16;
      drawShapes(c.getContext('2d'), item.icon, () => true);
      b.appendChild(c);
      onPress(b, {
        tap: () => this.handlers.onClick(id),
        long: () => this.handlers.onContext(id),
        down: () => this.handlers.onHover(id),
      });
      b.addEventListener('mouseenter', () => this.handlers.onHover(id));
      b.addEventListener('mouseleave', () => this.handlers.onHover(null));
      this.el.appendChild(b);
    }
  }
}
