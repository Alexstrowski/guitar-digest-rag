from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEORY = ROOT / "theory.md"
CHROMA_DIR = ROOT / "chroma"
CARDS_PATH = ROOT / "cards.json"

COLLECTION = "guitar_theory"
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"
TOP_K = 5
