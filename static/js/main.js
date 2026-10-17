// Das Haus Grauweide – Spielschleife und Interaktion.
import { drawShapes, drawHotspotOutlines } from './engine/renderer.js';
import { Actor } from './engine/actor.js';
import { clampToPolygon, hotspotAt } from './engine/room.js';
import { VerbBar, VERB_LABEL, PREPOSITION } from './engine/verbs.js';
import { InventoryView } from './engine/inventory.js';
import { ScriptRunner } from './engine/script.js';
import { Sound } from './engine/audio.js';

const W = 320;
const H = 144;
const SAVE_SLOT = 'slot1';

// Antworten, wenn ein Objekt für ein Verb nichts Eigenes festlegt.
const DEFAULT_REPLY = {
  look: 'Sieht ganz normal aus.',
  take: 'Das kann ich nicht mitnehmen.',
  use: 'Das funktioniert so nicht.',
  open: 'Das lässt sich nicht öffnen.',
  close: 'Das lässt sich nicht schließen.',
  talk: 'Ich glaube nicht, dass das antwortet.',
  give: 'Das will ich nicht hergeben.',
  push: 'Da bewegt sich nichts.',
  combine: 'Das passt nicht zusammen.',
};

class Game {
  constructor(data) {
    this.data = data;
    this.canvas = document.getElementById('scene');
    this.ctx = this.canvas.getContext('2d');
    this.ctx.imageSmoothingEnabled = false;
    this.el = {
      wrap: document.getElementById('scene-wrap'),
      speech: document.getElementById('speech'),
      narration: document.getElementById('narration'),
      sentence: document.getElementById('sentence'),
      roomName: document.getElementById('room-name'),
      toast: document.getElementById('toast'),
    };

    this.state = { room: null, flags: {}, inventory: [], activeChar: data.start.character };
    this.room = null;
    this.actor = new Actor(this.state.activeChar, data.characters[this.state.activeChar]);
    this.script = new ScriptRunner(this);
    this.sound = new Sound();
    this.busyCount = 0;     // > 0 während Skripte/Zwischensequenzen laufen
    this.skip = null;       // beendet den aktuellen Text vorzeitig
    this.hover = null;      // Objekt unter der Maus
    this.pending = null;    // erstes Objekt bei "Benutze X mit ..."
    this.showHotspots = false;

    this.verbs = new VerbBar(document.getElementById('verbs'), () => this.updateSentence());
    this.inventory = new InventoryView(document.getElementById('inventory'), data.items, {
      onClick: (id) => this.select(this.itemObj(id)),
      onContext: (id) => this.quickAction(this.itemObj(id)),
      onHover: (id) => { this.hover = id ? this.itemObj(id) : null; this.updateSentence(); },
    });
    this.bindInput();
  }

  get busy() { return this.busyCount > 0; }

  async withBusy(fn) {
    this.busyCount++;
    try { await fn(); } finally { this.busyCount--; this.updateSentence(); }
  }

  // ---- Objekte ----------------------------------------------------------
  hotspotObj(hs) { return { kind: 'hotspot', id: hs.id, name: hs.name, def: hs }; }
  itemObj(id) { return { kind: 'item', id, name: this.data.items[id].name, def: this.data.items[id] }; }

  visibleHotspots() {
    return (this.room?.hotspots ?? []).filter((hs) => this.script.check(hs.if));
  }

  // ---- Räume ------------------------------------------------------------
  setRoom(id, pos) {
    const room = this.data.rooms[id];
    if (!room) { console.error('Raum fehlt:', id); return false; }
    this.room = room;
    this.state.room = id;
    this.actor.place(...(pos ?? room.start));
    this.hover = null;
    this.el.roomName.textContent = room.name;
    this.updateSentence();
    return true;
  }

  async enterRoom(id, pos) {
    if (this.setRoom(id, pos) && this.room.on_enter) {
      await this.withBusy(() => this.script.run(this.room.on_enter));
    }
  }

  // ---- Inventar ---------------------------------------------------------
  addItem(id) {
    if (!this.state.inventory.includes(id)) this.state.inventory.push(id);
    this.state.flags[`got_${id}`] = true;
    this.renderInventory();
  }

