from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
import os

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

@app.post("/api/", response_model=TAResponse)
async def answer_question(request: QuestionRequest):
    try:
        prompt = f"Your prompt logic here. Question: {request.question}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content
        links = []  # Your links logic here
        return {"answer": answer, "links": links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
