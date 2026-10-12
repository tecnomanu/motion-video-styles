# pastel — soft editorial light

Calm, premium, lively without shouting: a cream page with large pastel color clouds drifting behind,
an elegant serif headline where the key word is in colored italics, white floating cards with soft
shadows, and UI mockups that build themselves. Each topic gets its own palette of clouds.

**Fonts:** headlines `Instrument Serif` 400 + italic (`@fontsource/instrument-serif`), UI/captions `Inter`
(`@fontsource-variable/inter`), code `JetBrains Mono`.
**Tokens:**
```css
:root{--bg:#F6F4EF;--ink:#17171A;--muted:#6E6E78;--line:rgba(23,23,26,.09);--a1:#7048E8;--a2:#14995E;--a3:#F0532D;--a4:#3E63DD;
  --sh:0 40px 90px rgba(30,30,60,.13),0 6px 18px rgba(30,30,60,.07)}
#stage{background:var(--bg);color:var(--ink);font-family:Inter,sans-serif}
.bgb{position:absolute;width:760px;height:760px;border-radius:50%;filter:blur(110px);opacity:.75} /* 4 clouds; color tweened per scene, position drifts in frame(t) */
#grain{position:absolute;inset:0;background-image:radial-gradient(rgba(0,0,0,.035) 1px,transparent 1px);background-size:6px 6px;opacity:.5}
.kicker{font:600 22px/1 Inter;letter-spacing:.2em;color:var(--muted);text-transform:uppercase}
.title{position:absolute;left:0;right:0;text-align:center;font:400 112px/1.02 "Instrument Serif";letter-spacing:-.01em}
.title em{font-style:italic;color:var(--acc)} /* --acc set per scene on the scene container */
.card{position:absolute;background:#fff;border-radius:34px;box-shadow:var(--sh);overflow:hidden}
.pcard{width:292px;height:436px;border-radius:32px;box-shadow:var(--sh)} /* "option" cards: dark gradient for others, white for the hero */
.qb{display:flex;align-items:center;gap:14px;background:#fff;border-radius:26px;padding:16px 26px 16px 16px;box-shadow:var(--sh);font:600 30px/1 Inter} /* question bubble with a colored dot avatar */
.chip{display:flex;align-items:center;gap:12px;background:#fff;border-radius:999px;padding:14px 24px;box-shadow:0 14px 34px rgba(30,30,60,.12);font:600 26px/1 Inter}
#cap{position:absolute;left:70px;right:70px;top:1500px;text-align:center;font:750 58px/1.18 Inter;letter-spacing:-.015em}
#cap .w{color:rgba(23,23,26,.22)} #cap .w.on{color:var(--ink)} #cap .w.act{color:var(--acc)}
#cap .w[data-k=yourbrand]{color:var(--a2)} /* brand and competitor names keep their color */
```
Cloud palettes per scene (example): hook `#FFD3BF #C9D4FF #C4F0DA #EDD0FF` · product A `#FFC0AC #FFD9A6 #FFC4D3 #FFE3CF` ·
product B `#C3D0FF #D8C8FF #BCE0FF #E3DBFF` · your product `#B8EFD2 #E2F7A0 #BAE9F1 #D2F4C4`.

**Motion signature**
- Scene change: clouds tween to the new palette (`backgroundColor`, 1.1 s), old scene `y:-60, autoAlpha:0`, new scene fades in.
- Header per scene: kicker (`ORG · LICENSE`), logo + name, serif subtitle with italic accent; subtitles swap
  (`y -40 → out`, `y 40 → in`) as the narration moves on.
- Hook: three option cards fly up with rotation (−7°, 0°, 7°) on each name; question bubbles pop; the
  question gets a colored strike-through bar, shrinks up, and the new title enters ("Wrong *question*.").
- Live mockups: a terminal that types, chat bubbles with typing dots, a board whose card moves column to
  column, a browser with an agent cursor and a "Take control" banner, a widget whose bars grow.
- Real product panel inside a window: slow Ken Burns zoom, then a diagonal **light → dark wipe** with a
  "☀ Light → ☾ Dark" pill (shows both themes).
- Mascots (optional): blinking eyes that follow a moving point or the cursor; a portrait drawn with the
  characters of a text file (glyph portrait) that assembles from noise; a bouncing row of mascots.
- Data hit: horizontal bars with count-up numbers and a badge ("−66%"), cued to the spoken numbers.
- Closing: "Meet [mascot that changes] your *[word that scrambles]*", logo, "Free and *open source*", repo pill.

**Scene recipes:** hook (question + 3 cards + bubbles) → twist (strike + "wrong question" + role tags under
cards) → one block per option (header + 2–3 live mockups) → your product (merge A + B → office/team/panel,
channels orbiting a portrait, browser, widget) → data chart → recap (stacked cards, the others dim) → CTA.

**Horizontal:** header left, mockups right; clouds bigger; captions at ~84 % height.
**Don't:** dark mode, saturated full-bleed color (that's `poster`), more than 2 accent colors per scene,
static screenshots without movement.