  removeItem(id) {
    this.state.inventory = this.state.inventory.filter((i) => i !== id);
    this.renderInventory();
  }

  renderInventory() {
    this.inventory.render(this.state.inventory, this.pending?.kind === 'item' ? this.pending.id : null);
  }

  // ---- Satzzeile --------------------------------------------------------
  updateSentence() {
    if (this.busy) { this.el.sentence.innerHTML = '&nbsp;'; return; }
    const verb = this.verbs.verb;
    const parts = [VERB_LABEL[verb]];
    if (this.pending) parts.push(this.pending.name, PREPOSITION[verb]);
    if (this.hover && this.hover !== this.pending) parts.push(this.hover.name);
    this.el.sentence.textContent = parts.join(' ');
  }

  // ---- Interaktion ------------------------------------------------------
  select(obj) {
    if (this.busy) return;
    let verb = this.verbs.verb;
    if (verb === 'walk' && obj.kind === 'item') verb = 'look';

    if (this.pending) {
      const first = this.pending;
      this.pending = null;
      if (first.kind === obj.kind && first.id === obj.id) { this.resetSelection(); return; }
      this.execute(verb, first, obj);
      return;
    }
    // Gegenstand ohne eigene "use"-Aktion -> wartet auf zweites Objekt
    const needsSecond = obj.kind === 'item' &&
      ((verb === 'use' && !(obj.def.actions && 'use' in obj.def.actions)) || verb === 'give');
    if (needsSecond) {
      this.pending = obj;
      this.renderInventory();
      this.updateSentence();
      return;
    }
    this.execute(verb, obj);
  }

  quickAction(obj) {
    if (this.busy) return;
    this.pending = null;
    this.execute(obj.def.default ?? 'look', obj);
  }

  resetSelection() {
    this.pending = null;
    this.verbs.reset();
    this.renderInventory();
  }

  findAction(verb, a, b) {
    const acts = (o) => o.def.actions ?? {};
    if (b) {
      return acts(b)[`${verb}:${a.id}`] ?? acts(a)[`${verb}:${b.id}`] ?? DEFAULT_REPLY.combine;
    }
    const own = acts(a)[verb];
    if (own !== undefined) return own;
    if (verb === 'walk') return null;
    if (verb === 'take' && a.kind === 'item') return 'Das habe ich doch schon.';
    if (verb === 'give' && a.kind === 'hotspot') return 'Das muss ich erst einmal haben.';
    return DEFAULT_REPLY[verb];
  }

  async execute(verb, a, b = null) {
    this.resetSelection();
    const target = [b, a].find((o) => o?.kind === 'hotspot');
    if (target) {
      const [hx, hy, hw, hh] = target.def.rect;
      const [wx, wy] = target.def.walk_to ?? [hx + hw / 2, hy + hh];
      if (!(await this.walkTo(wx, wy))) return; // Spieler hat woanders hingeklickt
      const cx = hx + hw / 2;
      if (Math.abs(cx - this.actor.x) > 2) this.actor.dir = Math.sign(cx - this.actor.x);
    }
    await this.withBusy(() => this.script.run(this.findAction(verb, a, b)));
  }

  walkTo(x, y) {
    const [tx, ty] = clampToPolygon(x, y, this.room.walkbox);
    return this.actor.walkTo(tx, ty);
  }

  // ---- Texte ------------------------------------------------------------
  showUntilDone(el, timeout) {
    el.hidden = false;
    return new Promise((resolve) => {
      let timer;
      const done = () => {
        clearTimeout(timer);
        el.hidden = true;
        this.skip = null;
        resolve();
      };
      if (timeout) timer = setTimeout(done, timeout);
      this.skip = done;
    });
  }

  say(text) {
    const el = this.el.speech;
    el.textContent = text;
    el.style.color = this.actor.def.text_color;
    el.hidden = false;
    const scale = this.el.wrap.clientWidth / W;
    const left = this.actor.x * scale - el.offsetWidth / 2;
    el.style.left = `${Math.max(4, Math.min(left, this.el.wrap.clientWidth - el.offsetWidth - 4))}px`;
    el.style.top = `${Math.max(4, (this.actor.y - 40) * scale - el.offsetHeight)}px`;
    return this.showUntilDone(el, 1400 + text.length * 55);
  }

