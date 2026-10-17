// Klänge per WebAudio erzeugt – keine Audiodateien nötig.

const midi = (n) => 440 * 2 ** ((n - 69) / 12);

// Eigene kleine Spieluhr-Melodie für das Radiosignal.
const MELODY = [76, 79, 83, 81, 79, 76, 74, 76, 72, 74, 76, 79, 78, 74, 71];

export class Sound {
  unlock() {
    if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (this.ctx.state === 'suspended') this.ctx.resume();
  }

  play(name) {
    this.unlock();
    const fn = { static: this.static, melody: this.melody, click: this.click, owl: this.owl }[name];
    if (!fn) {
      console.warn('Unbekannter Sound:', name);
      return Promise.resolve();
    }
    const seconds = fn.call(this, this.ctx, this.ctx.currentTime);
    return new Promise((r) => setTimeout(r, seconds * 1000));
  }

  static(ac, t) {
    const len = 1.6;
    const buf = ac.createBuffer(1, ac.sampleRate * len, ac.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    const src = ac.createBufferSource();
    src.buffer = buf;
    const filter = ac.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = 1800;
    const gain = ac.createGain();
    gain.gain.setValueAtTime(0.0, t);
    gain.gain.linearRampToValueAtTime(0.25, t + 0.2);
    gain.gain.linearRampToValueAtTime(0.0, t + len);
    src.connect(filter).connect(gain).connect(ac.destination);
    src.start(t);
    return len;
  }

  melody(ac, t) {
    const step = 0.3;
    MELODY.forEach((note, i) => {
      const start = t + i * step;
      for (const [mult, vol] of [[1, 0.18], [2, 0.05]]) { // Grundton + Oberton = Spieluhr
        const osc = ac.createOscillator();
        const g = ac.createGain();
        osc.type = 'sine';
        osc.frequency.value = midi(note) * mult;
        g.gain.setValueAtTime(vol, start);
        g.gain.exponentialRampToValueAtTime(0.0001, start + 0.9);
        osc.connect(g).connect(ac.destination);
        osc.start(start);
        osc.stop(start + 1);
      }
    });
    return MELODY.length * step + 0.6;
  }

  owl(ac, t) {
    // zwei weiche, abfallende Rufe
    [[0, 0.45], [0.6, 0.8]].forEach(([offset, len]) => {
      const osc = ac.createOscillator();
      const g = ac.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(420, t + offset);
      osc.frequency.exponentialRampToValueAtTime(330, t + offset + len);
      g.gain.setValueAtTime(0.0001, t + offset);
      g.gain.exponentialRampToValueAtTime(0.15, t + offset + 0.08);
      g.gain.exponentialRampToValueAtTime(0.0001, t + offset + len);
      osc.connect(g).connect(ac.destination);
      osc.start(t + offset);
      osc.stop(t + offset + len + 0.05);
    });
    return 1.5;
  }

  click(ac, t) {
    const osc = ac.createOscillator();
    const g = ac.createGain();
    osc.type = 'square';
    osc.frequency.value = 900;
    g.gain.setValueAtTime(0.08, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.05);
    osc.connect(g).connect(ac.destination);
    osc.start(t);
    osc.stop(t + 0.06);
    return 0.1;
  }
}
