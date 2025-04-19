import sqlite3

class InventoryModel:
    def __init__(self):
        self.conn = sqlite3.connect("restaurant.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                reorder_level INTEGER NOT NULL
            );
        """)
        self.conn.commit()

    def add_item(self, name, quantity, reorder_level):
        self.cur.execute("""
            INSERT INTO inventory (item_name, quantity, reorder_level)
            VALUES (?, ?, ?)""", (name, quantity, reorder_level))
        self.conn.commit()

    def get_all_items(self):
        self.cur.execute("SELECT * FROM inventory")
        return self.cur.fetchall()
