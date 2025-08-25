import os
from typing import List
import numpy as np
from openai import OpenAI

class Embedder:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        self._client = None
        if self.openai_key:
            try:
                self._client = OpenAI(api_key=self.openai_key)
            except Exception:
                self._client = None
    def embed(self, texts: List[str]) -> List[List[float]]:
        if self._client:
            resp = self._client.embeddings.create(model=self.embed_model, input=texts)
            return [d.embedding for d in resp.data]
        else:
            dim = 512
            vecs = []
            for t in texts:
                h = np.zeros(dim, dtype=np.float32)
                for w in t.lower().split():
                    h[hash(w) % dim] += 1.0
                norm = np.linalg.norm(h) or 1.0
                vecs.append((h / norm).tolist())
            return vecs

