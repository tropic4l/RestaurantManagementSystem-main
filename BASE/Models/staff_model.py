import sqlite3

class StaffModel:
    def __init__(self):
        self.conn = sqlite3.connect("restaurant.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                shift TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def save_staff(self, name, role, shift):
        self.cur.execute("INSERT INTO staff (name, role, shift) VALUES (?, ?, ?)", (name, role, shift))
        self.conn.commit()

    def get_all_staff(self):
        self.cur.execute("SELECT * FROM staff")
        return self.cur.fetchall()
