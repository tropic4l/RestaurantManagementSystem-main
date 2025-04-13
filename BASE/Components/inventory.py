import tkinter as tk
from tkinter import ttk
from BASE.Models.inventory_model import InventoryModel

class InventoryUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inventory Management")
        self.model = InventoryModel()
        self.build_ui()

    def build_ui(self):
        pass

    def add_inventory_item(self):
        pass
