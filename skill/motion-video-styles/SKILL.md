---
name: motion-video-styles
description: Guide a user from zero to a reusable video kit for vertical (9:16) or horizontal (16:9) motion-graphics videos — reels, shorts, product explainers — in one of 7 named styles (pastel, stamp, notebook, desktop, neon-night, poster, blueprint), adapted to their own brand. HTML + GSAP scenes driven by voice timing, karaoke captions, deterministic Playwright render, music suggestions. Use when the user wants to make animated social videos, set up a video style/brand kit, or pick a visual style for reels.
---

# Motion video styles

You help the user build **their own video kit** (a folder) and then make videos with it. No camera,
no editor: scenes are an HTML page animated with GSAP, every animation is cued to a spoken word, and
the video is captured frame by frame with Playwright and muxed with ffmpeg.

Be economical: don't look at many frames (images cost tokens). Render 2–4 stills to check a scene,
then do the full render.

## 1 · Onboarding (once per user)

Ask, briefly, and save the answers in `brand.json` (template: `engine/brand.example.json`):

1. Brand name, handle, logo file (PNG/SVG), and 2–4 brand colors (or offer to derive them).
2. Format: **vertical 1080×1920** (reels/shorts/TikTok) or **horizontal 1920×1080** (YouTube) — or both.
3. Languages (one voice track per language; never captions-only translations if a voice is possible).
4. Voice: **recommend [QVox](https://github.com/tecnomanu/qwen3-tts-api)** (local Qwen3-TTS, free, clones their
   own voice from a 25–40 s recording; `npm i -g qwen3-tts-api`). Alternatives: OpenAI, ElevenLabs, Piper,
   or no voice (music + on-screen text). One voice per language. Setup in `references/voice.md`.
5. **Style**: show the 7 options below (the README has a screenshot of each) and let them pick.
   Never pick for them. If they want, mix (e.g. desktop scenes + notebook hand-drawn marks).

Then create the kit:

```bash
cp -R <this-skill>/engine my-video-kit && cd my-video-kit
npm i && npx playwright install chromium     # once
pip install faster-whisper                    # word timestamps (local, free)
```

Apply the chosen style: copy the tokens, fonts and components from `references/styles/<style>.md`
into `scenes.html`, replacing the neutral starter CSS, and swap colors/fonts for the brand's.
Save a `STYLE.md` in the kit with what was decided (style, colors, fonts, caption look, voice, music).

## 2 · Each video

1. **Script** → `script.json`: one segment per sentence/beat (`id`, `cap`, optional `say` with phonetic
   fixes for the TTS, `gap` ~0.6 s at scene changes). Structure that works: hook question → twist
   ("wrong question") → one block per idea → hard data → recap → CTA. Keep it affirmative. 20–60 s.
2. **Voice** → `python3 tts.py` (one wav per segment, QVox by default; `references/voice.md`). Then
   `python3 transcribe.py audio/<id>.wav words/<id>.json <lang>` for each segment. Read the transcript:
   if a word came out wrong, rewrite `say` (phonetic spelling) or change `SEED=` and regenerate that id.
3. **Timings** → `python3 build_timings.py` (writes `timings.js` and `voice.wav`).
4. **Scenes** → write `STYLE.build(tl, h)` in `scenes.html`. Cue everything with `h.W('s02','question')`.
   Recipes per style in `references/styles/`, engine API in `references/engine.md`.
5. **Check** → `node render.mjs --stills=2,8,15 [--w=1920 --h=1080]` and look at those few images.
6. **Render** → `MUSIC=path/to/bed.mp3 bash make.sh out/video-en.mp4 [--lang en] [--w 1920 --h 1080]`.
7. **Cover** → `node render.mjs --stills=<hook time> --nocap --prefix=cover-` (the first frame is
   often empty, so platforms need an explicit cover).
8. **Subtitles file** (optional) → `python3 make_srt.py timings.js out/video.srt` for platforms that show
   their own subtitles, only with a `--nocap` render.

Second language: add `cap_en` (and `say_en`) to each segment, generate `audio_en/` + `words_en/`,
`python3 build_timings.py --lang en`, and in `scenes.html` load `timings-en.js` (see engine.md).

## The 7 styles

| Style | Look | Good for |
|---|---|---|
| `pastel` | Soft editorial light: cream page, drifting pastel clouds, serif headline with italic accent word, white cards, live UI mockups, light→dark panel wipe | product explainers and comparisons that feel premium |
| `stamp` | Neo-brutalist light: bone paper grid, huge grotesk, thick black borders + hard offset shadows, 2 loud accents, ticker | comparisons, launches, high energy |
| `notebook` | Stickers with tape on graph paper, handwriting, circles/strikes/arrows that draw themselves, highlighter | friendly explainers, tips, "how I do it" |
| `desktop` | The product as an OS: light desktop, menu bar, dock, windows that open and drag, notifications, dialogs, cursor, installer | software demos, apps, SaaS |
| `neon-night` | Dark: near-black, one neon accent with glow, condensed display type, mono labels, 3D card flips, glitch | brand identity in a dark feed, tech |
| `poster` | Full-bleed saturated color that switches per scene, display type rising from masks, Bauhaus shapes | strong hooks, breaking feed monotony |
| `blueprint` | Technical drawing: blue grid, everything drawn in white lines, dimensions, notes, schematics, approval stamp | architecture, "how it works inside" |

## Captions

Burned-in karaoke captions are on by default (most viewers watch muted): text from `cap`, timing from the
voice, active word highlighted, look defined by the style, kept above the bottom platform UI. Everything
about them — chunking, classes, per-style look, sizes, positions, .srt export — in `references/captions.md`.

## Music

Suggest royalty-free beds from Pixabay Music (free license, no attribution required; don't redistribute
the files themselves) — see `references/music.md`. Bed at **−35 LUFS** under a voice at −16 LUFS.

## Rules

- Deterministic: animate only through the GSAP timeline or `frame(t)`. No CSS animations, `Date`,
  `Math.random` (use `h.hsh(i)`), or video/SVG SMIL (strip `<animate>` from logos).
- Keep text inside safe areas: top ~12% and bottom ~18% are covered by platform UI in vertical video.
- Long renders run in the background (`nohup … &`); a 60 s video is ~2–4 min.
- Fonts locally (`@fontsource/*` packages), never from a CDN at render time.
- Never use real personal data in screenshots/mockups: fictional names and companies.
