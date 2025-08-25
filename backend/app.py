from fastapi import FastAPI, HTTPException
from .rag import RAGPipeline
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Movies/Series RAG Chatbot")


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


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


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    try:
        rag = RAGPipeline()
        result = await rag.answer(req.query, top_k=req.top_k)
        return AskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))