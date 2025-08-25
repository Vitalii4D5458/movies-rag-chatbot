import os
from .embed import Embedder
from .faiss_store import FaissStore
from openai import OpenAI
from typing import List, Dict, Any, Optional

class RAGPipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.store = FaissStore()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self._chat_client = None
        if self.openai_key:
            try:
                self._chat_client = OpenAI(api_key=self.openai_key)
            except Exception:
                self._chat_client = None
    
    def _format_context(self, items: List[Dict[str, Any]]) -> str:
        lines = []
        for r in items:
            m = r["meta"] or {}
            title = m.get("title") or "Unknown"
            year = m.get("year")
            genres = m.get("genres")
            plot = r.get("plot") or ""
            head = f"- {title}" + (f" ({year})" if year else "")
            if genres:
                head += f" | Жанри: {', '.join(genres)}"
            lines.append(head + f"\n  Коротко: {plot[:600]}")
        return "\n".join(lines)
    
    async def answer(self, query: str, top_k: Optional[int] = None):
        k = top_k or int(os.getenv("TOP_K_DEFAULT", "5"))
        qvec = self.embedder.embed([query])[0]
        retrieved_raw = self.store.query(qvec, k)

        retrieved = []
        for r in retrieved_raw:
            m = r["meta"] or {}
            retrieved.append({
                "id": r["id"],
                "title": m.get("title"),
                "year": m.get("year"),
                "genres": m.get("genres"),
                "plot": r.get("plot"),
                "distance": 1.0 - r["score"]
            })

        context = self._format_context(retrieved_raw)

        if not self._chat_client:
            answer = (
                "LLM не налаштовано. Ось релевантні знайдені позиції:\n\n"
                + context + "\n\n"
                + "Увімкніть OpenAI у `.env`, щоб отримувати згенеровані відповіді."
            )
            return {"answer": answer, "retrieved": retrieved, "used_llm": False}