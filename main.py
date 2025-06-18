from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

class Link(BaseModel):
    url: str
    text: str

class Response(BaseModel):
    answer: str
    links: List[Link]

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_db(query, top_k=3):
    conn = sqlite3.connect("virtualta.db")
    c = conn.cursor()
    c.execute("SELECT content, source, embedding FROM chunks")
    results = []
    query_emb = model.encode(query)
    for content, source, emb_blob in c.fetchall():
        emb = pickle.loads(emb_blob)
        sim = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
        results.append({"content": content, "source": source, "score": sim})
    conn.close()
    results.sort(key=lambda x: -x["score"])
    return results[:top_k]

@app.post("/api/", response_model=Response)
async def answer_question(request: QuestionRequest):
    try:
        results = search_db(request.question, top_k=3)
        context = "\n\n".join([r["content"] for r in results])
        answer = f"Based on the course and forum data, here's what I found:\n\n{context}"
        links = []
        for r in results:
            links.append(Link(url=str(r["source"]), text=r["content"][:80] + "..."))
        return Response(answer=answer, links=links)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Virtual TA API is running!"}
if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render sets $PORT, default to 8000 for local
    uvicorn.run("main:app", host="0.0.0.0", port=port)
