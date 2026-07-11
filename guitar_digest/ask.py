"""Ask

Single-turn RAG over the frozen Knowledge Base in ``chroma/``: embed the
question, retrieve the top-k lessons, and answer grounded strictly in those
excerpts.

Only *reads* ``chroma/`` (via ``get_collection``; never rebuilds it) and reuses
the ingest config + schema so a live answer behaves exactly like a frozen Card.

Quick smoke test:  uv run python -m guitar_digest.ask "What is timbre?"
"""

import sys
from functools import lru_cache

import chromadb
from openai import OpenAI

from .ingest.config import (
    CHAT_MODEL,
    CHROMA_DIR,
    COLLECTION,
    EMBED_MODEL,
    SYSTEM_PROMPT,
    TOP_K,
)
from .ingest.models import GroundedAnswer


@lru_cache(maxsize=1)
def _client() -> OpenAI:
    return OpenAI()


@lru_cache(maxsize=1)
def _collection():
    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return chroma.get_collection(COLLECTION)


def ask(question: str) -> GroundedAnswer:
    question = question.strip()
    if not question:
        return GroundedAnswer(answer="Please enter a question.", source="")

    client = _client()
    embedding = (
        client.embeddings.create(model=EMBED_MODEL, input=[question]).data[0].embedding
    )
    res = _collection().query(query_embeddings=[embedding], n_results=TOP_K)
    context = "\n\n---\n\n".join(
        f"[Lesson {meta['lesson']} — {meta['title']}]\n{doc}"
        for doc, meta in zip(res["documents"][0], res["metadatas"][0])
    )
    completion = client.chat.completions.parse(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Lesson excerpts:\n\n{context}\n\nQuestion: {question}",
            },
        ],
        response_format=GroundedAnswer,
    )
    return completion.choices[0].message.parsed


if __name__ == "__main__":
    from dotenv import load_dotenv

    from .ingest.config import ROOT

    load_dotenv(ROOT / ".env")
    query = " ".join(sys.argv[1:]) or "What is timbre?"
    result = ask(query)
    print(f"Q: {query}\n\nA: {result.answer}\n\nSource: {result.source}")
