// Führt die Aktionen aus den Python-Inhalten aus.
//
// Eine Aktion ist:
//   "Text"                        -> Figur sagt den Text
//   "befehl:argument"             -> Befehl (siehe COMMANDS)
//   [aktion, aktion, ...]         -> nacheinander ausführen
//   {if: bedingung, do: ..., else: ...}
//
// Bedingungen (mit "!" verneinbar, als Liste müssen alle gelten):
//   "flag:x"       Flag gesetzt
//   "has:item"     aktive Figur trägt den Gegenstand
//   "char:figur"   diese Figur wird gerade gespielt
//   "party:figur"  Figur gehört zur Gruppe
//   "here:n"       mindestens n Gruppenmitglieder im aktuellen Raum

const COMMANDS = new Set([
  'say', 'sayas', 'narrate', 'set', 'unset', 'take', 'drop', 'goto', 'party_goto',
  'place', 'remove', 'choose', 'sound', 'wait', 'dialog', 'walk', 'face', 'codelock',
]);

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
      case 'has': result = this.game.inventory.includes(arg); break;
      case 'char': result = st.activeChar === arg; break;
      case 'party': result = st.party.includes(arg); break;
      case 'here': result = this.game.partyHere().length >= Number(arg); break;
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
      case 'sayas': {
        const [who, ...rest] = arg.split(':');
        return g.say(rest.join(':'), who);
      }
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
      case 'party_goto': return g.partyGoto(arg);
      case 'place': {
        const [who, room, pos] = arg.split(':');
        return g.placeActor(who, room, pos ? pos.split(',').map(Number) : null);
      }
      case 'remove': return g.removeActor(arg);
      case 'choose': return g.chooseParty(Number(arg));
      case 'dialog': return g.runDialog(arg);
      case 'walk': {
        const [who, pos] = arg.split(':');
        const [x, y] = pos.split(',').map(Number);
        return g.actors[who]?.walkTo(x, y);
      }
      case 'face': {
        const [who, dir] = arg.split(':');
        if (g.actors[who]) g.actors[who].dir = dir === 'left' ? -1 : 1;
        return;
      }
      case 'codelock': {
        const [code, flag] = arg.split(':');
        if (await g.codeLock(code)) g.state.flags[flag] = true;
        return;
      }
    }
  }
}
