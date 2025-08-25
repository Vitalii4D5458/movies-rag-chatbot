import argparse, json, os, pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
from typing import List, Dict, Any
import faiss
import numpy as np
from .embed import Embedder

load_dotenv()

FAISS_DIR = os.getenv("FAISS_DIR", "backend/faiss_store")
NORMALIZE = os.getenv("NORMALIZE_EMBEDDINGS", "true").lower() == "true"

def load_items(path: str, is_csv: bool):
    if is_csv:
        df = pd.read_csv(path)
        return df.to_dict(orient="records")
    else:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

def ensure_dir(d: str):
    os.makedirs(d, exist_ok=True)

def main():
    ap = argparse.ArgumentParser(description="Ingest movie data into FAISS index.")
    ap.add_argument("--input", required=True, help="Path to JSON or CSV file")
    ap.add_argument("--csv", action="store_true", help="Treat input as CSV")
    ap.add_argument("--id-field", default="id")
    ap.add_argument("--title-field", default="title")
    ap.add_argument("--plot-field", default="plot")
    ap.add_argument("--year-field", default="year")
    ap.add_argument("--genres-field", default="genres")
    args = ap.parse_args()

    items = load_items(args.input, args.csv)

    embedder = Embedder()
    ids: List[str] = []
    docs: List[str] = []
    metas: List[Dict[str, Any]] = []
    all_vecs: List[List[float]] = []

    for row in tqdm(items, desc="Preparing"):
        _id = str(row.get(args.id_field) or row.get(args.title_field))
        title = row.get(args.title_field)
        plot = (row.get(args.plot_field) or "").strip()
        year = row.get(args.year_field)
        genres = row.get(args.genres_field)
        if isinstance(genres, str):
            genres = [g.strip() for g in genres.split(",") if g.strip()]
        if not _id or not plot:
            continue
        ids.append(_id)
        docs.append(plot)
        metas.append({"title": title, "year": year, "genres": genres})
    
    BATCH = 256
    for i in tqdm(range(0, len(docs), BATCH), desc="Embedding"):
        chunk_docs = docs[i:i+BATCH]
        vecs = embedder.embed(chunk_docs)
        all_vecs.extend(vecs)

    if not all_vecs:
        raise RuntimeError("No vectors to index. Check your input.")

    x = np.array(all_vecs, dtype="float32")
    dim = x.shape[1]
    if NORMALIZE:
        faiss.normalize_L2(x)
    index = faiss.IndexFlatIP(dim)
    index.add(x)
    
    ensure_dir(FAISS_DIR)
    faiss.write_index(index, os.path.join(FAISS_DIR, "index.faiss"))
    with open(os.path.join(FAISS_DIR, "ids.json"), "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False, indent=2)
    with open(os.path.join(FAISS_DIR, "docs.json"), "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    with open(os.path.join(FAISS_DIR, "metas.json"), "w", encoding="utf-8") as f:
        json.dump(metas, f, ensure_ascii=False, indent=2)
    with open(os.path.join(FAISS_DIR, "index_info.json"), "w", encoding="utf-8") as f:
        json.dump({"dim": dim, "normalize": NORMALIZE}, f, indent=2)

    print(f"Indexed {len(ids)} items to FAISS at {FAISS_DIR} (dim={dim}, normalize={NORMALIZE})")

if __name__ == "__main__":
    main()