#!/bin/bash
# Full render: timings → frames → music mix → final mp4.
#   bash make.sh [out.mp4] [--lang en] [--w 1920 --h 1080]        MUSIC=path/to/bed.mp3 to add a music bed
set -e; cd "$(dirname "$0")"
OUT=${1:-out/video.mp4}; shift || true
LANG_ARG=""; W=1080; H=1920
while [ $# -gt 0 ]; do case $1 in --lang) LANG_ARG=$2; shift 2;; --w) W=$2; shift 2;; --h) H=$2; shift 2;; *) shift;; esac; done
mkdir -p "$(dirname "$OUT")" _work
if [ -n "$LANG_ARG" ] && [ "$LANG_ARG" != es ]; then python3 build_timings.py --lang $LANG_ARG; VOICE=voice-$LANG_ARG.wav; TJ=timings-$LANG_ARG.js; else python3 build_timings.py; VOICE=voice.wav; TJ=timings.js; fi
TOTAL=$(python3 -c "import re;print(re.search(r'\"total\": ([0-9.]+)',open('$TJ').read()).group(1))")
node render.mjs _work/frames.mp4 --w=$W --h=$H ${LANG_ARG:+--lang=$LANG_ARG}
if [ -n "$MUSIC" ]; then
  FO=$(python3 -c "print($TOTAL-2.0)")
  # music far under the voice: bed at -35 LUFS, voice at -16 LUFS
  ffmpeg -hide_banner -loglevel error -y -i $VOICE -i "$MUSIC" -filter_complex \
   "[0]loudnorm=I=-16:TP=-1.5,aresample=48000[v];[1]atrim=0:$TOTAL,loudnorm=I=-35:TP=-8,afade=t=in:d=0.6,afade=t=out:st=$FO:d=2,aresample=48000[m];[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]" \
   -map "[a]" -ac 2 _work/mix.wav
else
  ffmpeg -hide_banner -loglevel error -y -i $VOICE -af "loudnorm=I=-16:TP=-1.5,aresample=48000" -ac 2 _work/mix.wav
fi
ffmpeg -hide_banner -loglevel error -y -i _work/frames.mp4 -i _work/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 23 \
  -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -shortest "$OUT"
ls -la "$OUT"
