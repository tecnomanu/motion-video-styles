# notebook — stickers & handwriting

Warm and personal: a graph-paper page where stickers get slapped on and marks are drawn by hand
while you talk.

**Fonts:** handwriting `Caveat` 500/700 (`@fontsource/caveat`), captions `Inter` 800.
**Tokens:**
```css
:root{--paper:#FBF7EE;--ink:#1F2340;--red:#E8504A;--hi:#FFE45C;--blue:#3E63DD;--green:#14995E}
#paper{position:absolute;inset:0;background-image:linear-gradient(rgba(120,160,210,.22) 2px,transparent 2px),linear-gradient(90deg,rgba(120,160,210,.22) 2px,transparent 2px);background-size:54px 54px}
#margin{position:absolute;top:0;bottom:0;left:96px;width:3px;background:rgba(232,80,74,.45)}
.hand{position:absolute;font:700 132px/1 Caveat;color:var(--ink)}
.stk{position:absolute;background:#fff;border-radius:34px;border:10px solid #fff;box-shadow:0 18px 30px rgba(31,35,64,.18)} /* sticker */
.tape{position:absolute;width:150px;height:46px;background:rgba(232,214,160,.75);top:-26px;left:50%;margin-left:-75px;transform:rotate(-6deg)}
.bub{background:#fff;border:4px solid var(--ink);border-radius:40px 40px 40px 8px;padding:16px 30px;font:700 52px/1 Caveat}
svg.ink{position:absolute;overflow:visible;fill:none;stroke-linecap:round;stroke-linejoin:round} /* hand-drawn marks */
#cap .w{color:rgba(31,35,64,.25)} #cap .w.on{color:var(--ink)}
#cap .w.act{background:linear-gradient(transparent 38%,var(--hi) 38%,var(--hi) 88%,transparent 88%)} /* highlighter */
```

**Motion signature**
- Slap a sticker: `fromTo(el,{scale:1.6,rotation:r*3},{scale:1,rotation:r,duration:.32,ease:'back.out(2.6)'})` with small random `r` (±3–7°).
- Hand marks with `h.draw()`: wobbly ellipse around a word, zigzag scribble to cross out, squiggle
  underline, curved arrows to labels (paths with slightly irregular Béziers, 5–12 px strokes).
- Page turn between scenes: everything flies up (`y:-1900, rotation:-6`) and the new page writes in.
- Starburst sticker (SVG polygon) for "free!/new!" slowly rotating in `frame`.
- Idle: stickers bob ±5 px.

**Scene recipes:** handwritten question + 3 stickers + speech bubbles → scribble over the question,
new phrase underlined, arrows to handwritten labels → sticker math (`A + B → C` with a drawn arrow) →
crossed-out word + highlighted replacement → round mascot/feature stickers slapped around → CTA:
starburst, washi-tape label, logo sticker, handwritten question with arrow pointing to the comments.

**Horizontal:** page with two columns; stickers left, handwriting right.
**Don't:** perfect geometric lines, too many fonts, captions in handwriting (hard to read).
