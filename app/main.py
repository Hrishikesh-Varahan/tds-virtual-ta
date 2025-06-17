from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_BASE_URL")

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

class Link(BaseModel):
    url: str
    text: str

class TAResponse(BaseModel):
    answer: str
    links: List[Link]

def get_context(question: str) -> str:
    # Dummy context fetch (replace with your logic)
    return "Relevant course/discourse content here."

@app.post("/api/", response_model=TAResponse)
async def answer_question(request: QuestionRequest):
    try:
        context = get_context(request.question)
        prompt = f"""You are a Teaching Assistant for IITM's Tools in Data Science course.
Context from course materials and discussions:
{context}

Question: {request.question}
Answer concisely and cite sources from context."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        links = [
            Link(url="https://discourse.example.com/post1", text="Relevant discussion 1"),
            Link(url="https://discourse.example.com/post2", text="Relevant discussion 2")
        ]
        return {
            "answer": response.choices[0].message['content'],
            "links": links
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
