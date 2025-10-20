# lib/models/user.py
# Represents a user and manages CRUD operations related to users.

from lib.database import CURSOR, CONN

class User:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        """Save a new user to the database."""
        CURSOR.execute("INSERT INTO users (name) VALUES (?)", (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        """Retrieve all users."""
        rows = CURSOR.execute("SELECT * FROM users").fetchall()
        return [cls(id=row[0], name=row[1]) for row in rows]

    @classmethod
    def delete(cls, user_id):
        """Delete a user safely (only if no transactions are linked)."""
        transactions = CURSOR.execute(
            "SELECT id FROM transactions WHERE user_id = ?", (user_id,)
        ).fetchall()
        if transactions:
            print("Cannot delete user: transactions exist for this user.")
            return False
        CURSOR.execute("DELETE FROM users WHERE id = ?", (user_id,))
        CONN.commit()
        return True
