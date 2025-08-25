import os
from .embed import Embedder
from .faiss_store import FaissStore
from openai import OpenAI

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