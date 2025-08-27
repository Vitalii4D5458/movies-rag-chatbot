from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .rag_pipeline import rag_search, load_index_and_metadata, generate_short_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX_PATH = "data/faiss.index" 
META_PATH = "data/meta.json"

index, metadata = load_index_and_metadata(INDEX_PATH, META_PATH)

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    answer: str

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    try:
        relevant_docs = rag_search(req.query, index, metadata)
        short_answer = generate_short_answer(req.query, relevant_docs)
        return AskResponse(answer=short_answer)
    except Exception as e:
        return AskResponse(answer=f"Error: {str(e)}")