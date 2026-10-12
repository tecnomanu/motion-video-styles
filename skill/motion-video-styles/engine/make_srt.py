#!/usr/bin/env python3
"""timings.js → .srt (for platforms that show their own subtitles, or a clean version without burned captions).
Usage: python3 make_srt.py [timings.js] [out.srt] [max_words=6]"""
import json, re, sys

src = sys.argv[1] if len(sys.argv) > 1 else "timings.js"
dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".js", ".srt")
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 6
T = json.loads(re.sub(r"^window\.T(_EN)?=|;\s*$", "", open(src).read().strip()))
fmt = lambda t: f"{int(t // 3600):02}:{int(t % 3600 // 60):02}:{int(t % 60):02},{int(round(t % 1 * 1000)) % 1000:03}"
cues = []
for s in T["segs"]:
    cur = []
    for i, w in enumerate(s["words"]):
        cur.append(w)
        if re.search(r"[.,:;?!]$", w["w"]) or len(cur) >= mx or i == len(s["words"]) - 1:
            cues.append((cur[0]["t"], max(cur[-1]["e"], cur[0]["t"] + .6), " ".join(x["w"] for x in cur))); cur = []
fixed, prev = [], 0.0
for a, b, txt in cues:  # never overlap cues, even if a segment's timing is off
    a = max(a, prev); b = max(b, a + .4); fixed.append((a, b, txt)); prev = b
with open(dst, "w") as f:
    for i, (a, b, txt) in enumerate(fixed, 1):
        f.write(f"{i}\n{fmt(a)} --> {fmt(b)}\n{txt}\n\n")
print(dst, len(cues), "cues")
