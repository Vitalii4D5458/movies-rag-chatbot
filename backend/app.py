from fastapi import FastAPI

app = FastAPI(title="Movies/Series RAG Chatbot")

@app.get("/health")
def health():
    return {"status": "ok"}
