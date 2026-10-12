#!/usr/bin/env python3
"""Voice per segment → audio/<id>.wav (or audio_<lang>/). Default backend: QVox (https://github.com/tecnomanu/qwen3-tts-api),
a local Qwen3-TTS server with an OpenAI-style API and cloneable voices. Any OpenAI-compatible /v1/audio/speech works too.

  python3 tts.py                        # all segments, main language (reads "say" or "cap")
  python3 tts.py s03 s07                # only these segments
  python3 tts.py --lang en              # second language (reads "say_en" or "cap_en", writes audio_en/)

Settings come from brand.json → "voice", for example:
  "voice": {"provider": "qvox", "url": "http://127.0.0.1:5111", "clone": "my-voice", "language": "Spanish",
            "temperature": 0.65, "seed": 1234,
            "en": {"clone": "my-voice-en", "language": "English", "temperature": 0.4}}
OpenAI: {"provider": "openai", "url": "https://api.openai.com", "model": "gpt-4o-mini-tts", "voice": "alloy"} + OPENAI_API_KEY.
"""
import json, os, sys, subprocess, urllib.request, pathlib

ROOT = pathlib.Path(__file__).parent
args = sys.argv[1:]
lang = None
if "--lang" in args:
    i = args.index("--lang"); lang = args[i + 1]; del args[i:i + 2]
only = set(args)
cfg = json.loads((ROOT / "brand.json").read_text()).get("voice", {}) if (ROOT / "brand.json").exists() else {}
if lang and isinstance(cfg.get(lang), dict):
    cfg = {**cfg, **cfg[lang]}
out_dir = ROOT / (f"audio_{lang}" if lang else "audio"); out_dir.mkdir(exist_ok=True)
segs = json.loads((ROOT / "script.json").read_text())["segments"]
provider = cfg.get("provider", "qvox")
url = cfg.get("url", "http://127.0.0.1:5111").rstrip("/") + "/v1/audio/speech"

for s in segs:
    if only and s["id"] not in only:
        continue
    sfx = f"_{lang}" if lang else ""
    text = s.get("say" + sfx) or s.get("cap" + sfx) or s["cap"]
    if provider == "openai":
        body = {"model": cfg.get("model", "gpt-4o-mini-tts"), "voice": cfg.get("voice", "alloy"), "input": text, "response_format": "wav"}
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', '')}"}
    else:  # qvox
        body = {"input": text, "language": cfg.get("language", "English"), "temperature": cfg.get("temperature", 0.65),
                "seed": int(os.environ.get("SEED", cfg.get("seed", 1234))), "split": False}
        if cfg.get("clone"): body["clone"] = cfg["clone"]          # a voice added with `qvox voice add`
        elif cfg.get("voice"): body["voice"] = cfg["voice"]        # a preset speaker
        if cfg.get("instruct") and not cfg.get("clone"): body["instruct"] = cfg["instruct"]
        headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    raw = out_dir / f"{s['id']}.raw.wav"
    with urllib.request.urlopen(req, timeout=900) as r:
        raw.write_bytes(r.read())
    # trim the start, keep a short tail (-60 dB / 0.12 s so final consonants survive), normalize to -16 LUFS
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-60dB:start_silence=0.12,areverse,"
                    "loudnorm=I=-16:TP=-1.5,aresample=48000", "-ac", "1", str(out_dir / f"{s['id']}.wav")], check=True)
    raw.unlink()
    print(s["id"], "ok", flush=True)
