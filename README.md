# TDS Virtual TA

A FastAPI-based virtual teaching assistant for IITM's Tools in Data Science course.

## How to run locally

1. Install dependencies:
   pip install -r requirements.txt

2. Start the server:
   uvicorn api.main:app --reload

3. Test the API:
   curl -X POST "http://localhost:8000/api/" \
     -H "Content-Type: application/json" \
     -d '{"question": "Should I use gpt-4o-mini or gpt3.5 turbo?"}'

## Deployment

This project is ready for deployment on Vercel.
