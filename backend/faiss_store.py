from typing import Optional
import os, json
import faiss

FAISS_DIR = os.getenv("FAISS_DIR", "backend/faiss_store")


class FaissStore:
    def __init__(self, directory: Optional[str] = None):
        self.dir = directory or FAISS_DIR
        self.index_path = os.path.join(self.dir, "index.faiss")
        self.ids_path = os.path.join(self.dir, "ids.json")
        self.docs_path = os.path.join(self.dir, "docs.json")
        self.metas_path = os.path.join(self.dir, "metas.json")
        self.info_path = os.path.join(self.dir, "index_info.json")
        self._index = None
        self._ids = []
        self._docs = []
        self._metas = []
        self._dim = 0
        self._load()
        
    def _load(self):
        if not (os.path.exists(self.index_path) and os.path.exists(self.ids_path) and os.path.exists(self.docs_path) and os.path.exists(self.metas_path) and os.path.exists(self.info_path)):
            raise RuntimeError(f"FAISS store not found in {self.dir}. Run ingest first.")
        self._index = faiss.read_index(self.index_path)
        with open(self.ids_path, "r", encoding="utf-8") as f:
            self._ids = json.load(f)
        with open(self.docs_path, "r", encoding="utf-8") as f:
            self._docs = json.load(f)
        with open(self.metas_path, "r", encoding="utf-8") as f:
            self._metas = json.load(f)
        with open(self.info_path, "r", encoding="utf-8") as f:
            info = json.load(f)
            self._dim = info["dim"]
            self._normalize = info.get("normalize", True)

        n = len(self._ids)
        if not (len(self._docs) == n and len(self._metas) == n):
            raise RuntimeError("FAISS store files length mismatch. Re-ingest.")
