# QuantumForge RAG bot

Локальный RAG-бот для вымышленной корпоративной базы знаний Nebula Forge.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python seed_knowledge_base.py && python build_index.py
uvicorn app:app --reload
curl -X POST localhost:8000/ask -H 'content-type: application/json' -d '{"question":"Что такое HyperRelay?"}'
```

Индекс: JSON-сериализация чанков с cosine-поиском; размер вектора — 256. В production его следует заменить на SentenceTransformers + FAISS (`faiss-cpu` уже зафиксирован в зависимостях). В документации лежит 31 файл: 30 доменных и один вредоносный тестовый.

## Безопасность

`app.py` проверяет запросы и retrieved-чанки на типовые prompt-injection-маркеры, исключает опасные фрагменты и возвращает безопасный отказ. В `logs/queries.jsonl` пишутся запросы, источники и результат.

## Автообновление

`python build_index.py` переиндексирует папку `knowledge_base/`. Пример cron: `0 6 * * * cd /app && python build_index.py >> logs/index.log 2>&1`.

Для проверки покрытия выполните `python evaluate.py`, для десяти демонстрационных диалогов — `python demo.py`.
