# ⚡ Pixel Clash v0.3: Sprite Edition

A Streamlit-hosted, browser-rendered fighting game with **96 original pixel-art animation frames** (32 frames per fighter). Frames cover idle, walk, jump, punch, kick, special, block, hurt, and KO.

## Deploy
On [Streamlit Community Cloud](https://share.streamlit.io/), choose repo `nate3d348b/PixelClash`, branch `main`, entrypoint `app.py`.

## Controls
**A/D** walk, **W** jump, **S** block, **J** punch, **K** kick, **L** special. Touch buttons are available; matches are best of three against CPU.

## Art pipeline
- `generate_sprites.py` contains the original hand-designed pixel-art frames. It generates an indexed **PNG** atlas, 384 × 768 pixels, with eight 48 × 64 frames per row.
- `app.py` generates the starter atlas **in memory** using Pillow and embeds it in the Streamlit iframe. No external image hosting or asset server.
- `characters.json` links characters to `sprite.sheet`, atlas row, frame dimensions, columns, and scale.
- Animation slots: idle 0–3; walk 4–9; jump 10–11; punch 12–15; kick 16–19; special 20–23; hurt 24–25; block 26–27; KO 28–31.
- For future artist-made characters, add their actual `.png` sprite sheet in `assets/characters/` and point `sprite.sheet` to it with `sprite.row: 0`. The loader automatically embeds it.
- Optional: run `python generate_sprites.py` locally to save `assets/fighters.png` for inspection.
- Fighters without sprite art retain the legacy rectangle renderer as a fallback.

## Local development
```bash
pip install -r requirements.txt
streamlit run app.py
```

All included sprite designs are original prototype assets. This is not yet an arcade-quality fighting engine, and online multiplayer is not included.
