# Voice

One TTS call per segment → `audio/<id>.wav`. Knowing each segment's length is what lets scenes sync to
words. `engine/tts.py` does it (reads `brand.json → voice`), trims and normalizes each file.

## Recommended: QVox (your own cloned voice, local and free)

[**QVox — qwen3-tts-api**](https://github.com/tecnomanu/qwen3-tts-api) is a local Qwen3-TTS server with an
OpenAI-style API, web panel, CLI and cloneable voices (MLX on Apple Silicon, PyTorch on CUDA/ROCm/CPU).
It's what these styles were built with.

```bash
npm install -g qwen3-tts-api      # installs the `qvox` command
qvox setup                        # checks requirements, creates config
qvox serve                        # API + panel at http://127.0.0.1:5111
qvox voice add my-voice voice-note.ogg --consent   # 25–40 s of clean speech → a cloneable voice
```

`brand.json`:
```json
"voice": { "provider": "qvox", "url": "http://127.0.0.1:5111", "clone": "my-voice", "language": "Spanish",
           "temperature": 0.65, "seed": 1234,
           "en": { "clone": "my-voice-en", "language": "English", "temperature": 0.4 } }
```
Then `python3 tts.py` (main language) and `python3 tts.py --lang en`.

What worked in practice:
- **Clone from a clean, narrative recording** in the register you want (explaining a demo ≠ telling a joke).
  The clone copies timbre, not accent: for a regional accent spell sounds phonetically in `say`
  (e.g. Rioplatense Spanish: `ll`/`y` → `sh`), keep the real spelling in `cap`.
- **Loanwords:** write them how they should sound (`"skills"` → `"eskíls"`, `"Codex"` → `"Cóudecs"`,
  `"Claude Code"` → `"Clod Cud"`, `"widgets"` → `"uíguets"`, product acronyms letter by letter).
- **Temperature:** ~0.65 for a cloned Spanish voice, ~0.4 for English. Fixed `seed` keeps takes consistent;
  change the seed to reroll a single bad segment.
- **Second language = second voice.** Generate a clean take with a preset speaker (or record one), add it
  with `qvox voice add`, and clone that — presets alone vary in loudness, a cloned take stays even.
- With `clone`, `instruct` and emotion tags are ignored (different checkpoints).

## Other providers

- **OpenAI** (`provider: "openai"` in `tts.py`): `gpt-4o-mini-tts` + a preset voice, `OPENAI_API_KEY`.
- **ElevenLabs**: `/v1/text-to-speech/<voice_id>`, then convert to wav 48 kHz.
- **Piper / `say` (macOS)**: fine for drafts and timing tests.
- **No voice:** silent wavs of the length you want per segment; captions become on-screen text.

## Cleanup and QA

`tts.py` trims the start, trims the tail at **−60 dB keeping ~0.12 s** (at −45 dB the final "s" gets cut)
and normalizes to **−16 LUFS**. Then, for every segment:

```bash
python3 transcribe.py audio/s01.wav words/s01.json es        # prints what was actually said
```
Compare with the script. If a word is wrong: phonetic spelling in `say` → change seed → rephrase.
Common failures: tiny isolated phrases change the timbre (merge them, or give them their own segment
with a pause); a word that keeps coming out as another one ("un agente" → "una gente") needs a rephrase.
Sentences that need a pause or a change of intonation go in separate segments with `gap`.
