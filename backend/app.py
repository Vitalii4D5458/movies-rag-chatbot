from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

app = FastAPI(title="Movies/Series RAG Chatbot")

class AskRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: Optional[int] = Field(default=5, ge=1, le=20)

class AskResponse(BaseModel):
    answer: str
    retrived: List[Dict[str, Any]]
    used_llm: bool

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ask", response_model=AskResponse)
async def ask(req: AskRequest): 
    return {"message":"data"}