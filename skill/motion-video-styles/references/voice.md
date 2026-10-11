# Voice

One TTS call per segment → `audio/<id>.wav` (48 kHz mono is fine). Knowing each segment's length is
what lets scenes sync to words.

- **OpenAI**: `POST /v1/audio/speech` `{model:"gpt-4o-mini-tts", voice:"…", input}` → wav.
- **ElevenLabs**: `/v1/text-to-speech/<voice_id>` with `output_format: pcm_48000` or mp3 → convert.
- **Local clone** (e.g. a local Qwen3-TTS server): pass the reference clip + its transcript
  (`ref_text`), language name, temperature ~0.4–0.65, fixed seed for consistency.
- **Piper / system TTS** (`say` on macOS) for drafts.
- No voice: write `script.json` with fixed durations instead (make silent wavs of the length you want).

Post-process each segment: trim leading silence, trim the tail at **−60 dB keeping ~0.12 s** (−45 dB eats
final "s"), normalize to −16 LUFS:
```bash
ffmpeg -i raw.wav -af "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-60dB:start_silence=0.12,areverse,loudnorm=I=-16:TP=-1.5" -ar 48000 -ac 1 audio/s01.wav
```

QA: run `transcribe.py` on every segment and compare with the script. Fixes that work:
- Spell loanwords phonetically in `say` (keep the real spelling in `cap`).
- Avoid very short isolated phrases (the voice timbre drifts); merge them or give them their own segment with a pause.
- Sentences that need a pause/cadence → separate segments with `gap`.
- If a word keeps coming out wrong, rephrase the sentence instead of rerolling seeds forever.
- A second language gets its own voice (another clone/preset), not the first-language voice with translated captions.
