class ReservationModel:
    def __init__(self, db=None):
        self.db = db or self.connect_to_db()

    def connect_to_db(self):
        import sqlite3
        return sqlite3.connect("restaurant.db")

    def add_reservation(self, customer_name, table_no, datetime, guests):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO reservations (customer_name, table_no, datetime, guests) VALUES (?, ?, ?, ?)",
            (customer_name, table_no, datetime, guests))
        self.db.commit()
