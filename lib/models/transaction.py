from lib.database import CURSOR, CONN

class Transaction:
    def __init__(self, user_id, category_id, amount, date, id=None):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.date = date

    def save(self):
        CURSOR.execute(
            "INSERT INTO transactions (user_id, category_id, amount, date) VALUES (?, ?, ?, ?)",
            (self.user_id, self.category_id, self.amount, self.date)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute('''
            SELECT t.id, u.name, c.name, t.amount, t.date
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            JOIN categories c ON t.category_id = c.id
        ''').fetchall()
        return rows
