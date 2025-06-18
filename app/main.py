from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
import os
import sqlite3
import json

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

class Link(BaseModel):
    url: str
    text: str

class TAResponse(BaseModel):
    answer: str
    links: List[Link]

def get_relevant_links(question: str, top_k: int = 2):
    db_path = "data/tds_content.db"
    if not os.path.exists(db_path):
        return []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Simple keyword search in topic_title/content
    cursor.execute(
        "SELECT url, topic_title FROM discourse_posts WHERE content LIKE ? OR topic_title LIKE ? LIMIT ?",
        (f"%{question}%", f"%{question}%", top_k)
    )
    results = cursor.fetchall()
    conn.close()
    return [Link(url=row[0], text=row[1]) for row in results]

@app.post("/api/", response_model=TAResponse)
async def answer_question(request: QuestionRequest):
    try:
        # Build the multimodal message content for OpenAI
        content = [
            {"type": "text", "text": f"You are a TA for IITM's Tools in Data Science. Question: {request.question}"}
        ]
        if request.image:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{request.image}",
                    "detail": "auto"
                }
            })

        response = client.chat.completions.create(
            model="gpt-4o",  # Use gpt-4o for multimodal support
            messages=[{"role": "user", "content": content}],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content

        links = get_relevant_links(request.question)
        return {"answer": answer, "links": [link.dict() for link in links]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
