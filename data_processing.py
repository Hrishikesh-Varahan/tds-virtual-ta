# Updated data_processing.py
import json
import sqlite3
from bs4 import BeautifulSoup

def html_to_md(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Add custom parsing rules for TDS content
    return soup.get_text(separator='\n', strip=True)

def process_scraped_data():
    with open('discourse_posts.json') as f:
        posts = json.load(f)
    
    conn = sqlite3.connect('data/tds_content.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge_base
                 (id INTEGER PRIMARY KEY, 
                  content TEXT, 
                  metadata TEXT, 
                  embeddings BLOB)''')
    
    for post in posts:
        clean_content = html_to_md(post['content'])
        metadata = json.dumps({
            'url': post['url'],
            'author': post['author'],
            'timestamp': post['created_at']
        })
        
        c.execute('''INSERT INTO knowledge_base 
                     (content, metadata) VALUES (?,?)''',
                     (clean_content, metadata))
    
    conn.commit()
    conn.close()
