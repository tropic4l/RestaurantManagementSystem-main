class StaffModel:
    def __init__(self, db=None):
        self.db = db or self.connect_to_db()

    def connect_to_db(self):
        import sqlite3
        return sqlite3.connect("restaurant.db")

    def add_shift(self, staff_id, name, role, shift_start, shift_end):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO staff (staff_id, name, role, shift_start, shift_end) VALUES (?, ?, ?, ?, ?)",
            (staff_id, name, role, shift_start, shift_end))
        self.db.commit()
