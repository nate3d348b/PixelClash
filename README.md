# ⚡ Pixel Clash

A standalone pixel-art fighting game hosted on **Streamlit**. Combat and animation run in JavaScript in the browser while Streamlit serves the game.

## Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/ and choose **Create app**.
2. Select the GitHub repository `nate3d348b/PixelClash`, branch `main`.
3. Set the main file path to `app.py` and deploy.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to play

Select a character and click **START FIGHT** to face the CPU in a best-of-three fight.

- **A / D**: move
- **W**: jump
- **S**: block
- **J**: punch
- **K**: kick
- **L**: special attack

Click inside the game frame to focus keyboard input. Touch controls are included.

## Adding fighters

Fighters are stored in `characters.json`. Each fighter has a unique ID, visual palette, stats, and special type. The initial roster has **Ember, Volt, and Onyx**. Adding deeper custom moves and sprite animations is a future improvement.

## Files

- `app.py`: Streamlit launcher
- `game.html`: game markup
- `game.css`: interface styles
- `game.js`: canvas fight engine and CPU behavior
- `characters.json`: fighter roster
- `requirements.txt`: Python dependency

This is an original **prototype**, not a finished commercial fighting engine. Online multiplayer is not included.
