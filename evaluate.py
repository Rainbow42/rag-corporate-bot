from __future__ import annotations

import json
from pathlib import Path

from rag_core import ROOT, create_service, utc_now


def evaluate() -> dict[str, object]:
    tests = json.loads((ROOT / "golden_questions.json").read_text(encoding="utf-8"))
    service = create_service()
    results = []
    for test in tests:
        response = service.ask(test["question"])
        answer = str(response["answer"])
        refused = answer.startswith("Я не знаю")
        expected_terms = test.get("expected_terms", [])
        expected_sources = test.get("expected_sources", [])
        terms_ok = all(term.lower() in answer.lower() for term in expected_terms)
        sources_ok = all(source in response["sources"] for source in expected_sources)
        answer_state_ok = refused != test["should_answer"]
        passed = answer_state_ok and terms_ok and sources_ok
        results.append({**test, "passed": passed, "response": response})
    report = {
        "evaluated_at": utc_now(),
        "passed": sum(item["passed"] for item in results),
        "total": len(results),
        "results": results,
    }
    output = ROOT / "logs" / "evaluation.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    summary = evaluate()
    print(f"passed {summary['passed']}/{summary['total']}")
