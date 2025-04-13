import tkinter as tk
from tkinter import ttk
from BASE.Models.staff_model import StaffModel

class StaffScheduleUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Staff Scheduling")
        self.model = StaffModel()
        self.build_ui()

    def build_ui(self):
        pass

    def save_shift(self):
        pass
