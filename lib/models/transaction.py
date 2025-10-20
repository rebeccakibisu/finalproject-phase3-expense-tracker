# lib/models/transaction.py
# Represents individual financial transactions.
# Includes both actual and budgeted amounts, and auto-calculates variance.

from lib.database import CURSOR, CONN

class Transaction:
    def __init__(self, user_id, category_id, amount, budgeted_amount, date, id=None):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.budgeted_amount = budgeted_amount
        self.variance = budgeted_amount - amount  # Positive = under budget, Negative = overspent
        self.date = date

    def save(self):
        """Save transaction record including variance."""
        CURSOR.execute(
            "INSERT INTO transactions (user_id, category_id, amount, budgeted_amount, variance, date) VALUES (?, ?, ?, ?, ?, ?)",
            (self.user_id, self.category_id, self.amount, self.budgeted_amount, self.variance, self.date)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        """Fetch all transactions joined with user and category details."""
        rows = CURSOR.execute('''
            SELECT t.id, u.name, c.name, t.amount, t.budgeted_amount, t.variance, t.date
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            JOIN categories c ON t.category_id = c.id
        ''').fetchall()
        return rows

    @classmethod
    def delete(cls, transaction_id):
        """Delete a transaction by ID."""
        CURSOR.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        CONN.commit()
