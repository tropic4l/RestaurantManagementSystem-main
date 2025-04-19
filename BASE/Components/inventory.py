import tkinter as tk
from tkinter import ttk, messagebox
from BASE.Models.inventory_model import InventoryModel

class InventoryUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inventory Management")
        self.model = InventoryModel()
        self.geometry("500x400")
        self.build_ui()

    def build_ui(self):
        ttk.Label(self, text="Item Name").grid(row=0, column=0)
        self.item_name = ttk.Entry(self)
        self.item_name.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Quantity").grid(row=1, column=0)
        self.item_qty = ttk.Entry(self)
        self.item_qty.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self, text="Reorder Level").grid(row=2, column=0)
        self.reorder_lvl = ttk.Entry(self)
        self.reorder_lvl.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self, text="Add Item", command=self.add_inventory_item).grid(row=3, column=1, pady=10)

        self.tree = ttk.Treeview(self, columns=("Item", "Qty", "Reorder"), show="headings")
        self.tree.heading("Item", text="Item")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Reorder", text="Reorder Level")
        self.tree.grid(row=4, column=0, columnspan=2, padx=10)

        self.load_items()

    def add_inventory_item(self):
        name = self.item_name.get()
        qty = self.item_qty.get()
        reorder = self.reorder_lvl.get()

        if name and qty.isdigit() and reorder.isdigit():
            self.model.add_item(name, int(qty), int(reorder))
            self.load_items()
            self.item_name.delete(0, tk.END)
            self.item_qty.delete(0, tk.END)
            self.reorder_lvl.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Input", "Enter valid name, quantity, and reorder level.")

    def load_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        items = self.model.get_all_items()
        for item in items:
            self.tree.insert("", "end", values=(item[1], item[2], item[3]))
