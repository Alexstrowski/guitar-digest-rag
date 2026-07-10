from pydantic import BaseModel


class Card(BaseModel):
    question: str
    answer: str
    source: str
