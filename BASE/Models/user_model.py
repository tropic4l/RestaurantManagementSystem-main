import sqlite3
import bcrypt

class UserModel:
    def __init__(self):
        self.conn = sqlite3.connect("restaurant.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            );
        """)
        self.conn.commit()
        self.seed_users()

    def seed_users(self):
        sample_users = [
            ("admin", "admin123", "admin"),
            ("staff1", "waiterpass", "staff"),
            ("chef", "kitchen123", "chef"),
            ("manager", "managerpass", "manager"),
            ("customer1", "dinein123", "customer")
        ]
        self.cur.execute("SELECT COUNT(*) FROM users")
        if self.cur.fetchone()[0] == 0:
            for username, password, role in sample_users:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                self.cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
            self.conn.commit()

    def authenticate_user(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cur.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return {"id": user[0], "username": user[1], "role": user[3]}
        return None

    def get_user_role(self, username):
        self.cur.execute("SELECT role FROM users WHERE username = ?", (username,))
        res = self.cur.fetchone()
        return res[0] if res else None
