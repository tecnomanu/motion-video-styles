#!/usr/bin/env python3
"""script.json + audio/<id>.wav + words/<id>.json  →  timings.js (window.T) and voice.wav (all segments placed in time).

script.json: {"segments": [{"id": "s01", "cap": "Text shown in captions", "say": "Text sent to TTS (optional)", "gap": 0.4}, ...]}
words/<id>.json: [{"text","start","end"}, ...] from transcribe.py. Caption words are aligned to spoken words by
relative character position, so `cap` may differ slightly from what was said (phonetic spellings in `say`).
Usage: python3 build_timings.py [--lang en]   (en → audio_en/, words_en/, cap_en, timings-en.js as window.T_EN, voice-en.wav)
"""
import json, pathlib, subprocess, re, sys

ROOT = pathlib.Path(__file__).parent
EN = "--lang" in sys.argv and sys.argv[sys.argv.index("--lang") + 1] != "es"
SUF = "" if not EN else "_" + sys.argv[sys.argv.index("--lang") + 1]
segs = json.loads((ROOT / "script.json").read_text())["segments"]
TAIL = 2.2          # seconds after the last word: never end a video abruptly
DEFAULT_GAP = 0.4   # silence before each segment (use "gap" per segment for scene breaks, ~0.6)

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)

def norm(s):
    return re.sub(r"[^\wáéíóúñü]", "", s.lower())

out, t = [], 0.0
for i, s in enumerate(segs):
    t += s.get("gap", 0.25 if i == 0 else DEFAULT_GAP)
    wav = ROOT / f"audio{SUF}" / f"{s['id']}.wav"
    d = dur(wav)
    ww = json.loads((ROOT / f"words{SUF}" / f"{s['id']}.json").read_text())
    cap = (s.get("cap" + SUF) or s["cap"]).split()
    wl = [len(norm(w["text"])) or 1 for w in ww]; tw = sum(wl); acc = 0; wpos = []
    for L in wl:
        wpos.append((acc + L / 2) / tw); acc += L
    cl = [len(norm(w)) or 1 for w in cap]; tc = sum(cl); acc = 0; words = []
    for k, L in enumerate(cl):
        p = (acc + L / 2) / tc; acc += L
        j = min(range(len(ww)), key=lambda q: abs(wpos[q] - p))
        words.append({"w": cap[k], "t": round(t + ww[j]["start"], 3), "e": round(t + ww[j]["end"], 3)})
    for k in range(1, len(words)):
        if words[k]["t"] <= words[k - 1]["t"]:
            words[k]["t"] = round(words[k - 1]["t"] + 0.08, 3)
    out.append({"id": s["id"], "start": round(t, 3), "end": round(t + d, 3), "words": words})
    t += d

total = round(t + TAIL, 3)
var = "window.T_EN=" if EN else "window.T="
(ROOT / ("timings-en.js" if EN else "timings.js")).write_text(var + json.dumps({"total": total, "segs": out}, ensure_ascii=False) + ";\n")

inputs, filt = [], []
for i, s in enumerate(out):
    inputs += ["-i", str(ROOT / f"audio{SUF}" / f"{s['id']}.wav")]
    ms = int(s["start"] * 1000)
    filt.append(f"[{i}]adelay={ms}|{ms}[a{i}]")
filt.append("".join(f"[a{i}]" for i in range(len(out))) + f"amix=inputs={len(out)}:normalize=0,apad,atrim=0:{total}[v]")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filt),
                "-map", "[v]", "-ar", "48000", "-ac", "1", str(ROOT / ("voice-en.wav" if EN else "voice.wav"))], check=True)
print("total", total)
