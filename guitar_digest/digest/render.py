from html import escape
from urllib.parse import quote

from .config import ASK_URL
from .models import Card


def deep_link(card: Card) -> str:
    return f"{ASK_URL}?q={quote(card.question)}"


def render_subject(card: Card) -> str:
    return f"🎸 Guitar recall — {card.question}"


def render_html(card: Card, day_number: int) -> str:
    q = escape(card.question)
    a = escape(card.answer)
    src = escape(card.source)
    link = escape(deep_link(card))
    return f"""\
<!doctype html>
<html>
  <body style="margin:0;padding:24px 12px;background:#f4f4f5;
               font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
               color:#18181b;">
    <div style="max-width:560px;margin:0 auto;background:#ffffff;border-radius:12px;
                padding:32px;box-shadow:0 1px 3px rgba(0,0,0,.08);">
      <p style="margin:0 0 8px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;
                color:#a1a1aa;">Day {day_number} · Active recall</p>
      <h1 style="margin:0;font-size:21px;line-height:1.35;font-weight:700;">{q}</h1>

      <!-- Reveal-by-distance: whitespace, not a collapsible, keeps the answer
           out of sight so you actually try to recall it first. -->
      <p style="margin:24px 0 0;font-size:13px;color:#a1a1aa;">Try to answer, then scroll ↓</p>
      <div style="height:88px;"></div>
      <hr style="border:none;border-top:1px solid #e4e4e7;margin:0;">
      <div style="height:24px;"></div>

      <p style="margin:0;font-size:16px;line-height:1.6;">{a}</p>
      <p style="margin:20px 0 0;font-size:13px;color:#71717a;">Source: {src}</p>

      <div style="margin-top:28px;">
        <a href="{link}" style="display:inline-block;background:#18181b;color:#ffffff;
                  text-decoration:none;font-size:14px;font-weight:600;
                  padding:11px 18px;border-radius:8px;">Ask a follow-up →</a>
      </div>
    </div>
    <p style="max-width:560px;margin:16px auto 0;font-size:11px;color:#a1a1aa;text-align:center;">
      Guitar Digest · one card a day from your own theory notes
    </p>
  </body>
</html>"""


def render_text(card: Card, day_number: int) -> str:
    return (
        f"Day {day_number} · Active recall\n\n"
        f"Q: {card.question}\n\n"
        f"(try to recall, then read on)\n\n"
        f"{'-' * 40}\n\n"
        f"A: {card.answer}\n\n"
        f"Source: {card.source}\n\n"
        f"Ask a follow-up: {deep_link(card)}\n"
    )
