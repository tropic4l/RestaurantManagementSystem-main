import sqlite3

class UserModel:
    def __init__(self):
        self.conn = sqlite3.connect("restaurant.db")
        self.cur = self.conn.cursor()
        # MODIFIED: Include `role` in users table
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
        self.cur.execute("SELECT * FROM users")
        if not self.cur.fetchall():
            for user in sample_users:
                self.cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", user)
            self.conn.commit()


    def authenticate_user(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return bool(self.cur.fetchone())

    # NEW: Get user role
    def get_user_role(self, username):
        self.cur.execute("SELECT role FROM users WHERE username = ?", (username,))
        res = self.cur.fetchone()
        return res[0] if res else Non

