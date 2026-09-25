import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI(title="rag-qa", version="0.1.0")

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

class ChatRequest(BaseModel):
    q: str
    top_k: int = 5

class ChatResponse(BaseModel):
    a: str
    sources: list[str] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {"name": "rag-qa", "version": "0.1.0", "stage": "scaffold"}

@app.post("/chat", response_model=ChatResponse)
def chat(req:ChatRequest):
    if not req.q or not req.q.strip():
        raise HTTPException(status_code=422, detail="q 不能为空")

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[{"role": "user", "content": req.q}],
    )
    answer = response.choices[0].message.content

    return ChatResponse(a = answer, sources=[])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )