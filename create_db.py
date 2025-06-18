import os
import sqlite3
import pandas as pd

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Sample data
sample_data = [
    {"title": "GA2 Submission Deadline", "content": "The deadline for GA2 is 25th August 2024. Submit via the portal.", "url": "https://discourse.example.com/ga2"},
    {"title": "TDS Assignment FAQ", "content": "GA2 deadlines are strict. Late submissions incur penalties.", "url": "https://discourse.example.com/faq"}
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Create SQLite database and table
conn = sqlite3.connect('data/tds_content.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT NOT NULL
)
''')
cursor.execute('DELETE FROM posts')  # Clear existing data

# Insert data
for _, row in df.iterrows():
    cursor.execute('INSERT INTO posts (title, content, url) VALUES (?, ?, ?)', (row['title'], row['content'], row['url']))

conn.commit()
conn.close()
