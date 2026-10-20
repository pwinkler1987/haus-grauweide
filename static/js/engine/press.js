// Tippen und langes Drücken: Maus nutzt Klick/Rechtsklick, Touch drückt lange
// für die Standardaktion.

const LONG_PRESS_MS = 450;

export function onPress(el, { tap, long, down }) {
  let timer = null;
  let start = null;
  let longFired = false;
  const cancel = () => { clearTimeout(timer); timer = null; };

  el.addEventListener('pointerdown', (e) => {
    longFired = false;
    if (e.pointerType === 'mouse') return;
    down?.(e);
    start = [e.clientX, e.clientY];
    const pos = { clientX: e.clientX, clientY: e.clientY };
    cancel();
    timer = setTimeout(() => {
      timer = null;
      longFired = true;
      navigator.vibrate?.(15);
      long(pos);
    }, LONG_PRESS_MS);
  });
  el.addEventListener('pointermove', (e) => {
    if (timer && Math.hypot(e.clientX - start[0], e.clientY - start[1]) > 10) cancel();
  });
  el.addEventListener('pointerup', cancel);
  el.addEventListener('pointercancel', cancel);
  el.addEventListener('click', (e) => {
    if (longFired) { longFired = false; return; }
    tap(e);
  });
  el.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    if (timer || longFired) return; // Touch: das lange Drücken übernimmt
    long(e);
  });
}
