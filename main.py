import os
import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from core import ask

app = FastAPI(title="rag-qa", version="0.1.0")

class ChatRequest(BaseModel):
    q: str

class ChatResponse(BaseModel):
    a: str
    retrieved: list[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {"name": "rag-qa", "version": "1.0", "stage": "scaffold"}

@app.post("/ask", response_model=ChatResponse)
def ask_questions(req:ChatRequest):
    if not req.q or not req.q.strip():
        raise HTTPException(status_code=422, detail="q 不能为空")

    answer,retrieved = ask(req.q)

    return ChatResponse(a = answer, retrieved=retrieved)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )