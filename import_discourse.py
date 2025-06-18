import json, sqlite3, os

JSON_PATH = 'TDS-Project1-Data/discourse_posts.json'
DB_PATH = 'data/tds_content.db'

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    posts = json.load(f)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for post in posts:
    cursor.execute(
        '''INSERT OR IGNORE INTO discourse_posts (
            topic_id, topic_title, category_id, tags, post_id, post_number, author,
            created_at, updated_at, reply_to_post_number, is_reply, reply_count,
            like_count, is_accepted_answer, mentioned_users, url, content
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            post.get('topic_id'),
            post.get('topic_title'),
            post.get('category_id'),
            json.dumps(post.get('tags', [])),  # store as JSON string
            post.get('post_id'),
            post.get('post_number'),
            post.get('author'),
            post.get('created_at'),
            post.get('updated_at'),
            post.get('reply_to_post_number'),
            int(post.get('is_reply', False)),
            post.get('reply_count'),
            post.get('like_count'),
            int(post.get('is_accepted_answer', False)),
            json.dumps(post.get('mentioned_users', [])),  # store as JSON string
            post.get('url'),
            post.get('content')
        )
    )

conn.commit()
conn.close()
print("Discourse posts imported successfully!")
