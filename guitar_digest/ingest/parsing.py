import re

LESSON_RE = re.compile(r"^## Lesson (\d+) — (.+)$", re.MULTILINE)
QUESTION_RE = re.compile(r"^\s*\d+\.\s+(.*\S)\s*$", re.MULTILINE)


def parse_lessons(md: str) -> list[dict]:
    matches = list(LESSON_RE.finditer(md))
    lessons = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        lessons.append(
            {
                "num": int(m.group(1)),
                "title": m.group(2).strip(),
                "text": md[m.end():end].strip(),
            }
        )
    return lessons


def parse_quiz(lessons: list[dict]) -> list[str]:
    quiz = next(lesson for lesson in lessons if lesson["num"] == 11)
    return [m.group(1).strip() for m in QUESTION_RE.finditer(quiz["text"])]


def label(lesson: dict) -> str:
    return f"Lesson {lesson['num']} — {lesson['title']}"
