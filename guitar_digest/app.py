"""Ask — Gradio demo

Wraps ``ask()`` in a one-textbox, one-button UI: type a question, get an
answer grounded in the single lesson it cites.

    uv run python -m guitar_digest.app
"""

from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

from .ask import ask

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def answer(question: str) -> tuple[str, str]:
    result = ask(question)
    source = f"**Source:** {result.source}" if result.source else ""
    return result.answer, source


with gr.Blocks(title="Guitar Theory — Ask") as demo:
    gr.Markdown(
        "# 🎸 Ask my guitar theory\n"
        "Single-turn RAG over 10 lessons. Every answer is grounded strictly in "
        "the one lesson it cites — if it isn't in the lessons, it says so."
    )
    question = gr.Textbox(label="Question", placeholder="e.g. What is timbre?", lines=2)
    ask_btn = gr.Button("Ask", variant="primary")
    answer_box = gr.Markdown(label="Answer")
    source_box = gr.Markdown()

    ask_btn.click(answer, inputs=question, outputs=[answer_box, source_box])
    question.submit(answer, inputs=question, outputs=[answer_box, source_box])

    gr.Examples(
        examples=[
            "What are the 6 MAIN AREAS of MUSIC?",
            "How is TIMBRE different than PITCH?",
            "What is EAR TRAINING and why is it so IMPORTANT?",
        ],
        inputs=question,
    )


if __name__ == "__main__":
    demo.launch()
