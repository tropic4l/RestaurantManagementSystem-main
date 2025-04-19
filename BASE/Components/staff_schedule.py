import tkinter as tk
from tkinter import ttk, messagebox
from BASE.Models.staff_model import StaffModel

class StaffScheduleUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Staff Scheduling")
        self.model = StaffModel()
        self.geometry("500x400")
        self.build_ui()

    def build_ui(self):
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self, text="Name").grid(row=0, column=0)

        self.role_entry = ttk.Entry(self)
        self.role_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self, text="Role").grid(row=1, column=0)

        self.shift_entry = ttk.Entry(self)
        self.shift_entry.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self, text="Shift Time").grid(row=2, column=0)

        ttk.Button(self, text="Save Shift", command=self.save_shift).grid(row=3, column=1, pady=15)

        self.staff_list = tk.Listbox(self, width=60)
        self.staff_list.grid(row=4, column=0, columnspan=2, padx=10)
        self.load_staff()

    def save_shift(self):
        name = self.name_entry.get()
        role = self.role_entry.get()
        shift = self.shift_entry.get()

        if name and role and shift:
            self.model.save_staff(name, role, shift)
            messagebox.showinfo("Saved", "Staff shift saved!")
            self.load_staff()
        else:
            messagebox.showerror("Error", "All fields are required.")

    def load_staff(self):
        self.staff_list.delete(0, tk.END)
        data = self.model.get_all_staff()
        for row in data:
            self.staff_list.insert(tk.END, f"{row[1]} ({row[2]}): {row[3]}")
