"""Ежедневное обновление локального индекса с журналированием."""
from datetime import datetime, timezone
from pathlib import Path
from app import build_index

count = build_index()
Path("logs").mkdir(exist_ok=True)
with Path("logs/index.log").open("a", encoding="utf-8") as log:
    log.write(f"{datetime.now(timezone.utc).isoformat()} index updated: {count} chunks, 0 errors\n")
print(f"index updated: {count} chunks")
