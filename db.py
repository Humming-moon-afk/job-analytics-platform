import sqlite3
import requests
from bs4 import BeautifulSoup

def parse_jobs(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.find_all('a')

def fetch_page(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text


def create_db():
    connector = sqlite3.connect('jobs.db')
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
    connector = sqlite3.connect('jobs.db')
    cursor = connector.cursor()
    cursor.execute("INSERT OR IGNORE INTO jobs (url, keywords, source) VALUES(?, ?, ?)", (url, keywords, source))
    connector.commit()
    connector.close()


def list_entries():
    connector = sqlite3.connect('jobs.db')
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
        if link != None and link in ('/jobs/view/'):
            title = tag.text.strip()
            add_jobs(link, title, "Web")


run_scraper("https://www.linkedin.com/jobs/search?keywords=Werkstudent")
list_entries()