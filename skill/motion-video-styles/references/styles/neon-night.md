# neon-night — dark with one neon accent

The dark feed look: near-black, one neon accent with glow, tall condensed display type, mono labels
like an editorial series ("BRAND / DEV · 35"). Cards flip in 3D; the twist glitches.

**Fonts:** display `Anton` (`@fontsource/anton`), body `Inter` 800, labels `JetBrains Mono`.
**Tokens:**
```css
:root{--bg:#0B0B0C;--card:#141416;--neon:#C7F536;--fg:#F4F2EB;--mut:#8A8A92}
#stage{background:var(--bg);color:var(--fg)}
#glow{position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(199,245,54,.20),transparent 62%)} /* drifts in frame(t) */
#noise{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:5px 5px}
.lab{position:absolute;font:700 24px/1 "JetBrains Mono";letter-spacing:.12em;text-transform:uppercase} /* "BRAND / DEV" top-left, "35 / TOPIC" top-right, handle bottom */
.an{position:absolute;left:80px;right:80px;font:400 176px/.9 Anton;text-transform:uppercase}
.cd{background:var(--card);border:2px solid rgba(199,245,54,.28);border-radius:24px;box-shadow:0 30px 60px rgba(0,0,0,.5);transform-style:preserve-3d}
.cd.hero{border-color:var(--neon);box-shadow:0 0 60px rgba(199,245,54,.25)}
.out{color:transparent;-webkit-text-stroke:3px var(--fg)} /* outline display word */
#cap .w{color:rgba(244,242,235,.25)} #cap .w.on{color:var(--fg)} #cap .w.act{color:var(--neon);text-shadow:0 0 26px rgba(199,245,54,.6)}
```

**Motion signature**
- 3D flip-in: `fromTo(card,{rotationY:-100,y:60},{rotationY:0,y:0,duration:.55,ease:'back.out(1.4)'})`; exit `rotationY:90`.
- Terminal lines: `> question_` typed in mono neon.
- Glitch on the twist: `x` jitter (`.04 s` yoyo ×7) + RGB split `text-shadow: Npx 0 #FF3B6B, -Npx 0 #3BD6FF` toggled per frame; swap title with `ease:'steps(4)'`.
- Braces `{ … }` slide in from the sides around an equation, then `= C` pops with `scale 1.4→1`.
- Mascots/features with neon drop-shadow glow.
- CTA: giant neon word, outline word, logo, neon-bordered box "TRY IT?".

**Horizontal:** title column left, cards/visual right; keep the editorial labels in the corners.
**Don't:** more than one neon accent, pure #000, light gray body text below 60% contrast.
