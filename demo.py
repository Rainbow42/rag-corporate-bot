from pathlib import Path

from rag_core import ROOT, create_service


if __name__ == "__main__":
    service = create_service()
    questions = [item["question"] for item in __import__("json").loads((ROOT / "golden_questions.json").read_text())]
    lines = []
    for number, question in enumerate(questions[:10], 1):
        result = service.ask(question)
        sources = ", ".join(result["sources"]) or "нет"
        lines.append(f"## {number}. {question}\n\n{result['answer']}\n\nИсточники: {sources}\n")
    Path("docs/demo_results.md").write_text("\n".join(lines), encoding="utf-8")
    print("saved docs/demo_results.md")
