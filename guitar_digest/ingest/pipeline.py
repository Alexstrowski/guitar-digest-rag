import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from guitar_digest.ingest.cards import make_card
from guitar_digest.ingest.config import CARDS_PATH, CHROMA_DIR, ROOT, THEORY
from guitar_digest.ingest.parsing import parse_lessons, parse_quiz
from guitar_digest.ingest.retrieval import build_kb


def main() -> None:
    load_dotenv(ROOT / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY not set. Copy .env.example to .env and fill it in."
        )

    client = OpenAI()
    lessons = parse_lessons(THEORY.read_text(encoding="utf-8"))
    questions = parse_quiz(lessons)
    print(f"Parsed {len(lessons)} lessons and {len(questions)} quiz questions.")

    collection = build_kb(client, lessons)
    print(f"Embedded {collection.count()} lessons into Chroma at {CHROMA_DIR.name}/.")

    cards = []
    for i, question in enumerate(questions, 1):
        card = make_card(client, collection, question)
        cards.append(card)
        print(f"  [{i:>2}/{len(questions)}] {card.source}")

    CARDS_PATH.write_text(
        json.dumps([c.model_dump() for c in cards], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {len(cards)} cards to {CARDS_PATH.name}.")
