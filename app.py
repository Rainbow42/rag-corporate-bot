from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from rag_core import RAGService, create_service, render_demo

app = FastAPI(title="QuantumForge RAG", version="2.0")


class Query(BaseModel):
    question: str = Field(min_length=2, max_length=2000)


@lru_cache(maxsize=1)
def service() -> RAGService:
    return create_service()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(query: Query) -> dict[str, object]:
    try:
        return service().ask(query.question)
    except Exception as error:
        raise HTTPException(status_code=503, detail="RAG service is temporarily unavailable") from error


@app.get("/demo", response_class=HTMLResponse)
def demo(question: str) -> str:
    if not 2 <= len(question) <= 2000:
        raise HTTPException(status_code=422, detail="Question length must be between 2 and 2000 characters")
    return render_demo(service().ask(question))
