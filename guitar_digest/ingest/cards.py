from openai import OpenAI

from .config import CHAT_MODEL, TOP_K
from .models import Card, GroundedAnswer
from .retrieval import embed

SYSTEM_PROMPT = (
    "You answer questions about guitar theory using ONLY the lesson excerpts provided. "
    "Write a clear, self-contained answer of 2-4 sentences. "
    "If the excerpts do not contain the answer, say so plainly instead of guessing. "
    "Set `source` to exactly ONE lesson label (e.g. 'Lesson 4 — Basic Stuff About Chords'), "
    "the single excerpt that most supports your answer. Never list more than one lesson."
)


def make_card(client: OpenAI, collection, question: str) -> Card:
    res = collection.query(query_embeddings=embed(client, [question]), n_results=TOP_K)
    context = "\n\n---\n\n".join(
        f"[Lesson {meta['lesson']} — {meta['title']}]\n{doc}"
        for doc, meta in zip(res["documents"][0], res["metadatas"][0])
    )
    completion = client.chat.completions.parse(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Lesson excerpts:\n\n{context}\n\nQuestion: {question}"},
        ],
        response_format=GroundedAnswer,
    )
    grounded = completion.choices[0].message.parsed
    return Card(question=question, answer=grounded.answer, source=grounded.source)
