# Captions (subtitles)

Captions are **burned into the video** by default and are karaoke-style: the chunk appears, each word
lights up exactly when it's spoken. Most people watch reels muted, so captions are not optional.

## Where the text comes from

- `cap` in `script.json` is the caption text (real spelling). `say` is what the TTS reads (phonetic).
  They can differ: `build_timings.py` aligns caption words to the spoken words by relative position.
- Timing comes from `transcribe.py` (faster-whisper word timestamps) on each segment.
- Second language: `cap_en` + its own voice → `timings-en.js`. Never put second-language captions over
  the first-language voice if a second voice is possible.

## How they behave (engine)

- Chunks of `STYLE.capMax` words (3 for big punchy type, 4 default), cut early at punctuation.
- A chunk shows from its first word to the next chunk, and stays 0.25 s after the segment ends.
- Classes: `.w` upcoming, `.w.on` already spoken, `.w.act` the word being spoken now.
  `.w[data-k=brandname]` targets a word (normalized: lowercase, no accents/punctuation) to color names.
- `?nocap` / `--nocap` hides them (covers, thumbnails, clean versions).

## Look (each style defines it)

| Style | Caption look |
|---|---|
| stamp | uppercase grotesk; active word in an accent box with black border + hard shadow |
| notebook | bold sans; active word with a yellow highlighter stroke |
| desktop | frosted-glass pill; active word in the accent color |
| neon-night | white; active word neon with glow |
| poster | foreground color at 30 % → 100 %; active word in the theme accent (changes with the background) |
| blueprint | white; active word accent + thick underline |

Rules: ≥ 54 px (vertical 1080 wide), weight 700–800, upcoming words at ~22–30 % opacity, never more than
two lines. Position: vertical ~1500–1600 px from the top (above the platform UI at the bottom 18 %);
horizontal ~84 % of the height. Don't let scene elements overlap the caption band — check stills.

## Platform subtitles / clean version

`python3 make_srt.py timings.js video.srt` (or `timings-en.js`) exports an .srt from the same timings, for
YouTube/LinkedIn uploads or a version rendered with `--nocap`. Don't upload an .srt together with a video
that already has burned captions (double subtitles).
