#ingest.py

import argparse
import pandas as pd
import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np


def build_index(csv_path, index_path, meta_path):
    # читаємо CSV з урахуванням твого формату
    df = pd.read_csv(csv_path)

    # формуємо текстовий опис (щоб embeddings були інформативніші)
    df["text"] = (
        df["Series_Title"].astype(str)
        + " (" + df["Released_Year"].astype(str) + ")"
        + ". Genres: " + df["Genre"].astype(str)
        + ". Plot: " + df["Overview"].astype(str)
    )

    # створюємо embeddings
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)

    # будуємо FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype="float32"))

    faiss.write_index(index, index_path)

    # зберігаємо метадані (щоб потім повертати повну інфу про фільм)
    metadata = df.to_dict(orient="records")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"Index saved to {index_path}, metadata saved to {meta_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--index_path", required=True)
    parser.add_argument("--meta_path", required=True)
    args = parser.parse_args()

    build_index(args.csv, args.index_path, args.meta_path)
