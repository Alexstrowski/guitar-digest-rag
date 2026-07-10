import json
from datetime import date

from .config import CARDS_PATH, START_DATE
from .models import Card


def load_cards() -> list[Card]:
    data = json.loads(CARDS_PATH.read_text(encoding="utf-8"))
    return [Card(**c) for c in data]


def card_for_today(cards: list[Card], today: date | None = None) -> tuple[int, Card]:
    today = today or date.today()
    days = (today - START_DATE).days
    return days, cards[days % len(cards)]
