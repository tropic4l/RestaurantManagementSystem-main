import tkinter as tk
from tkinter import ttk
from BASE.Components.database import Database
from datetime import datetime
from collections import Counter

class ReportWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Daily Sales Report")
        self.geometry("500x500")
        self.fac_db = Database("restaurant.db")

        ttk.Label(self, text="Today's Sales Summary", font=("Helvetica", 14)).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Product", "Qty", "Total"), show="headings")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Qty", text="Total Ordered")
        self.tree.heading("Total", text="Revenue (Ft)")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_data()

    def load_data(self):
        query = """SELECT product_name, SUM(order_quantity), SUM(order_price)
                   FROM cooked_orders GROUP BY product_name"""
        data = self.fac_db.read_val(query)
        for row in data:
            self.tree.insert("", tk.END, values=row)
