# poster — full-bleed color & Bauhaus shapes

Neither white nor dark: the whole frame is a saturated brand color that switches at each turn of the
story. Huge condensed type rises from masks; options are flat geometric shapes.

**Fonts:** `Anton` display, `Inter` 800 captions/body.
**Tokens (themes are CSS variables tweened by GSAP):**
```css
:root{--c1:#3B2FE0;--c2:#C7F536;--c3:#FF6B4A;--bone:#F4F2EB;--ink:#0F0F0F}
#stage{--bg:var(--c1);--fg:var(--bone);--acc:var(--c2);background:var(--bg);color:var(--fg)}
.ln{position:absolute;left:70px;right:70px;overflow:hidden;font:400 230px/1.02 Anton;text-transform:uppercase} .ln span{display:inline-block}
.acc{color:var(--acc)}
.circ{border-radius:50%;background:var(--c3)} .sq{background:var(--bone);border-radius:6px}
.dia{background:var(--c2);border-radius:30px;transform:rotate(45deg);box-shadow:0 0 0 9px var(--ink),14px 14px 0 9px var(--ink)} /* outline so it survives a same-color background */
.bb{background:var(--bone);color:var(--ink);font:700 40px/1 Inter;padding:22px 30px} /* flat speech blocks */
#band{position:absolute;left:0;right:0;height:300px;background:var(--bone)} /* strip for mascots/logos */
#cap .w{color:var(--fg);opacity:.3} #cap .w.on{opacity:1} #cap .w.act{color:var(--acc)}
```

**Motion signature**
- Theme switch on the twist word: `tl.to('#stage',{'--bg':'#C7F536','--fg':'#0F0F0F','--acc':'#3B2FE0',duration:.25},t)`.
  Pattern: c1 → c2 (twist) → c1 (solution) → c2 (CTA).
- Masked line reveal: `span yPercent 110→0` (`power4.out`, .45 s); exit `yPercent -110`.
- Shapes grow with rotation (`scale 0→1, rotation ±90→0`); merge: circle + square slide together,
  shrink and fade while the diamond (the answer) pops with `back.out(2.2)`.
- Band of mascots/logos: `scaleY 0→1`, items bounce in a wave.

**Horizontal:** type on the left two thirds, shapes stacked on the right; band at the bottom.
**Don't:** more than 3 background colors in one video, thin type, small text on saturated color.
