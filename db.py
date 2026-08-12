import sqlite3
import requests


def fetch_page(url):
    response = requests.get(url)
    return response.text


def create_db():
    connector = sqlite3.connect('jobs_db')
    cursor = connector.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    keywords TEXT,
    source TEXT
    )""")
    connector.commit()
    connector.close()
create_db()

def add_jobs(url, keywords, source):
    connector = sqlite3.connect('jobs_db')
    cursor = connector.cursor()
    cursor.execute("INSERT OR IGNORE INTO jobs (url, keywords, source) VALUES(?, ?, ?)", (url, keywords, source))
    connector.commit()
    connector.close()

add_jobs("https://www.linkedin.com/jobs/", "IT", "LinkedIn")

def list_entries():
    connector = sqlite3.connect('jobs_db')
    cursor = connector.cursor()
    print(cursor.execute("SELECT * FROM jobs").fetchall())
    connector.commit()
    connector.close()
list_entries()