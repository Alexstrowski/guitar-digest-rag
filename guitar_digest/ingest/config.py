from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEORY = ROOT / "theory.md"
CHROMA_DIR = ROOT / "chroma"
CARDS_PATH = ROOT / "cards.json"

COLLECTION = "guitar_theory"
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"
TOP_K = 5

SYSTEM_PROMPT = (
    "You answer questions about guitar theory using ONLY the lesson excerpts provided. "
    "Write a clear, self-contained answer of 2-4 sentences. "
    "If the excerpts do not contain the answer, say so plainly instead of guessing. "
    "Set `source` to exactly ONE lesson label (e.g. 'Lesson 4 — Basic Stuff About Chords'), "
    "the single excerpt that most supports your answer. Never list more than one lesson."
)
