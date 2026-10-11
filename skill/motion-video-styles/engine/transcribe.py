#!/usr/bin/env python3
"""Word timestamps with faster-whisper (local, free). pip install faster-whisper
Usage: python3 transcribe.py audio/s01.wav words/s01.json [lang=es] [model=medium]
Also the QA step: compare the printed text with what the segment should say; regenerate the TTS if it differs."""
import sys, json, os
from faster_whisper import WhisperModel

src, dst = sys.argv[1], sys.argv[2]
lang = sys.argv[3] if len(sys.argv) > 3 else "es"
model = WhisperModel(sys.argv[4] if len(sys.argv) > 4 else "medium", device="cpu", compute_type="int8")
segments, _ = model.transcribe(src, language=lang, word_timestamps=True, vad_filter=False, beam_size=5)
words = [{"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s in segments for w in (s.words or []) if w.word.strip()]
os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
json.dump(words, open(dst, "w"), ensure_ascii=False, indent=1)
print(os.path.basename(src), "→", " ".join(w["text"] for w in words))
