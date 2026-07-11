from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CARDS_PATH = ROOT / "cards.json"
PREVIEW_PATH = ROOT / "digest_preview.html"

# Anchor for the stateless scheduler. Day 0 = first card; it just rotates the
# deck deterministically, so the exact anchor only sets which card shows first.
START_DATE = date(2026, 7, 10)

ASK_URL = "https://guitar-digest-rag-m2crd3rgefjrjqpeabumha.streamlit.app"
