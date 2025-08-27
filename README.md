# Movies RAG Chatbot

Інтерактивний чат-бот, який допомагає знаходити та коротко описувати фільми на основі їх сюжетів, жанрів та описів. Поєднання **FastAPI + FAISS + SentenceTransformers + Gemini API** на бекенді та **React + Tailwind** на фронтенді.

---

## Використані технології

- **Backend**

  - [FastAPI](https://fastapi.tiangolo.com/) — REST API
  - [FAISS](https://github.com/facebookresearch/faiss) — пошук за векторними embeddings
  - [SentenceTransformers](https://www.sbert.net/) — генерація embeddings
  - [LLM] — підключається як провайдер; можливі варіанти: Gemini, OpenAI, локальні моделі через Hugging Face Transformers
  - [Pandas, NumPy] — обробка даних

- **Frontend**
  - [React](https://react.dev/) + [Vite](https://vitejs.dev/)
  - [TailwindCSS](https://tailwindcss.com/) — стилізація

---

## Структура проєкту

```text
movies-rag-chatbot/
│
├── backend/
│ ├── data/
│ │ ├── imdb_top_1000.csv # дані з IMDb
│ │ ├── faiss.index # згенерований FAISS індекс
│ │ └── meta.json # метадані для фільмів
│ │
│ ├── src/
│ │ ├── api.py # FastAPI сервер
│ │ ├── rag_pipeline.py # RAG-логіка + інтеграція з LLM(Gemini)
│ │ └── ingest.py # побудова індексу з CSV
│ │
│ └── init.py
│
├── frontend/ # React + Tailwind UI
│
├── .env # API ключі, конфіги
├── .gitignore
├── requirements.txt # залежності бекенду
└── README.md
```

---

## Як запустити

### 1. Клонування репозиторію

```bash
git clone https://github.com/<your-username>/movies-rag-chatbot.git
cd movies-rag-chatbot
```

### 2️. Backend

Встановлення залежностей

```bash
python -m venv venv
.\venv\Scripts\activate   # або source venv/bin/activate для MacOS/Linux
pip install -r requirements.txt
```

Змінні середовища  
Створи файл .env у backend/ з вмістом:

```bash
GEMINI_API_KEY=your_google_gemini_api_key
```

Побудова індексу (одноразово)

```bash
cd backend
python src/ingest.py --csv data/imdb_top_1000.csv --index_path data/faiss.index --meta_path data/meta.json
```

Запуск API

```bash
uvicorn src.api:app --reload
```

API буде доступне на: http://127.0.0.1:8000/docs

### 3️. Frontend

```bash
cd frontend
npm install
npm run dev
```

Інтерфейс буде доступний на: http://localhost:5173

### Приклад використання

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"Tell me about Titanic\"}"
```
