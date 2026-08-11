import sqlite3

def init_db():
    sqlite3.connect('jobs.db')