# TDS Virtual TA

A virtual teaching assistant for IITM's Tools in Data Science course.

- Answers student questions using course and Discourse content.
- FastAPI backend.
- Includes a Discourse scraping script for bonus marks.

## API

POST /api/
{
  "question": "Your question here",
  "image": "base64string" (optional)
}

## Bonus

Run the scraper with:
python scrapers/discourse_scraper.py
