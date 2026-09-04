# QuantumForge RAG bot

Корпоративный RAG-бот для синтетической базы знаний Nebula Forge. Production-путь использует multilingual SentenceTransformer, FAISS и OpenAI Responses API. Доступны REST API и Telegram-интерфейс.

## Быстрый запуск

```bash
cp .env.example .env
# заполните OPENAI_API_KEY и, для Telegram, TELEGRAM_BOT_TOKEN
docker compose up --build rag-api scheduler
curl -X POST http://localhost:8000/ask \
  -H 'content-type: application/json' \
  -d '{"question":"Что известно о системе HyperRelay?"}'
```

Telegram запускается отдельным профилем:

```bash
docker compose --profile telegram up --build telegram scheduler
```

## Локальная разработка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed_knowledge_base.py
python build_index.py
uvicorn app:app --reload
```

Используется модель `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` с 384 измерениями. Тексты режутся на чанки по 180 слов с overlap 30 слов. Метаданные и позиции сохраняются в `data/index/chunks.json`, параметры сборки — в `data/index/manifest.json`, векторы — в `data/index/faiss.index`.

## Проверка

```bash
pytest -q
python evaluate.py
python update_index.py
```

`evaluate.py` требует настроенный `OPENAI_API_KEY`. Результат сохраняется в `logs/evaluation.json`, каждый запрос — в `logs/queries.jsonl`. Повторный `update_index.py` без изменений должен вернуть статус `unchanged`.

## Защита

По умолчанию `PROTECTION_MODE=on`. Проверяются запрос, найденные чанки и итоговый ответ. Для локального учебного эксперимента поведение без фильтрации можно включить через `PROTECTION_MODE=off`; такой режим нельзя использовать в production.

Не коммитьте `.env`, токены и рабочие логи.
