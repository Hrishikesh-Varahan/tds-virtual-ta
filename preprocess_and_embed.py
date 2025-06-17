import os
import json
import glob
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import sqlite3

# Paths
DISCOURSE_JSON = "TDS-Project1-Data/discourse_posts.json"
COURSE_MD_DIR = "TDS-Project1-Data/tds_pages_md"
DB_PATH = "virtualta.db"

# 1. Load Discourse posts
with open(DISCOURSE_JSON, "r", encoding="utf-8") as f:
    discourse_posts = json.load(f)

# 2. Load course markdown files
course_chunks = []
for mdfile in glob.glob(os.path.join(COURSE_MD_DIR, "*.md")):
    with open(mdfile, "r", encoding="utf-8") as f:
        content = f.read()
        # Simple chunking by paragraphs
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        for p in paragraphs:
            course_chunks.append({"content": p, "source": mdfile})

# 3. Chunk Discourse posts (by post)
discourse_chunks = []
for post in discourse_posts:
    if post.get("cooked"):
        text = post["cooked"]
        url = post.get("url", "")
        discourse_chunks.append({"content": text, "source": url})

# 4. Combine all chunks
all_chunks = course_chunks + discourse_chunks

# 5. Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = []
for chunk in all_chunks:
    emb = model.encode(chunk["content"])
    embeddings.append({"embedding": emb, "content": chunk["content"], "source": chunk["source"]})

# 6. Save to SQLite DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY, content TEXT, source TEXT, embedding BLOB)")
for entry in embeddings:
    c.execute("INSERT INTO chunks (content, source, embedding) VALUES (?, ?, ?)",
              (entry["content"], str(entry["source"]), pickle.dumps(entry["embedding"])))
conn.commit()
conn.close()

print("Preprocessing and embedding complete!")
