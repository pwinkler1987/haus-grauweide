// Speichert auf dem Gerät: in der App über Capacitor Preferences (wird vom
// Betriebssystem nicht weggeräumt), im Browser über localStorage.

function prefs() {
  const cap = window.Capacitor;
  return cap?.isNativePlatform?.() ? cap.Plugins?.Preferences : null;
}

export async function getItem(key) {
  const p = prefs();
  if (p) return (await p.get({ key })).value;
  try { return localStorage.getItem(key); } catch { return null; }
}

export async function setItem(key, value) {
  const p = prefs();
  if (p) return p.set({ key, value });
  localStorage.setItem(key, value);
}

export async function getJSON(key, fallback = null) {
  try { return JSON.parse((await getItem(key)) ?? 'null') ?? fallback; } catch { return fallback; }
}

export const setJSON = (key, value) => setItem(key, JSON.stringify(value));
