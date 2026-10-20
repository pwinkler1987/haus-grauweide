// Sprache der Oberfläche (de/en). Gewählt wird die Gerätesprache, im Menü umschaltbar.
import { getItem, setItem } from './storage.js';

const LANG_KEY = 'grauweide_lang';
export const LANGS = ['de', 'en'];
export let LANG = 'de';

const UI = {
  de: {
    verbs: { open: 'Öffne', close: 'Schließe', give: 'Gib', take: 'Nimm', look: 'Schau an', talk: 'Rede mit', use: 'Benutze', push: 'Drücke', walk: 'Gehe zu' },
    prep: { use: 'mit', give: 'an' },
    reply: {
      look: 'Sieht ganz normal aus.', take: 'Das kann ich nicht mitnehmen.', use: 'Das funktioniert so nicht.',
      open: 'Das lässt sich nicht öffnen.', close: 'Das lässt sich nicht schließen.',
      talk: 'Ich glaube nicht, dass das antwortet.', give: 'Das will ich nicht hergeben.',
      push: 'Da bewegt sich nichts.', combine: 'Das passt nicht zusammen.',
      haveIt: 'Das habe ich doch schon.', carryParty: 'Die Gruppe trage ich nicht auch noch.',
      needFirst: 'Das muss ich erst einmal haben.', keep: 'Das behalte ich lieber.',
      hereTake: 'Hier, nimm {item}.', thanks: 'Danke!',
    },
    title: 'Das Haus Grauweide', key: 'Taste {n}',
    subtitle: 'Ein Spukhaus-Mysterium', start: 'Klicken zum Starten', continue: 'Spielstand laden',
    clickHint: '▼ Klick', menu: 'Menü', rotate: 'Bitte das Gerät quer halten.',
    keys: '1–9 Verben · Tab Figur wechseln · H Hotspots · Rechtsklick: Standardaktion · F5 Speichern · F9 Laden',
    whoComes: 'Wer kommt mit? Wähle {n}.', go: "Los geht's!",
    rideHome: '{names} und {last} radeln nach Hause.\n\nWenn jemand fragt: Alle übernachten bei allen.',
    and: ' und ', others: 'den anderen',
    turn: 'Drehen', cancel: 'Abbrechen', codeTitle: 'Das Messingrad',
    ending: 'Ende ({kind})', kinds: { gut: 'gut', neutral: 'neutral', schlecht: 'schlecht' },
    found: 'Gefundene Enden: {n} von {total}', again: 'Nochmal von vorn', loadLast: 'Letzten Spielstand laden',
    resume: 'Weiterspielen', save: 'Speichern', load: 'Laden', hotspots: 'Hotspots an/aus', newGame: 'Neues Spiel',
    restore: 'Kauf wiederherstellen', privacy: 'Datenschutz-Einstellungen', language: 'Language: English',
    busy: 'Gerade nicht möglich.', saved: 'Gespeichert.', saveFailed: 'Speichern fehlgeschlagen.',
    noSave: 'Kein Spielstand gefunden.', saveOld: 'Spielstand ist zu alt.', loaded: 'Geladen.',
    bought: 'Danke! Die Werbung ist weg.', buyCancel: 'Kauf abgebrochen.', restored: 'Kauf wiederhergestellt.',
    noPurchase: 'Kein Kauf gefunden.', restoreFailed: 'Wiederherstellen fehlgeschlagen.',
  },
  en: {
    verbs: { open: 'Open', close: 'Close', give: 'Give', take: 'Pick up', look: 'Look at', talk: 'Talk to', use: 'Use', push: 'Push', walk: 'Walk to' },
    prep: { use: 'with', give: 'to' },
    reply: {
      look: 'Looks perfectly normal.', take: "I can't take that with me.", use: "That doesn't work.",
      open: "That doesn't open.", close: "That doesn't close.",
      talk: "I don't think it's going to answer.", give: "I'd rather not give that away.",
      push: "It won't budge.", combine: "Those don't go together.",
      haveIt: 'I already have that.', carryParty: "I'm not carrying the whole gang as well.",
      needFirst: 'I need to have that first.', keep: "I'd rather keep that.",
      hereTake: 'Here, take this: {item}.', thanks: 'Thanks!',
    },
    title: 'Grauweide House', key: 'Key {n}',
    subtitle: 'A Haunted House Mystery', start: 'Click to start', continue: 'Load saved game',
    clickHint: '▼ Click', menu: 'Menu', rotate: 'Please turn your device sideways.',
    keys: '1–9 verbs · Tab switch character · H hotspots · Right-click: default action · F5 save · F9 load',
    whoComes: 'Who comes along? Pick {n}.', go: "Let's go!",
    rideHome: '{names} and {last} cycle home.\n\nIf anyone asks: everyone is sleeping over at everyone else\'s.',
    and: ' and ', others: 'the others',
    turn: 'Turn', cancel: 'Cancel', codeTitle: 'The Brass Wheel',
    ending: 'Ending ({kind})', kinds: { gut: 'good', neutral: 'neutral', schlecht: 'bad' },
    found: 'Endings found: {n} of {total}', again: 'Start over', loadLast: 'Load last save',
    resume: 'Resume', save: 'Save', load: 'Load', hotspots: 'Hotspots on/off', newGame: 'New game',
    restore: 'Restore purchase', privacy: 'Privacy settings', language: 'Sprache: Deutsch',
    busy: 'Not right now.', saved: 'Saved.', saveFailed: 'Saving failed.',
    noSave: 'No saved game found.', saveOld: 'This saved game is too old.', loaded: 'Loaded.',
    bought: 'Thank you! The ads are gone.', buyCancel: 'Purchase cancelled.', restored: 'Purchase restored.',
    noPurchase: 'No purchase found.', restoreFailed: 'Restore failed.',
  },
};

export async function initLang() {
  const saved = await getItem(LANG_KEY).catch(() => null);
  const device = (navigator.languages?.[0] ?? navigator.language ?? 'de').slice(0, 2).toLowerCase();
  LANG = LANGS.includes(saved) ? saved : (device === 'de' ? 'de' : 'en');
  document.documentElement.lang = LANG;
  document.title = t('title');
  for (const el of document.querySelectorAll('[data-t]')) el.textContent = t(el.dataset.t);
  for (const el of document.querySelectorAll('[data-t-label]')) el.setAttribute('aria-label', t(el.dataset.tLabel));
  return LANG;
}

export async function switchLang() {
  await setItem(LANG_KEY, LANG === 'de' ? 'en' : 'de');
  window.location.href = window.location.pathname;
}

export function t(path, vars = {}) {
  let v = path.split('.').reduce((o, k) => o?.[k], UI[LANG]);
  if (typeof v !== 'string') v = path.split('.').reduce((o, k) => o?.[k], UI.de) ?? path;
  return v.replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? '');
}

export const dataFile = () => (LANG === 'de' ? 'data.json' : `data.${LANG}.json`);
