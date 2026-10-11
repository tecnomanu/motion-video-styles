# blueprint — technical drawing

A blue drafting sheet where the idea is drawn as you explain it: boxes, dimensions, notes with leader
lines, wiring diagrams, an org chart, and an approval stamp at the end.

**Fonts:** `Space Grotesk` 700 titles, `JetBrains Mono` labels/notes, captions Space Grotesk 700.
**Tokens:**
```css
:root{--wh:#F4F7FF;--accent:#C7F536;--dim:rgba(244,247,255,.55)}
#stage{background:radial-gradient(ellipse at 50% 40%,#2353C4 0%,#1C47B0 55%,#163A92 100%);color:var(--wh)}
#grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(rgba(255,255,255,.16) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.16) 2px,transparent 2px);background-size:30px 30px,30px 30px,150px 150px,150px 150px}
.lab{font:500 24px/1 "JetBrains Mono";letter-spacing:.1em;color:var(--dim);text-transform:uppercase} /* "SHEET 01 · BRAND", "SCALE 1:1", "FIG. 01 — …" */
svg#ink{position:absolute;inset:0;fill:none;stroke:var(--wh);stroke-width:4;stroke-linecap:round} /* one SVG for all lines */
.note{font:500 30px/1.3 "JetBrains Mono"} .note b{color:var(--accent);font-weight:500} /* "NOTE 1 …" */
#stamp{border:6px double var(--accent);color:var(--accent);transform:rotate(-6deg);padding:26px;text-align:center}
#cap .w{color:rgba(244,247,255,.3)} #cap .w.on{color:var(--wh)} #cap .w.act{color:var(--accent);text-decoration:underline;text-decoration-thickness:5px;text-underline-offset:10px}
```

**Motion signature**
- Everything is drawn: `h.draw('#box1', t)` on rects/paths, then the icon fades in inside.
- Dimension line above the options with tick marks + label ("3 systems · 940 px").
- Notes with leader lines appear one by one (fictional questions/annotations).
- Correction: a thick accent X drawn over the old title.
- Schematic: `C = A + B` — two boxes, wires (curved paths) drawn into the third (accent stroke), then a
  tree drawn down to nodes (team/features).
- Stamp: `scale 2.2→1, rotation -20→-6` with `power4.in` (it "hits" the paper).

**Horizontal:** the natural sheet format — title block in a corner, diagram centered.
**Don't:** filled heavy shapes, more than one accent color, drop shadows.
