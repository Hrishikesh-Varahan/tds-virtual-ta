from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import google.generativeai as genai
from PIL import Image
import base64
import io

app = FastAPI()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=GEMINI_API_KEY)

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64-encoded PNG/JPEG

class Link(BaseModel):
    url: str
    text: str

class TAResponse(BaseModel):
    answer: str
    links: List[Link]

def decode_image(base64_str):
    try:
        # Remove data:image/...;base64, if present
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
        image_bytes = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {e}")

@app.post("/api/", response_model=TAResponse)
async def answer_question(request: QuestionRequest):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        # Prepare content
        contents = []
        if request.image:
            image = decode_image(request.image)
            contents.append(image)
        contents.append(request.question)

        # Generate response
        response = model.generate_content(contents)
        answer = response.text

        # Dummy links logic (replace with your own DB search if needed)
        links = []
        if "assignment" in request.question.lower():
            links.append(Link(url="https://example.com/assignment", text="Assignment Help"))

        return {"answer": answer, "links": [link.dict() for link in links]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Virtual TA API is live!"}
