class InventoryModel:
    def __init__(self, db=None):
        self.db = db or self.connect_to_db()

    def connect_to_db(self):
        import sqlite3
        return sqlite3.connect("restaurant.db")

    def add_item(self, item_name, quantity, threshold, supplier):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO inventory (item_name, quantity, threshold, supplier) VALUES (?, ?, ?, ?)",
            (item_name, quantity, threshold, supplier))
        self.db.commit()
