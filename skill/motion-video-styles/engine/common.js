// motion-video-styles engine: time-driven GSAP scenes, word-synced karaoke captions, deterministic render.
// A scene page defines window.STYLE = { capMax, pre(h), build(tl, h), frame(t, h) } and loads this file last.
// Needs (before this file): gsap.min.js and timings.js (window.T, made by build_timings.py).
const Q = new URLSearchParams(location.search);
const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const SEG = Object.fromEntries(T.segs.map(s => [s.id, s]));
const st = id => SEG[id].start, en = id => SEG[id].end;
const nrm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]/g, '');
// Time (s) of the n-th spoken word in segment `id` containing `m`. Cue every animation to a word.
function W(id, m, n = 0) { let c = 0; for (const w of SEG[id].words) if (nrm(w.w).includes(nrm(m))) { if (c++ === n) return w.t; } console.warn('cue not found', id, m); return st(id); }
const hsh = n => { const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); }; // deterministic "random"
const tl = gsap.timeline({ paused: true });
const typers = [], counters = [];
const E = { o: 'power3.out', io: 'power2.inOut', back: 'back.out(1.7)', in: 'power2.in' };
const H = {
  W, st, en, hsh, E, $, $$,
  pop(sel, t, o = {}) { tl.fromTo(sel, { autoAlpha: 0, scale: o.s ?? .6, y: o.y ?? 30, rotation: o.r ?? 0 }, { autoAlpha: 1, scale: 1, y: 0, rotation: o.r2 ?? 0, duration: o.d ?? .55, ease: o.e ?? E.back, stagger: o.st ?? 0 }, t); },
  rise(sel, t, o = {}) { tl.fromTo(sel, { autoAlpha: 0, y: o.y ?? 80 }, { autoAlpha: 1, y: 0, duration: o.d ?? .7, ease: E.o, stagger: o.st ?? 0 }, t); },
  hide(sel, t, d = .3) { tl.to(sel, { autoAlpha: 0, duration: d, ease: 'none' }, t); },
  type(el, text, t0, cps = 28) { typers.push({ el: typeof el === 'string' ? $(el) : el, text, t0, cps }); },
  count(el, to, t0, d = 1, dec = false) { counters.push({ el: typeof el === 'string' ? $(el) : el, to, t0, d, dec }); },
  draw(sel, t, d = .6) { $$(sel).forEach(p => { const L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; tl.to(p, { strokeDashoffset: 0, duration: d, ease: E.io }, t); }); },
};

// Captions: the page CSS decides the look of #cap .w / .w.on (already spoken) / .w.act (being spoken).
let CH = [], lastC = null;
function buildCaps(max) {
  for (const s of T.segs) {
    let cur = [];
    s.words.forEach((w, i) => { cur.push(w); if (/[.,:;?!]$/.test(w.w) || cur.length >= max || i === s.words.length - 1) { CH.push({ seg: s, words: cur }); cur = []; } });
  }
  CH.forEach((c, i) => { const nx = CH[i + 1]; c.t0 = c.words[0].t - .06; c.t1 = (nx && nx.seg === c.seg) ? nx.words[0].t - .06 : c.seg.end + .25; });
}
function renderCaps(t) {
  const cap = $('#cap'); if (!cap) return; const c = CH.find(c => t >= c.t0 && t < c.t1);
  if (c !== lastC) { cap.innerHTML = c ? c.words.map(w => `<span class="w" data-k="${nrm(w.w)}">${w.w}</span>`).join(' ') : ''; lastC = c; }
  cap.style.visibility = c ? 'visible' : 'hidden'; if (!c) return;
  c.words.forEach((w, i) => {
    const el = cap.children[i], on = t >= w.t - .04, act = on && (i === c.words.length - 1 || t < c.words[i + 1].t - .04);
    el.classList.toggle('on', on); el.classList.toggle('act', act);
    const k = Math.min(1, Math.max(0, (t - w.t + .04) / .12)); el.style.transform = `translateY(${(1 - k) * 10}px)`;
  });
  cap.style.opacity = Math.min(1, (t - c.t0) / .14);
}

// Everything is a pure function of t: seek the timeline, then per-frame effects. Never use Date, Math.random or CSS animations.
function renderAt(t) {
  tl.seek(t, false);
  if (!Q.has('nocap')) renderCaps(t); else if ($('#cap')) $('#cap').innerHTML = '';
  for (const ty of typers) { const n = Math.max(0, Math.min(ty.text.length, Math.floor((t - ty.t0) * ty.cps))); const s = ty.text.slice(0, n); if (ty.el.textContent !== s) ty.el.textContent = s; }
  for (const c of counters) { const k = Math.max(0, Math.min(1, (t - c.t0) / c.d)); const v = c.to * (1 - Math.pow(1 - k, 3)); c.el.textContent = c.dec ? v.toFixed(1) : Math.round(v); }
  STYLE.frame && STYLE.frame(t, H);
}
window.renderAt = renderAt;

(async () => {
  STYLE.pre && STYLE.pre(H);
  STYLE.build(tl, H);
  tl.set({}, {}, T.total);
  buildCaps(STYLE.capMax || 4);
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => { })));
  window.TOTAL = T.total; window.READY = true;
  if (Q.has('t')) renderAt(+Q.get('t'));
  else if (Q.has('play')) { const t0 = performance.now(); const f = () => { renderAt(((performance.now() - t0) / 1000) % T.total); requestAnimationFrame(f); }; f(); }
  else renderAt(0);
})();
