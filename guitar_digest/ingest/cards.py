from openai import OpenAI

from .config import CHAT_MODEL, SYSTEM_PROMPT, TOP_K
from .models import Card, GroundedAnswer
from .retrieval import embed


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
