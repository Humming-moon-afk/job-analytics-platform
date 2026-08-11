import sqlite3

def init_db():
    connection = sqlite3.connect('jobs.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS job_urls(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    source TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    connection.commit()
    connection.close()

init_db()