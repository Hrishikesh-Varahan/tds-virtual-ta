# app/main.py (Updated)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db_connection():
    conn = sqlite3.connect('data/tds_content.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/query")
async def handle_query(query: dict):
    conn = get_db_connection()
    
    # Simple semantic search implementation
    results = conn.execute('''
        SELECT content, metadata 
        FROM knowledge_base 
        WHERE content LIKE ? 
        LIMIT 5
    ''', ('%'+query['text']+'%',)).fetchall()
    
    return {
        "response": [dict(row) for row in results],
        "context": query.get('image', None)
    }
