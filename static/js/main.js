// Das Haus Grauweide – Spielschleife und Interaktion.
import { drawShapes, drawHotspotOutlines } from './engine/renderer.js';
import { Actor, drawPortrait } from './engine/actor.js';
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
      party: document.getElementById('party'),
      chooser: document.getElementById('chooser'),
    };

    const lead = data.start.character;
    // Alles, was gespeichert wird. Positionen stecken in this.actors und
    // werden beim Speichern nach state.actors kopiert.
    this.state = { flags: {}, party: [lead], activeChar: lead, inventories: { [lead]: [] } };
    this.actors = { [lead]: new Actor(lead, data.characters[lead]) };
    this.room = null;
    this.script = new ScriptRunner(this);
    this.sound = new Sound();
    this.busyCount = 0;     // > 0 während Skripte/Zwischensequenzen laufen
    this.skip = null;       // beendet den aktuellen Text vorzeitig
    this.hover = null;      // Objekt unter der Maus
    this.pending = null;    // erstes Objekt bei "Benutze X mit ..."
    this.showHotspots = false;

    this.verbs = new VerbBar(document.getElementById('verbs'), () => this.updateSentence());
    this.inventoryView = new InventoryView(document.getElementById('inventory'), data.items, {
      onClick: (id) => this.select(this.itemObj(id)),
      onContext: (id) => this.quickAction(this.itemObj(id)),
      onHover: (id) => { this.hover = id ? this.itemObj(id) : null; this.updateSentence(); },
    });
    this.bindInput();
  }

  get busy() { return this.busyCount > 0; }
  get actor() { return this.actors[this.state.activeChar]; }
  get inventory() { return (this.state.inventories[this.state.activeChar] ??= []); }

  async withBusy(fn) {
    this.busyCount++;
    try { await fn(); } finally { this.busyCount--; this.updateSentence(); }
  }

  // ---- Objekte ----------------------------------------------------------
  hotspotObj(hs) { return { kind: 'hotspot', id: hs.id, name: hs.name, def: hs }; }
  itemObj(id) { return { kind: 'item', id, name: this.data.items[id].name, def: this.data.items[id] }; }
  actorObj(a) { return { kind: 'actor', id: a.id, name: a.def.name, def: a.def, actor: a }; }

  visibleHotspots() {
    return (this.room?.hotspots ?? []).filter((hs) => this.script.check(hs.if));
  }

  actorsInRoom() {
    return Object.values(this.actors).filter((a) => a.room === this.room?.id);
  }

  partyHere() {
    return this.state.party.filter((id) => this.actors[id]?.room === this.room?.id);
  }

  objectAt(x, y) {
    const others = this.actorsInRoom()
      .filter((a) => a !== this.actor)
      .sort((a, b) => b.y - a.y);
    const a = others.find((o) => o.contains(x, y));
    if (a) return this.actorObj(a);
    const hs = hotspotAt(this.visibleHotspots(), x, y);
    return hs ? this.hotspotObj(hs) : null;
  }

  // ---- Räume & Figuren --------------------------------------------------
  showRoom(id) {
    const room = this.data.rooms[id];
    if (!room) { console.error('Raum fehlt:', id); return false; }
    this.room = room;
    this.hover = null;
    this.el.roomName.textContent = room.name;
    this.updateSentence();
    return true;
  }

  async runOnEnter() {
    if (this.room.on_enter) await this.withBusy(() => this.script.run(this.room.on_enter));
  }

  async enterRoom(id, pos) {
    if (!this.data.rooms[id]) { console.error('Raum fehlt:', id); return; }
    this.actor.room = id;
    this.actor.place(...(pos ?? this.data.rooms[id].start));
    this.showRoom(id);
    await this.runOnEnter();
  }

  // Alle Gruppenmitglieder im aktuellen Raum ziehen gemeinsam weiter.
  async partyGoto(id) {
    const room = this.data.rooms[id];
    if (!room) { console.error('Raum fehlt:', id); return; }
    const [sx, sy] = room.start;
    this.partyHere().forEach((who, i) => {
      const a = this.actors[who];
      a.room = id;
      a.place(...clampToPolygon(sx + (i % 2 ? 1 : -1) * Math.ceil(i / 2) * 18, sy - (i % 2) * 4, room.walkbox));
    });
    this.showRoom(id);
    await this.runOnEnter();
  }

  placeActor(id, roomId, pos) {
    const def = this.data.characters[id];
    if (!def) { console.error('Figur fehlt:', id); return; }
    const a = (this.actors[id] ??= new Actor(id, def));
    a.room = roomId;
    a.place(...(pos ?? this.data.rooms[roomId].start));
  }

  removeActor(id) {
    delete this.actors[id];
    this.state.party = this.state.party.filter((p) => p !== id);
    this.renderParty();
  }

  switchTo(id) {
    if (this.busy || id === this.state.activeChar || !this.actors[id]) return;
    this.actor.cancel();
    this.state.activeChar = id;
    this.resetSelection();
    this.showRoom(this.actor.room);
    this.renderParty();
  }

  renderParty() {
    const el = this.el.party;
    el.innerHTML = '';
    if (this.state.party.length < 2) return;
    this.state.party.forEach((id, i) => {
      const def = this.data.characters[id];
      const b = document.createElement('button');
      b.classList.toggle('active', id === this.state.activeChar);
      b.title = `${def.name} – ${def.ability} (Tab)`;
      const c = document.createElement('canvas');
      c.width = 20;
      c.height = 40;
      drawPortrait(c, id, def);
      const label = document.createElement('span');
      label.textContent = def.name;
      b.append(c, label);
      b.addEventListener('click', () => this.switchTo(id));
      el.appendChild(b);
    });
  }

  // Overlay "Wer kommt mit?" – liefert erst nach der Auswahl zurück.
  chooseParty(count) {
    const el = this.el.chooser;
    const lead = this.state.party[0];
    const candidates = Object.keys(this.data.characters).filter((id) => id !== lead);
    const chosen = new Set();
    el.innerHTML = '';
    const title = document.createElement('h2');
    title.textContent = `Wer kommt mit? Wähle ${count}.`;
    const grid = document.createElement('div');
    grid.className = 'cards';
    const go = document.createElement('button');
    go.className = 'go';
    go.textContent = "Los geht's!";
    go.disabled = true;

    for (const id of candidates) {
      const def = this.data.characters[id];
      const card = document.createElement('button');
      card.className = 'card';
      const c = document.createElement('canvas');
      c.width = 20;
      c.height = 40;
      drawPortrait(c, id, def);
      card.innerHTML = `<strong>${def.name}</strong><em>${def.role}</em><small>${def.ability}</small>`;
      card.prepend(c);
      card.addEventListener('click', () => {
        if (chosen.has(id)) chosen.delete(id);
        else if (chosen.size < count) chosen.add(id);
        card.classList.toggle('picked', chosen.has(id));
        go.disabled = chosen.size !== count;
      });
      grid.appendChild(card);
    }
    el.append(title, grid, go);
    el.hidden = false;

    return new Promise((resolve) => {
      go.addEventListener('click', async () => {
        el.hidden = true;
        const left = candidates.filter((id) => !chosen.has(id));
        this.state.party = [lead, ...chosen];
        for (const id of chosen) this.state.inventories[id] ??= [];
        left.forEach((id) => delete this.actors[id]);
        this.renderParty();
        const names = left.map((id) => this.data.characters[id].name);
        await this.narrate(
          `${names.slice(0, -1).join(', ')} und ${names.at(-1)} radeln nach Hause.\n\n` +
          'Wenn jemand fragt: Alle übernachten bei allen.',
        );
        resolve();
      }, { once: true });
    });
  }

  // ---- Inventar ---------------------------------------------------------
  addItem(id, who = this.state.activeChar) {
    const inv = (this.state.inventories[who] ??= []);
    if (!inv.includes(id)) inv.push(id);
    this.state.flags[`got_${id}`] = true;
    this.renderInventory();
  }

  removeItem(id, who = this.state.activeChar) {
    const inv = this.state.inventories[who] ?? [];
    const i = inv.indexOf(id);
    if (i >= 0) inv.splice(i, 1);
    this.renderInventory();
  }

  renderInventory() {
    this.inventoryView.render(this.inventory, this.pending?.kind === 'item' ? this.pending.id : null);
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
    if (verb === 'take' && a.kind === 'actor') return 'Die Gruppe trage ich nicht auch noch.';
    if (verb === 'give' && a.kind !== 'item') return 'Das muss ich erst einmal haben.';
    return DEFAULT_REPLY[verb];
  }

  // Wohin läuft die Figur, um mit einem Objekt zu interagieren?
  approachPoint(obj) {
    if (obj.kind === 'actor') {
      const side = this.actor.x < obj.actor.x ? -16 : 16;
      return [obj.actor.x + side, obj.actor.y];
    }
    const [hx, hy, hw, hh] = obj.def.rect;
    return obj.def.walk_to ?? [hx + hw / 2, hy + hh];
  }

  async execute(verb, a, b = null) {
    this.resetSelection();
    const target = [b, a].find((o) => o && o.kind !== 'item');
    if (target) {
      const [wx, wy] = this.approachPoint(target);
      if (!(await this.walkTo(wx, wy))) return; // Spieler hat woanders hingeklickt
      const cx = target.kind === 'actor' ? target.actor.x : target.def.rect[0] + target.def.rect[2] / 2;
      if (Math.abs(cx - this.actor.x) > 2) this.actor.dir = Math.sign(cx - this.actor.x);
      if (target.kind === 'actor') target.actor.dir = -this.actor.dir;
    }
    if (verb === 'give' && a.kind === 'item' && b?.kind === 'actor') {
      return this.withBusy(() => this.giveItem(a.id, b.id));
    }
    await this.withBusy(() => this.script.run(this.findAction(verb, a, b)));
  }

  async giveItem(itemId, toId) {
    if (!this.state.party.includes(toId)) return this.say('Das behalte ich lieber.');
    this.removeItem(itemId);
    this.addItem(itemId, toId);
    await this.say(`Hier, nimm ${this.data.items[itemId].name}.`);
    await this.say('Danke!', toId);
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

  say(text, who = this.state.activeChar) {
    const speaker = this.actors[who] ?? this.actor;
    const el = this.el.speech;
    el.textContent = text;
    el.style.color = speaker.def.text_color;
    el.hidden = false;
    const scale = this.el.wrap.clientWidth / W;
    const left = speaker.x * scale - el.offsetWidth / 2;
    el.style.left = `${Math.max(4, Math.min(left, this.el.wrap.clientWidth - el.offsetWidth - 4))}px`;
    el.style.top = `${Math.max(4, (speaker.y - 40) * scale - el.offsetHeight)}px`;
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
    const actors = Object.fromEntries(Object.values(this.actors).map((a) =>
      [a.id, { room: a.room, x: Math.round(a.x), y: Math.round(a.y), dir: a.dir }]));
    const res = await fetch('/api/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slot: SAVE_SLOT, state: { ...this.state, actors } }),
    });
    this.toast(res.ok ? 'Gespeichert.' : 'Speichern fehlgeschlagen.');
  }

  async load() {
    if (this.busy) return this.toast('Gerade nicht möglich.');
    const res = await fetch(`/api/load?slot=${SAVE_SLOT}`);
    if (!res.ok) return this.toast('Kein Spielstand gefunden.');
    const { actors, ...state } = await res.json();
    if (!actors) return this.toast('Spielstand ist zu alt.');
    this.state = state;
    this.actors = {};
    for (const [id, s] of Object.entries(actors)) {
      this.placeActor(id, s.room, [s.x, s.y]);
      this.actors[id].dir = s.dir ?? 1;
    }
    this.resetSelection();
    this.showRoom(this.actor.room);
    this.renderParty();
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
      const obj = this.objectAt(...this.scenePos(e));
      if (obj?.id !== this.hover?.id) { this.hover = obj; this.updateSentence(); }
    });
    c.addEventListener('mouseleave', () => { this.hover = null; this.updateSentence(); });
    c.addEventListener('click', (e) => this.onSceneClick(e, false));
    c.addEventListener('contextmenu', (e) => { e.preventDefault(); this.onSceneClick(e, true); });
    this.el.narration.addEventListener('click', () => this.skip?.());

    window.addEventListener('keydown', (e) => {
      if (!this.el.chooser.hidden) return;
      if (e.key === 'F5') { e.preventDefault(); this.save(); return; }
      if (e.key === 'F9') { e.preventDefault(); this.load(); return; }
      if (e.key === 'Escape' || e.key === ' ' || e.key === '.') {
        if (this.skip) { e.preventDefault(); this.skip(); return; }
        if (e.key === 'Escape') this.resetSelection();
        return;
      }
      if (this.busy) return;
      if (e.key === 'Tab') {
        e.preventDefault();
        const p = this.state.party;
        this.switchTo(p[(p.indexOf(this.state.activeChar) + 1) % p.length]);
      }
      if (e.key === 'h' || e.key === 'H') this.showHotspots = !this.showHotspots;
      if (e.key >= '1' && e.key <= '9') this.verbs.setByIndex(Number(e.key) - 1);
    });
  }

  onSceneClick(e, quick) {
    this.sound.unlock();
    if (this.busy) { this.skip?.(); return; }
    const [x, y] = this.scenePos(e);
    const obj = this.objectAt(x, y);
    if (!obj) {
      this.resetSelection();
      this.walkTo(x, y);
      return;
    }
    if (quick) this.quickAction(obj);
    else this.select(obj);
  }

  // ---- Spielschleife ----------------------------------------------------
  start() {
    let last = performance.now();
    const frame = (now) => {
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      for (const a of Object.values(this.actors)) a.update(dt);
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
    for (const a of this.actorsInRoom().sort((p, q) => p.y - q.y)) a.draw(ctx);
    if (this.showHotspots) drawHotspotOutlines(ctx, this.visibleHotspots());
  }
}

async function boot() {
  const res = await fetch('/api/data');
  const data = await res.json();
  const game = new Game(data);
  window.adventure = game; // zum Ausprobieren in der Browser-Konsole
  game.start();

  const title = document.getElementById('title');
  title.addEventListener('click', () => {
    title.hidden = true;
    game.sound.unlock();
    game.enterRoom(data.start.room);
  }, { once: true });
}

boot();
