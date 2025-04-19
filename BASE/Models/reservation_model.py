import sqlite3

class ReservationModel:
    def __init__(self):
        self.conn = sqlite3.connect("restaurant.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                table_number INTEGER NOT NULL,
                datetime TEXT NOT NULL,
                guest_count INTEGER NOT NULL
            );
        """)
        self.conn.commit()

    def save_reservation(self, name, table, datetime, guests):
        self.cur.execute("""
            INSERT INTO reservations (customer_name, table_number, datetime, guest_count)
            VALUES (?, ?, ?, ?)""", (name, table, datetime, guests))
        self.conn.commit()

    def get_all_reservations(self):
        self.cur.execute("SELECT * FROM reservations")
        return self.cur.fetchall()
