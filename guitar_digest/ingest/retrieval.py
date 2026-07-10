import shutil

import chromadb
from openai import OpenAI

from .config import CHROMA_DIR, COLLECTION, EMBED_MODEL
from .parsing import label


def embed(client: OpenAI, texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def build_kb(client: OpenAI, lessons: list[dict]):
    kb = [lesson for lesson in lessons if lesson["num"] <= 10]
    documents = [f"{label(lesson)}\n\n{lesson['text']}" for lesson in kb]

    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = chroma.create_collection(COLLECTION)
    collection.add(
        ids=[f"lesson-{lesson['num']}" for lesson in kb],
        documents=documents,
        embeddings=embed(client, documents),
        metadatas=[{"lesson": lesson["num"], "title": lesson["title"]} for lesson in kb],
    )
    return collection
