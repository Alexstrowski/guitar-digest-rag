from pydantic import BaseModel


class GroundedAnswer(BaseModel):
    answer: str
    source: str


class Card(BaseModel):
    question: str
    answer: str
    source: str
