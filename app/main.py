from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import google.generativeai as genai
from PIL import Image
import base64
import io

app = FastAPI()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY environment variable")
genai.configure(api_key=GEMINI_API_KEY)

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64-encoded image

class Link(BaseModel):
    url: str
    text: str

class TAResponse(BaseModel):
    answer: str
    links: List[Link]

def decode_image(base64_str: str):
    try:
        if "," in base64_str:  # Remove data:image/... header if present
            base64_str = base64_str.split(",")[1]
        image_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(image_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")

@app.post("/api/", response_model=TAResponse)
async def answer_question(request: QuestionRequest):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Prepare content
        contents = []
        if request.image:
            image = decode_image(request.image)
            contents.append(image)
        contents.append(request.question)

        # Generate response
        response = model.generate_content(contents)
        answer = response.text

        # Dummy links (replace with your database logic)
        links = []
        if "assignment" in request.question.lower():
            links.append(Link(
                url="https://discourse.onlinedegree.iitm.ac.in/t/tds-assignment-is-not-submitting/166189/1",
                text="TDS Assignment Submission Thread"
            ))

        return TAResponse(answer=answer, links=links)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "OK"}
