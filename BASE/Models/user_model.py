class UserModel:
    def __init__(self, db=None):
        self.db = db or self.connect_to_db()

    def connect_to_db(self):
        import sqlite3
        return sqlite3.connect("restaurant.db")

    def check_credentials(self, username, password):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return cursor.fetchone()
