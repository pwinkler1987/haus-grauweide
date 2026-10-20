// Die Verb-Leiste (3x3 wie bei den Klassikern).
import { t } from './i18n.js';

export const VERBS = [
  ['open', 'Öffne'],   ['close', 'Schließe'], ['give', 'Gib'],
  ['take', 'Nimm'],    ['look', 'Schau an'],  ['talk', 'Rede mit'],
  ['use', 'Benutze'],  ['push', 'Drücke'],    ['walk', 'Gehe zu'],
];

export const verbLabel = (id) => t(`verbs.${id}`);

// Verben, die zwei Objekte verbinden können: "Benutze X mit Y", "Gib X an Y".
export const preposition = (id) => t(`prep.${id}`);

export class VerbBar {
  constructor(el, onChange) {
    this.onChange = onChange;
    this.buttons = {};
    this.verb = 'walk';
    VERBS.forEach(([id], i) => {
      const label = verbLabel(id);
      const b = document.createElement('button');
      b.textContent = label;
      b.title = t('key', { n: i + 1 });
      b.addEventListener('click', () => this.set(id));
      el.appendChild(b);
      this.buttons[id] = b;
    });
    this.highlight();
  }

  highlight() {
    for (const [id, b] of Object.entries(this.buttons)) b.classList.toggle('active', id === this.verb);
  }

  set(verb) {
    this.verb = verb;
    this.highlight();
    this.onChange(verb);
  }

  setByIndex(i) {
    if (VERBS[i]) this.set(VERBS[i][0]);
  }

  reset() { this.set('walk'); }
}
