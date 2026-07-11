from ..ingest.config import CHAT_MODEL, ROOT

JUDGE_MODEL = CHAT_MODEL
GOLDEN_PATH = ROOT / "golden.json"
REPORT_PATH = ROOT / "eval_report.md"

JUDGE_PROMPT = (
    "You are grading a guitar-theory Q&A system. You are given a question, a "
    "REFERENCE answer known to be correct, and the system's LIVE answer. Decide "
    "whether the live answer is factually correct and consistent with the "
    "reference. It does NOT need to match word-for-word or cover every detail; a "
    "shorter answer passes if what it says is accurate and on-topic. Fail it only "
    "if it is wrong, contradicts the reference, is off-topic, or wrongly claims "
    "the information is not in the lessons. Give a one-sentence reason."
)
