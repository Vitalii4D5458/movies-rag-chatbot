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

