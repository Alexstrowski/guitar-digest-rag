from pydantic import BaseModel


class GoldenItem(BaseModel):
    question: str
    expected_answer: str
    expected_source: str


class Verdict(BaseModel):
    passed: bool
    reason: str


class Result(BaseModel):
    question: str
    expected_answer: str
    live_answer: str
    expected_source: str
    live_source: str
    source_match: bool
    passed: bool
    reason: str
