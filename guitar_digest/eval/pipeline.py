"""Grade the Ask RAG against the golden set.

Each question is answered live by ask(), then scored two ways: an LLM judge
compares the answer to the golden reference, and a string match checks it cited
the right lesson.

    uv run python -m guitar_digest.eval            # full run, writes the report
    uv run python -m guitar_digest.eval --limit 2  # quick check, no write
"""

import argparse
import json

from dotenv import load_dotenv
from openai import OpenAI

from ..ask import ask
from ..ingest.config import ROOT
from .config import GOLDEN_PATH, REPORT_PATH
from .judge import judge
from .models import GoldenItem, Result
from .report import pct, render_report


def load_eval_set() -> list[GoldenItem]:
    return [GoldenItem(**item) for item in json.loads(GOLDEN_PATH.read_text())]


def run_eval(items: list[GoldenItem]) -> list[Result]:
    client = OpenAI()
    results: list[Result] = []
    for i, item in enumerate(items, 1):
        live = ask(item.question)
        verdict = judge(client, item, live)
        match = live.source.strip() == item.expected_source.strip()
        results.append(
            Result(
                question=item.question,
                expected_answer=item.expected_answer,
                live_answer=live.answer,
                expected_source=item.expected_source,
                live_source=live.source,
                source_match=match,
                passed=verdict.passed,
                reason=verdict.reason,
            )
        )
        src = "✓" if match else f"✗ (live: {live.source})"
        print(
            f"\n{'=' * 78}\n"
            f"[{i}/{len(items)}]  {'PASS ✅' if verdict.passed else 'FAIL ❌'}   "
            f"source {src}\n"
            f"Q         {item.question}\n"
            f"Reference {item.expected_answer}\n"
            f"Live      {live.answer}\n"
            f"Source    live={live.source!r} | expected={item.expected_source!r}\n"
            f"Judge     {verdict.reason}"
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the Ask RAG.")
    parser.add_argument(
        "--limit", type=int, default=None, help="only run the first N questions"
    )
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")

    items = load_eval_set()
    if args.limit:
        items = items[: args.limit]

    results = run_eval(items)
    report = render_report(results)

    if args.limit:
        print("\n--- report preview (not written, --limit set) ---\n")
        print(report)
    else:
        REPORT_PATH.write_text(report)
        passed = sum(r.passed for r in results)
        print(f"\nWrote {REPORT_PATH.name}: {pct(passed, len(results))} correct")
