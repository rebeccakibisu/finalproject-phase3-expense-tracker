# lib/models/category.py
# Represents a category (e.g., Food, Rent, Utilities) and handles CRUD.

from lib.database import CURSOR, CONN

class Category:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        """Save a new category."""
        CURSOR.execute("INSERT INTO categories (name) VALUES (?)", (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        """Retrieve all categories."""
        rows = CURSOR.execute("SELECT * FROM categories").fetchall()
        return [cls(id=row[0], name=row[1]) for row in rows]

    @classmethod
    def delete(cls, category_id):
        """Delete category only if no transactions are linked."""
        transactions = CURSOR.execute(
            "SELECT id FROM transactions WHERE category_id = ?", (category_id,)
        ).fetchall()
        if transactions:
            print("Cannot delete category: transactions exist for this category.")
            return False
        CURSOR.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        CONN.commit()
        return True
