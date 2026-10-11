# stamp — neo-brutalist light

Loud, graphic, confident. Blocks slam in like rubber stamps; everything has a thick black border and a
hard offset shadow. Two saturated accents on bone paper.

**Fonts:** display/body `Space Grotesk` 500/700 (`@fontsource/space-grotesk`). Uppercase for titles.
**Tokens:**
```css
:root{--bone:#F4F2EB;--ink:#0F0F0F;--a1:#C7F536;--a2:#3B2FE0;--a3:#FF6B4A;--alert:#FF3B30}
#stage{background:var(--bone);color:var(--ink);font-family:"Space Grotesk",sans-serif}
#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(15,15,15,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(15,15,15,.07) 2px,transparent 2px);background-size:90px 90px}
.nb{border:6px solid var(--ink);box-shadow:14px 14px 0 var(--ink);border-radius:18px}
.big{position:absolute;left:90px;right:90px;font:700 150px/.92 "Space Grotesk";letter-spacing:-.045em;text-transform:uppercase}
.hl{position:relative;display:inline-block;z-index:0} .hl i{position:absolute;left:-14px;right:-14px;top:18%;bottom:6%;z-index:-1;transform-origin:0 50%;border:6px solid var(--ink)} /* marker block behind a word */
.tag{background:var(--ink);color:var(--a1);font:700 30px/1 "Space Grotesk";padding:14px 22px;border-radius:12px;letter-spacing:.08em}
#ticker{position:absolute;left:-20px;right:-20px;top:150px;height:76px;background:var(--ink);transform:rotate(-2deg);overflow:hidden} /* text moved in frame(t) */
#cap .w{color:rgba(15,15,15,.22);padding:0 10px;border:5px solid transparent;border-radius:12px;text-transform:uppercase}
#cap .w.on{color:var(--ink)} #cap .w.act{background:var(--a1);border-color:var(--ink);box-shadow:6px 6px 0 var(--ink)}
```

**Motion signature**
- Slam: `fromTo(el,{x:±900,rotation:±14},{x:0,rotation:∓1.5,duration:.45,ease:'back.out(1.4)'})`.
- Marker reveal: `.hl i` `scaleX 0→1` (.35 s) right when the word is said.
- Red X stamp: two bars `scaleX 0→1` at ±12°, .22 s each, over the old title; then the new title pops at `scale 1.3→1`.
- Ticker: `translateX(-(t*140)%1000)` in `frame`.
- Idle: every `.nb` bobs ±3 px.

**Scene recipes:** stacked name blocks (one per option) → big question with marker → red X → "WRONG
QUESTION" with second accent → equation of tiles `A + B = C` (each tile pops on its word) → strike a word
with a red bar, highlight the replacement → grid of bordered tiles (team/features) dropping with slight
random rotations → CTA on a full accent flash: giant word, black banner rotated −3°, sticker "TRY IT?".

**Horizontal:** blocks become a row; title on the left half, tiles on the right; ticker full width at top.
**Don't:** soft shadows, gradients, more than 3 accents, rounded "friendly" corners above 20 px.
