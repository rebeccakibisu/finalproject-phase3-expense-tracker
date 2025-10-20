from lib.database import CURSOR, CONN

class User:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        CURSOR.execute("INSERT INTO users (name) VALUES (?)", (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM users").fetchall()
        return [cls(id=row[0], name=row[1]) for row in rows]
