"""Ask — Streamlit demo

Thin UI over ``ask()``: type a question, get an answer grounded in the single
lesson it cites.

    uv run streamlit run streamlit_app.py
"""

import os
import time
from collections import deque

import streamlit as st
from dotenv import load_dotenv

from guitar_digest.ask import ask


load_dotenv()
try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ.setdefault("OPENAI_API_KEY", st.secrets["OPENAI_API_KEY"])
except Exception:
    pass


MAX_QUESTION_LEN = 500
MAX_QUESTIONS = 10
RATE_WINDOW = 60  # ...per this many seconds, shared globally
_recent_calls: deque[float] = deque()

EXAMPLES = [
    "What are the 6 MAIN AREAS of MUSIC?",
    "How is TIMBRE different than PITCH?",
    "What is EAR TRAINING and why is it so IMPORTANT?",
]


def _rate_limited() -> bool:
    """Sliding-window limiter over the whole app; True means turn this call away."""
    now = time.monotonic()
    while _recent_calls and now - _recent_calls[0] > RATE_WINDOW:
        _recent_calls.popleft()
    if len(_recent_calls) >= MAX_QUESTIONS:
        return True
    _recent_calls.append(now)
    return False


st.set_page_config(page_title="Guitar Theory — Ask", page_icon="🎸")
st.title("🎸 Ask my guitar theory")
st.caption(
    "Single-turn RAG over 10 lessons. Every answer is grounded strictly in the "
    "one lesson it cites — if it isn't in the lessons, it says so."
)

with st.expander("About this demo"):
    st.markdown(
        "Ask my guitar-theory course anything. It answers only from the lessons, "
        "points to the exact one it used, and tells you when the answer isn't there. "
        "The same notes also email me one question a day to keep it fresh."
    )

st.session_state.setdefault("question", "")

st.write("**Try an example:**")
for col, example in zip(st.columns(len(EXAMPLES)), EXAMPLES):
    if col.button(example, use_container_width=True):
        st.session_state.question = example

question = st.text_area(
    "Question", key="question", placeholder="e.g. What is timbre?", height=80
)

if st.button("Ask", type="primary"):
    q = question.strip()
    if not q:
        st.warning("Please enter a question.")
    elif len(q) > MAX_QUESTION_LEN:
        st.warning(f"Question too long — keep it under {MAX_QUESTION_LEN} characters.")
    elif _rate_limited():
        st.warning("⏳ The demo is busy right now. Please wait a minute and try again.")
    else:
        with st.spinner("Thinking…"):
            result = ask(q)
        st.markdown(result.answer)
        if result.source:
            st.info(f"**Source:** {result.source}")
