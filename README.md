# ⚡ Pixel Clash v0.3: Sprite Edition

A Streamlit-hosted pixel-art fighting game. **The actual character sprite sheets are committed to GitHub**, so you can preview and edit them without running the generator.

## 🎨 Browse the real character sprites

Each PNG contains **32 hand-designed frames** (8 columns × 4 rows; individual frames are 48 × 64 pixels).

- [Ember](assets/characters/ember/sprites.png)
- [Volt](assets/characters/volt/sprites.png)
- [Onyx](assets/characters/onyx/sprites.png)

All three are original placeholder-quality pixel-art fighters intended to be refined. They animate in real time, including idle, walk, jump, punches, kicks, special attacks, hurt, blocking, and KO.

### Folder structure

```text
PixelClash/
├── app.py
├── game.js
├── game.html
├── game.css
├── characters.json
├── generate_sprites.py
├── requirements.txt
└── assets/
    └── characters/
        ├── ember/sprites.png
        ├── volt/sprites.png
        └── onyx/sprites.png
```

### Animation layout

| Animation | Frames (0-based) |
|---|---|
| Idle | 0–3 |
| Walk | 4–9 |
| Jump | 10–11 |
| Punch | 12–15 |
| Kick | 16–19 |
| Special | 20–23 |
| Hurt | 24–25 |
| Block | 26–27 |
| KO | 28–31 |

Frame indexes run left to right, top to bottom in each PNG.

### How sprites load

`characters.json` lists each fighter's own `sprite.sheet` file, `row: 0`, frame size, columns, and scaling. `app.py` reads those PNGs **from the repository** and embeds the image data into the Streamlit game iframe. No external image server is needed. A generated fallback remains for older rosters that reference `assets/fighters.png`.

To add a character with custom art, add `assets/characters/new_fighter/sprites.png` and update `characters.json`. The current renderer expects 48 × 64 pixel frames in the above order (8 columns; 4 rows). In a future update we can support more flexible per-character animation maps.

**Regenerating starter art:** Install dependencies, then run `python generate_sprites.py`. This recreates the individual tracked PNGs and a combined `assets/fighters.png` preview locally. Editing a generated PNG by hand is fine, but running the generator again will overwrite it.

## Play and deploy

[Streamlit Community Cloud](https://share.streamlit.io/): choose GitHub repo `nate3d348b/PixelClash`, branch `main`, and entrypoint `app.py`.

Locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Controls: **A/D** walk, **W** jump, **S** block, **J** punch, **K** kick, **L** special. Mobile touch buttons are provided. Best-of-three rounds against a CPU opponent.

This is an original hobby-game prototype, not a finished arcade game. Online multiplayer is not implemented.
