# desktop — the product as an operating system

The story happens on a light desktop: windows open, a search bar types the question, notifications
arrive, a system dialog interrupts, the cursor drags windows, an installer finishes. Best for software.

**Fonts:** `Inter` (UI), `JetBrains Mono` (terminal).
**Tokens:**
```css
:root{--ink:#14161B;--muted:#6B7280;--accent:#14995E;--glass:rgba(255,255,255,.62)}
#stage{background:linear-gradient(160deg,#E3F7EC 0%,#E6EEFF 55%,#F6E9FF 100%)} /* + 3 blurred color blobs drifting */
#menubar{position:absolute;left:0;right:0;top:110px;height:66px;background:var(--glass);backdrop-filter:blur(20px);display:flex;align-items:center;gap:34px;padding:0 36px;font:600 26px/1 Inter}
.win{position:absolute;background:#fff;border-radius:24px;box-shadow:0 40px 80px rgba(20,22,27,.18),0 0 0 1px rgba(20,22,27,.06);overflow:hidden}
.tb{height:56px;display:flex;align-items:center;gap:10px;padding:0 20px;background:#F5F5F7;font:600 22px/1 Inter} /* + 3 dots #FF5F57 #FEBC2E #28C840 */
.toast{position:absolute;right:40px;width:560px;background:rgba(255,255,255,.9);backdrop-filter:blur(30px);border-radius:26px;box-shadow:0 20px 40px rgba(20,22,27,.14);padding:20px 24px}
#dock{position:absolute;left:50%;transform:translateX(-50%);top:1395px;height:150px;background:var(--glass);backdrop-filter:blur(24px);border-radius:40px;display:flex;align-items:flex-end;gap:10px;padding:0 22px 16px}
.dlg{position:absolute;width:700px;background:rgba(255,255,255,.95);border-radius:30px;box-shadow:0 50px 100px rgba(20,22,27,.25);padding:44px;text-align:center}
#cap{background:rgba(255,255,255,.6);backdrop-filter:blur(20px);border-radius:30px;padding:18px 24px}
#cap .w{color:rgba(20,22,27,.28)} #cap .w.on{color:var(--ink)} #cap .w.act{color:var(--accent)}
```

**Motion signature**
- Window open: `fromTo(win,{scale:.5,y:200,autoAlpha:0},{scale:1,y:0,autoAlpha:1,duration:.45,ease:'back.out(1.3)'})`.
- Spotlight: a frosted search bar pops, `h.type()` the question, blinking caret in `frame`.
- Notifications slide from the right (`x:620→0`), stacked, avatar + name + message (fictional people).
- System dialog with ⚠️ + title + button; the cursor (SVG arrow) travels and "clicks" (button `scale .92` yoyo).
- Tile windows into columns with `tl.to(win,{left,top,width,height})`.
- Drag & merge: cursor grabs window A/B, they shrink into C, C maximizes into the full app view.
- Dock items bounce one by one (`y:-60` yoyo) when "team/features" is said.
- Installer window: progress bar `scaleX 0→1`, terminal line typed, final toast with the CTA.
- Optional: eyes/mascots in the dock look at the cursor position.

**Horizontal:** the most natural style for 16:9 — real desktop proportions, dock at the bottom.
**Don't:** real screenshots with personal data (build mock UI or run the app with demo data).