  narrate(text) {
    this.el.narration.querySelector('p').textContent = text;
    return this.showUntilDone(this.el.narration, 0);
  }

  toast(text) {
    this.el.toast.textContent = text;
    this.el.toast.hidden = false;
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => { this.el.toast.hidden = true; }, 1600);
  }

  // ---- Speichern / Laden ------------------------------------------------
  async save() {
    if (this.busy) return this.toast('Gerade nicht möglich.');
    const state = { ...this.state, actor: [Math.round(this.actor.x), Math.round(this.actor.y)] };
    const res = await fetch('/api/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slot: SAVE_SLOT, state }),
    });
    this.toast(res.ok ? 'Gespeichert.' : 'Speichern fehlgeschlagen.');
  }

  async load() {
    if (this.busy) return this.toast('Gerade nicht möglich.');
    const res = await fetch(`/api/load?slot=${SAVE_SLOT}`);
    if (!res.ok) return this.toast('Kein Spielstand gefunden.');
    const s = await res.json();
    this.state.flags = s.flags ?? {};
    this.state.inventory = s.inventory ?? [];
    this.resetSelection();
    this.setRoom(s.room, s.actor);
    this.toast('Geladen.');
  }

  // ---- Eingabe ----------------------------------------------------------
  scenePos(e) {
    const r = this.canvas.getBoundingClientRect();
    return [((e.clientX - r.left) / r.width) * W, ((e.clientY - r.top) / r.height) * H];
  }

  bindInput() {
    const c = this.canvas;
    c.addEventListener('mousemove', (e) => {
      const hs = hotspotAt(this.visibleHotspots(), ...this.scenePos(e));
      const obj = hs ? this.hotspotObj(hs) : null;
      if (obj?.id !== this.hover?.id) { this.hover = obj; this.updateSentence(); }
    });
    c.addEventListener('mouseleave', () => { this.hover = null; this.updateSentence(); });
    c.addEventListener('click', (e) => this.onSceneClick(e, false));
    c.addEventListener('contextmenu', (e) => { e.preventDefault(); this.onSceneClick(e, true); });
    this.el.narration.addEventListener('click', () => this.skip?.());

    window.addEventListener('keydown', (e) => {
      if (e.key === 'F5') { e.preventDefault(); this.save(); return; }
      if (e.key === 'F9') { e.preventDefault(); this.load(); return; }
      if (e.key === 'Escape' || e.key === ' ' || e.key === '.') {
        if (this.skip) { e.preventDefault(); this.skip(); return; }
        if (e.key === 'Escape') this.resetSelection();
        return;
      }
      if (this.busy) return;
      if (e.key === 'h' || e.key === 'H') this.showHotspots = !this.showHotspots;
      if (e.key >= '1' && e.key <= '9') this.verbs.setByIndex(Number(e.key) - 1);
    });
  }

  onSceneClick(e, quick) {
    this.sound.unlock();
    if (this.busy) { this.skip?.(); return; }
    const [x, y] = this.scenePos(e);
    const hs = hotspotAt(this.visibleHotspots(), x, y);
    if (!hs) {
      this.resetSelection();
      this.walkTo(x, y);
      return;
    }
    const obj = this.hotspotObj(hs);
    if (quick) this.quickAction(obj);
    else this.select(obj);
  }

  // ---- Spielschleife ----------------------------------------------------
  start() {
    let last = performance.now();
    const frame = (now) => {
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      this.actor.update(dt);
      this.draw();
      requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }

  draw() {
    const ctx = this.ctx;
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, W, H);
    if (!this.room) return;
    drawShapes(ctx, this.room.draw, (cond) => this.script.check(cond));
    this.actor.draw(ctx);
    if (this.showHotspots) drawHotspotOutlines(ctx, this.visibleHotspots());
  }
}

async function boot() {
  const res = await fetch('/api/data');
  const data = await res.json();
  const game = new Game(data);
  window.game = game; // zum Ausprobieren in der Browser-Konsole
  game.start();

  const title = document.getElementById('title');
  title.addEventListener('click', () => {
    title.hidden = true;
    game.sound.unlock();
    game.enterRoom(data.start.room);
  }, { once: true });
}

boot();
