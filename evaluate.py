"""Проверка RAG на golden set: известные темы и безопасные отказы."""
import json
from pathlib import Path
from app import answer, build_index

build_index(); tests = json.loads(Path("golden_questions.json").read_text())
results = []
for test in tests:
    response = answer(test["question"])["answer"]
    refused = response.startswith("Я не знаю")
    ok = (test["known"] and not refused) or (not test["known"] and refused)
    results.append({**test, "ok": ok, "response": response})
Path("logs/evaluation.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(f"passed {sum(x['ok'] for x in results)}/{len(results)}")
