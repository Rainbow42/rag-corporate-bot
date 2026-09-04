FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/data/model-cache

WORKDIR /app
RUN apt-get update \
    && apt-get install --no-install-recommends -y cron \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY scheduler/rag-index.cron /etc/cron.d/rag-index
RUN chmod 0644 /etc/cron.d/rag-index \
    && python seed_knowledge_base.py \
    && python build_index.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
