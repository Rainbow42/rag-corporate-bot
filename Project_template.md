# Project work 7 — QuantumForge RAG

## 1. Модели и инфраструктура
| Вариант | Плюсы | Минусы | Решение |
|---|---|---|---|
| Локальная LLM + SentenceTransformers + FAISS | Данные остаются локально, низкая цена | Нужны CPU/GPU и эксплуатация | Подходит для закрытых данных |
| OpenAI/YandexGPT + облачные embeddings | Высокое качество, быстрый запуск | Стоимость и риск передачи данных | Подходит для non-sensitive MVP |
| Hybrid: локальный retrieval + API LLM | Баланс качества и приватности | Две зоны эксплуатации | **Рекомендован для QuantumForge** |

Рекомендованный сервер для MVP: 4 vCPU, 16 GB RAM; GPU не требуется для малого индекса. Для роста — 8 vCPU, 32 GB RAM и GPU 16 GB для локальной LLM. FAISS выбран для простого локального MVP; ChromaDB удобнее при необходимости metadata-фильтров и сервиса.

## 2. База знаний
`knowledge_base/` создаётся `seed_knowledge_base.py`: 30 оригинальных документов Nebula Forge и безопасностный fixture. `terms_map.json` фиксирует терминологию. Это синтетический мир, поэтому модель не может ответить по предобученным данным.

## 3–4. Индекс и RAG
`build_index.py` создаёт индекс; `app.py` принимает вопрос, ищет чанки, строит ответ с источниками и ведёт лог. В production prompt включает few-shot примеры и скрытое reasoning; API возвращает краткий проверяемый ответ, а не внутренние рассуждения.

## 5. Демонстрация и защита
Проверить `HyperRelay`, `VoidCore`, `Asterion`; неизвестный термин и вопрос про `swordfish` должны вернуть отказ. Защита: pre-filter запроса, фильтрация retrieved-чанков, запрет следовать инструкциям из документов.

## 6. Обновление
`build_index.py` запускается ежедневно cron; лог перенаправляется в `logs/index.log`. Поток: docs → chunking → embeddings → index → log.

## 7. Оценка
Golden set: вопросы к Asterion, VoidCore, HyperRelay, Synth Flux, Orbis Guard и неизвестные `Ghost Harbor`, `swordfish`, `Old Empire`. Лог `queries.jsonl` содержит запрос, ответ и источники; покрытие оценивается по доле полезных ответов и корректных отказов.

## Доказательства запуска
`demo.py` создаёт десять диалогов в `docs/demo_results.md`; `evaluate.py` сохраняет результат golden set в `logs/evaluation.json`. Расписание воспроизводимо через `scheduler/crontab.example`. FAISS-индекс создаётся как `data/index/faiss.index` при наличии `faiss-cpu`.
