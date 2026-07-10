"""Digest — the push clock.

Sends one active-recall Card per day by email.

Local run:   uv run python -m guitar_digest.digest
Preview:     uv run python -m guitar_digest.digest --dry-run
"""

import argparse
import os

from dotenv import load_dotenv

from .config import PREVIEW_PATH, ROOT
from .mailer import send_email
from .render import render_html, render_subject, render_text
from .scheduler import card_for_today, load_cards


def main() -> None:
    parser = argparse.ArgumentParser(description="Send today's guitar recall card.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render the email to a file and print it instead of sending.",
    )
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    cards = load_cards()
    day_number, card = card_for_today(cards)
    subject = render_subject(card)
    html = render_html(card, day_number)
    text = render_text(card, day_number)

    if args.dry_run:
        PREVIEW_PATH.write_text(html, encoding="utf-8")
        print(f"[dry-run] Day {day_number} · {card.source}")
        print(f"[dry-run] Subject: {subject}")
        print(f"[dry-run] HTML preview written to {PREVIEW_PATH}")
        return

    send_email(subject, html, text)
    print(f"Sent Day {day_number} card ({card.source}) to {os.getenv('GMAIL_USER')}.")
