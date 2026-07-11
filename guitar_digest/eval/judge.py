from openai import OpenAI

from ..ingest.models import GroundedAnswer
from .config import JUDGE_MODEL, JUDGE_PROMPT
from .models import GoldenItem, Verdict


def judge(client: OpenAI, item: GoldenItem, live: GroundedAnswer) -> Verdict:
    """LLM-as-judge: is the live answer correct and consistent with the reference?"""
    user = (
        f"Question: {item.question}\n\n"
        f"REFERENCE answer: {item.expected_answer}\n\n"
        f"LIVE answer: {live.answer}"
    )
    completion = client.chat.completions.parse(
        model=JUDGE_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": user},
        ],
        response_format=Verdict,
    )
    return completion.choices[0].message.parsed
