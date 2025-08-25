import os
from .embed import Embedder
from .faiss_store import FaissStore
from openai import OpenAI
from typing import List, Dict, Any

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