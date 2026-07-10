import os
import smtplib
from email.message import EmailMessage


def send_email(subject: str, html: str, text: str) -> None:
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")
    if not user or not password:
        raise SystemExit(
            "GMAIL_USER / GMAIL_APP_PASSWORD not set. "
            "Copy .env.example to .env and fill in a Gmail app password."
        )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = user
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(user, password)
        server.send_message(msg)
