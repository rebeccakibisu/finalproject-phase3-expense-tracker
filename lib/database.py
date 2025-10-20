# lib/database.py
# Handles database connection and table creation using sqlite3.
# Uses a standalone database file named 'database.db' in the project root.

import sqlite3

# Connect to a standalone database (creates automatically if it doesn’t exist)
CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

def create_tables():
    """
    Create all database tables if they don't exist.
    This ensures smooth operation on first run.
    """
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

    # Transactions now include actual, budgeted, and variance columns
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_id INTEGER,
            amount REAL,
            budgeted_amount REAL,
            variance REAL,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    CONN.commit()
