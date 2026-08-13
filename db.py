import sqlite3
import requests
from bs4 import BeautifulSoup

def parse_jobs(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.find_all('a')

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

def add_jobs(url, keywords, source):
    connector = sqlite3.connect('jobs_db')
    cursor = connector.cursor()
    cursor.execute("INSERT OR IGNORE INTO jobs (url, keywords, source) VALUES(?, ?, ?)", (url, keywords, source))
    connector.commit()
    connector.close()


def list_entries():
    connector = sqlite3.connect('jobs_db')
    cursor = connector.cursor()
    print(cursor.execute("SELECT * FROM jobs").fetchall())
    connector.commit()
    connector.close()


def run_scraper(url):
    create_db()
    result = fetch_page(url)
    tags = parse_jobs(result)
    for tag in tags:
        link = tag.get('href')
        if link:
            title = tag.text
            add_jobs(link, title, "Web")


run_scraper("https://python.org")
list_entries()