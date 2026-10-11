# Engine API (`common.js`)

A scene page = HTML stage + CSS + `window.STYLE`, then `<script src="common.js">` last.
Load order: gsap → `timings.js` → (optional `timings-en.js` + language switch) → your STYLE → common.js.

```js
window.STYLE = {
  capMax: 4,                 // words per caption chunk (3 for big punchy captions)
  pre(h) { /* build DOM that depends on data (lists, mascots…) */ },
  build(tl, h) { /* all tweens, at absolute times */ },
  frame(t, h) { /* per-frame effects that are a pure function of t: floating, drifting blobs, tickers */ },
};
```

`h` helpers:

| Helper | Use |
|---|---|
| `h.W(seg, word, n=0)` | time the n-th word containing `word` is spoken in `seg` (accents/case ignored) |
| `h.st(seg)` / `h.en(seg)` | start / end of a segment |
| `h.pop(sel, t, {s,y,r,r2,d,e,st})` | scale-pop in (stickers, badges) |
| `h.rise(sel, t, {y,d,st})` | fade + rise in |
| `h.hide(sel, t, d)` | fade out |
| `h.type(sel, text, t0, cps)` | typewriter |
| `h.count(sel, to, t0, d, dec)` | number count-up |
| `h.draw('svg path', t, d)` | draw an SVG stroke (hand-drawn marks, wires, blueprint lines) |
| `h.hsh(i)` | deterministic pseudo-random 0–1 |

Patterns:

```js
// a scene enters at its first segment and leaves before the next scene
const S2 = h.st('s04') - .35;
tl.fromTo('#scene2', { autoAlpha: 0 }, { autoAlpha: 1, duration: .35 }, S2);
tl.to('#scene1', { autoAlpha: 0, y: -60, duration: .4, ease: 'power2.in' }, S2);
// hide everything that appears later at t=0
['#t2', '#badge'].forEach(s => tl.set(s, { autoAlpha: 0 }, 0));
// theme switch (poster style): tween CSS variables
tl.to('#stage', { '--bg': '#C7F536', '--fg': '#0F0F0F', duration: .25 }, h.W('s02', 'wrong'));
// masked line reveal (poster): <div class="ln"><span>TEXT</span></div> with overflow:hidden
tl.fromTo('#l1 span', { yPercent: 110 }, { yPercent: 0, duration: .45, ease: 'power4.out' }, t);
```

Captions: put `<div id="cap"></div>` in the stage and style `#cap .w` (upcoming), `.w.on` (spoken),
`.w.act` (being spoken). `.w[data-k=brandname]` colors a specific word.

Second language: in the page, before your STYLE:
```html
<script src="timings-en.js" onerror="0"></script>
<script>const EN = new URLSearchParams(location.search).get('lang') === 'en'; if (EN && window.T_EN) window.T = window.T_EN;</script>
```
Cue words differ per language: write cues with names that exist in both (product names) or branch
`EN ? h.W('s02','question') : h.W('s02','pregunta')`. Translate on-screen text with a small dictionary.

Horizontal: the stage is `100vw × 100vh`; size type in `vw` for vertical and override with a
`@media (min-aspect-ratio:1/1)` block in `vh` (see `scenes.html`). Render with `--w=1920 --h=1080`.
