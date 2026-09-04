"""Запускает десять демонстрационных диалогов и сохраняет текстовые доказательства."""
from pathlib import Path
from app import answer, build_index

build_index()
questions = [x["question"] for x in __import__("json").loads(Path("golden_questions.json").read_text())]
lines = []
for number, question in enumerate(questions, 1):
    result = answer(question)
    lines.append(f"## {number}. {question}\n\n{result['answer']}\n\nИсточники: {', '.join(x['source'] for x in result['sources']) or 'нет'}\n")
Path("docs/demo_results.md").write_text("\n".join(lines), encoding="utf-8")
print("saved docs/demo_results.md")
