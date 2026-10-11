# Music

Suggest beds from **Pixabay Music** — free for commercial use, no attribution required under the
Pixabay Content License. Download them into the user's kit (`assets/music/`); **don't redistribute the
files on their own** (e.g. committing them to a public repo), the license forbids standalone distribution.

- Search: https://pixabay.com/music/search/reels%20background/
- Other useful searches: `upbeat corporate`, `lofi`, `tech`, `motivational`, `minimal`.
- Tracks that worked well for 20–90 s explainers (search by name on Pixabay):
  - "Instagram Reels Marketing Music" by **monume** — constant, emotional; a safe default.
  - "Catchy Reels School" by **maeve** — brighter, playful.
  - "Lofi Reel" by **zephiramusic** — calm, lofi.

Ask the user for the mood (energetic / friendly / calm / dramatic) and suggest 2–3 options; keep the
chosen default in `brand.json`. Pick a track longer than the video, or loop with a crossfade.

Mix: voice −16 LUFS, bed **−35 LUFS** (at −31 it already competes with the voice), fade in 0.6 s,
fade out the last 2 s. `make.sh` does this when `MUSIC=` is set.
