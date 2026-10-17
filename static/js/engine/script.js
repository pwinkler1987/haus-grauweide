// Führt die Aktionen aus den Python-Inhalten aus.
//
// Eine Aktion ist:
//   "Text"                        -> Figur sagt den Text
//   "befehl:argument"             -> Befehl (siehe COMMANDS)
//   [aktion, aktion, ...]         -> nacheinander ausführen
//   {if: bedingung, do: ..., else: ...}
//
// Bedingungen: "flag:x", "has:gegenstand", "char:figur", mit "!" verneint,
// oder eine Liste (alle müssen gelten).

const COMMANDS = new Set(['say', 'narrate', 'set', 'unset', 'take', 'drop', 'goto', 'sound', 'wait']);

export class ScriptRunner {
  constructor(game) {
    this.game = game;
  }

  check(cond) {
    if (cond == null) return true;
    if (Array.isArray(cond)) return cond.every((c) => this.check(c));
    const negate = cond.startsWith('!');
    const [kind, arg] = (negate ? cond.slice(1) : cond).split(':');
    const st = this.game.state;
    let result;
    switch (kind) {
      case 'flag': result = !!st.flags[arg]; break;
      case 'has': result = st.inventory.includes(arg); break;
      case 'char': result = st.activeChar === arg; break;
      default:
        console.warn('Unbekannte Bedingung:', cond);
        result = false;
    }
    return negate ? !result : result;
  }

  async run(action) {
    if (action == null) return;
    if (typeof action === 'string') return this.command(action);
    if (Array.isArray(action)) {
      for (const a of action) await this.run(a);
      return;
    }
    if ('if' in action) return this.run(this.check(action.if) ? action.do : action.else);
    return this.run(action.do);
  }

  async command(text) {
    const m = text.match(/^(\w+):([\s\S]*)$/);
    if (!m || !COMMANDS.has(m[1])) return this.game.say(text);
    const [, cmd, arg] = m;
    const g = this.game;
    switch (cmd) {
      case 'say': return g.say(arg);
      case 'narrate': return g.narrate(arg);
      case 'set': g.state.flags[arg] = true; return;
      case 'unset': delete g.state.flags[arg]; return;
      case 'take': return g.addItem(arg);
      case 'drop': return g.removeItem(arg);
      case 'sound': return g.sound.play(arg);
      case 'wait': return new Promise((r) => setTimeout(r, Number(arg)));
      case 'goto': {
        const [room, pos] = arg.split(':');
        return g.enterRoom(room, pos ? pos.split(',').map(Number) : null);
      }
    }
  }
}
