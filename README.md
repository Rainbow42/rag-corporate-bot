# QuantumForge RAG bot

Корпоративный RAG-бот для синтетической базы знаний Nebula Forge. Учебный стенд использует multilingual SentenceTransformer, FAISS и локальную Qwen2.5 3B через Ollama. Доступны REST API и Telegram-интерфейс.

Результаты демонстрации, пять успешных ответов, пять корректных отказов, эксперимент с prompt injection и проверка обновления индекса собраны в [`docs/screenshots`](docs/screenshots/README.md). Ответы на все пункты проектной работы приведены в [`Project_template.md`](Project_template.md).

## Быстрый запуск

```bash
brew install ollama
ollama serve
```

В другом терминале скачайте модель и подготовьте окружение:

```bash
ollama pull qwen2.5:3b
cp .env.example .env
# заполните TELEGRAM_BOT_TOKEN
docker compose -f compose.yml up --build rag-api scheduler
curl -X POST http://localhost:8000/ask \
  -H 'content-type: application/json' \
  -d '{"question":"Что известно о системе HyperRelay?"}'
```

Ollama должна оставаться запущенной на компьютере. В контейнерах адрес переопределяется на `host.docker.internal`, поэтому редактировать `LLM_BASE_URL` для Docker не нужно.

Telegram запускается отдельным профилем:

```bash
docker compose -f compose.yml --profile telegram up --build telegram scheduler
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

Для Fish переменные из `.env` и Telegram-бот запускаются так:

```fish
bash -lc 'set -a; source .env; set +a; exec .venv/bin/python telegram_bot.py'
```

Используется модель `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` с 384 измерениями. Тексты режутся на чанки по 180 слов с overlap 30 слов. Метаданные и позиции сохраняются в `data/index/chunks.json`, параметры сборки — в `data/index/manifest.json`, векторы — в `data/index/faiss.index`.

## Проверка

```bash
pytest -q
python evaluate.py
python update_index.py
```

Перед `evaluate.py` запустите Ollama и скачайте модель `qwen2.5:3b`. Результат сохраняется в `logs/evaluation.json`, каждый запрос — в `logs/queries.jsonl`. Повторный `update_index.py` без изменений должен вернуть статус `unchanged`.

Контрольный прогон golden-набора на локальной модели завершён с результатом `12/12`; модульные тесты — `11 passed`.

## Настройки LLM

По умолчанию используется локальный OpenAI-совместимый endpoint Ollama:

```env
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=qwen2.5:3b
```

`LLM_API_KEY` является техническим непустым значением для OpenAI SDK, а не секретом. Платный ключ OpenAI не требуется.

## Защита

По умолчанию `PROTECTION_MODE=on`. Проверяются запрос, найденные чанки и итоговый ответ. Для локального учебного эксперимента поведение без фильтрации можно включить через `PROTECTION_MODE=off`; такой режим нельзя использовать в production.

Не коммитьте `.env`, токены и рабочие логи.
