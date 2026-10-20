"""Streamlit launcher for Pixel Clash.

Combat runs at full frame rate in the browser iframe; Python only assembles
self-contained HTML and embeds sprite-sheet PNGs as data URIs.
"""
import base64
import json
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

HERE = Path(__file__).resolve().parent
st.set_page_config(page_title="Pixel Clash", page_icon="⚡", layout="wide")
st.markdown("""<style>
.block-container {padding-top: .5rem; padding-bottom: .3rem; max-width: 1120px;}
[data-testid="stHeader"] {height: 2rem;}
</style>""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def starter_sheet():
    from generate_sprites import build_atlas_png
    return build_atlas_png()

def load_game() -> str:
    roster = json.loads((HERE / 'characters.json').read_text(encoding='utf-8'))
    if not isinstance(roster, list) or len(roster) < 2:
        raise ValueError('At least two fighters are required.')
    ids = [fighter['id'] for fighter in roster]
    if len(ids) != len(set(ids)):
        raise ValueError('Every fighter must have a unique id.')
    sheets = {}
    for fighter in roster:
        name = fighter.get('sprite', {}).get('sheet')
        if not name:
            continue
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or relative.suffix.lower() != '.png':
            raise ValueError(f'Invalid sprite path for {fighter["id"]}')
        if name not in sheets:
            file_path = HERE / relative
            if file_path.is_file():
                sprite_bytes = file_path.read_bytes()
            elif name == 'assets/fighters.png':
                sprite_bytes = starter_sheet()
            else:
                raise FileNotFoundError(f'Sprite PNG not found: {name}')
            sheets[name] = 'data:image/png;base64,' + base64.b64encode(sprite_bytes).decode('ascii')
    html = (HERE / 'game.html').read_text(encoding='utf-8')
    css = (HERE / 'game.css').read_text(encoding='utf-8')
    javascript = (HERE / 'game.js').read_text(encoding='utf-8')
    def safe_json(value):
        return json.dumps(value, ensure_ascii=True).replace('<', '\\u003c')
    javascript = javascript.replace('__CHARACTERS_JSON__', safe_json(roster))
    javascript = javascript.replace('__SPRITE_SHEETS_JSON__', safe_json(sheets))
    return html.replace('__GAME_CSS__', css).replace('__GAME_JS__', javascript)

components.html(load_game(), height=930, scrolling=True)
