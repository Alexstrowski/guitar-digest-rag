from ..ingest.config import CHAT_MODEL
from .config import JUDGE_MODEL
from .models import Result


def pct(n: int, total: int) -> str:
    return f"{n}/{total} ({100 * n // total if total else 0}%)"


def render_report(results: list[Result]) -> str:
    total = len(results)
    passed = sum(r.passed for r in results)
    grounded = sum(r.source_match for r in results)

    lines = [
        "# RAG Evaluation Report",
        "",
        f"Live single-turn RAG (`ask()`, `{CHAT_MODEL}`) answered the "
        f"{total}-question Lesson 11 quiz. An LLM-as-judge (`{JUDGE_MODEL}`) "
        "graded each live answer against an **independent golden set** for "
        "correctness; grounding is a deterministic check that the cited lesson "
        "matches the golden set.",
        "",
        f"- **Correctness (judge): {pct(passed, total)}**",
        f"- **Grounding (source match): {pct(grounded, total)}**",
        "",
        "## Method",
        "",
        "The eval set is the PDF's own Lesson 11 quiz — 29 human-written "
        "questions. Crucially, the reference answers in `golden.json` were "
        "written from the lesson text by a *different* model (Claude) and "
        "reviewed by a human, so they are **independent of the RAG pipeline "
        "under test** — the answerer (`gpt-4.1-mini`), the reference author "
        "(Claude), and the judge are separate, which avoids the self-preference "
        "/ data-leakage bias of grading a system against its own output. "
        "Grounding is stricter than reality: it fails whenever live retrieval "
        "cites a different lesson than the golden set, even if that lesson also "
        "supports the answer.",
        "",
        "| # | Question | Judge | Source | Reason |",
        "|---|---|:---:|:---:|---|",
    ]
    for i, r in enumerate(results, 1):
        q = r.question.replace("|", "\\|")
        reason = r.reason.replace("|", "\\|")
        src = "✓" if r.source_match else f"✗ ({r.live_source} vs {r.expected_source})"
        lines.append(
            f"| {i} | {q} | {'✅' if r.passed else '❌'} | {src} | {reason} |"
        )
    return "\n".join(lines) + "\n"
