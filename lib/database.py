import sqlite3
import os

# Ensure the db folder exists
os.makedirs("db", exist_ok=True)

CONN = sqlite3.connect("db/database.db")
CURSOR = CONN.cursor()

def create_tables():
    """Create the database tables if they don't exist."""
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_id INTEGER,
            amount REAL,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    CONN.commit()
