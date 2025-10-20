# lib/database.py
# Handles database connection and table creation using SQLite3.
# A standalone database file 'database.db' is created in the project root.

import sqlite3

# Connect to a local database file (auto-created if missing)
CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

def create_tables():
    """Creates all required tables if they don't exist."""
    
    # Create Users table
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create Categories table
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create Transactions table with budget, actual, and variance
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
