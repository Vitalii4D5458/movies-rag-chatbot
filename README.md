# Movies RAG Chatbot

### An interactive chatbot that helps find and briefly describe movies based on their plots, genres, and descriptions. A combination of **FastAPI + FAISS + SentenceTransformers + LLM(Gemini)** on the backend and **React + Tailwind** on the frontend.

## Features

- Ingest [imdb_top_1000.csv](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows) and build FAISS index of plot embeddings.
- Fast nearest-neighbor retrieval using FAISS.
- Generate user-friendly answers with LLM using retrieved plots as context.
- Simple FastAPI server with /ask endpoint.

---

## Technologies Used

- **Backend**

  - [FastAPI](https://fastapi.tiangolo.com/) — REST API
  - [FAISS](https://github.com/facebookresearch/faiss) — search by vector embeddings
  - [SentenceTransformers](https://www.sbert.net/) — embeddings generation
  - LLM — connects as a provider; possible options: Gemini, OpenAI, local models via Hugging Face Transformers
  - [Pandas, NumPy] — data processing

- **Frontend**
  - [React](https://react.dev/) + [Vite](https://vitejs.dev/)
  - [TailwindCSS](https://tailwindcss.com/) — stylization

---

## Project structure

```text
movies-rag-chatbot/
│
├── backend/
│ ├── data/
│ │ ├── imdb_top_1000.csv # data from IMDb
│ │ ├── faiss.index # generated FAISS index
│ │ └── meta.json # metadata for movies
│ │
│ ├── src/
│ │ ├── api.py # FastAPI server
│ │ ├── rag_pipeline.py # RAG logic + integration with LLM (Gemini)
│ │ └── ingest.py # building an index from CSV
│ │
│ └── init.py
│
├── frontend/ # React + Tailwind UI
│
├── .env # API keys, configurations
├── .gitignore
├── requirements.txt # backend dependencies
└── README.md
```

---

## Getting Started

### 1. Cloning a repository

```bash
git clone https://github.com/<your-username>/movies-rag-chatbot.git
cd movies-rag-chatbot
```

### 2️. Backend

Activate the virtual environment and install dependencies:

```bash
python -m venv venv
.\venv\Scripts\activate   # or source venv/bin/activate для MacOS/Linux
pip install -r requirements.txt
```

Create a .env file in movies-rag-chatbot/ with the following content:

```bash
GEMINI_API_KEY=your_google_gemini_api_key
```

Index construction (one-time):

```bash
cd backend
python src/ingest.py --csv data/imdb_top_1000.csv --index_path data/faiss.index --meta_path data/meta.json
```

API launch

```bash
uvicorn src.api:app --reload
```

API will be available on: http://127.0.0.1:8000/docs

### 3️. Frontend

```bash
cd frontend
npm install
npm run dev
```

The interface will be available on: http://localhost:5173

### Example ask

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"Tell me about Titanic\"}"
```
