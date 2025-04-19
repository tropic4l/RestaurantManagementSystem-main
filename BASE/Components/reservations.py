import tkinter as tk
from tkinter import ttk, messagebox
from BASE.Models.reservation_model import ReservationModel

class ReservationUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Reservations")
        self.model = ReservationModel()
        self.geometry("500x400")
        self.build_ui()

    def build_ui(self):
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self, text="Customer Name").grid(row=0, column=0)

        self.table_entry = ttk.Entry(self)
        self.table_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self, text="Table Number").grid(row=1, column=0)

        self.datetime_entry = ttk.Entry(self)
        self.datetime_entry.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self, text="Date & Time").grid(row=2, column=0)

        self.guest_entry = ttk.Entry(self)
        self.guest_entry.grid(row=3, column=1, padx=10, pady=10)
        ttk.Label(self, text="Number of Guests").grid(row=3, column=0)

        ttk.Button(self, text="Save Reservation", command=self.save_reservation).grid(row=4, column=1, pady=10)

        self.res_list = tk.Listbox(self, width=60)
        self.res_list.grid(row=5, column=0, columnspan=2, padx=10)
        self.load_reservations()

    def save_reservation(self):
        name = self.name_entry.get()
        table = self.table_entry.get()
        datetime = self.datetime_entry.get()
        guests = self.guest_entry.get()

        if name and table and datetime and guests:
            self.model.save_reservation(name, table, datetime, guests)
            messagebox.showinfo("Saved", "Reservation saved!")
            self.load_reservations()
        else:
            messagebox.showerror("Error", "All fields are required.")

    def load_reservations(self):
        self.res_list.delete(0, tk.END)
        reservations = self.model.get_all_reservations()
        for res in reservations:
            self.res_list.insert(tk.END, f"{res[1]} - Table {res[2]} at {res[3]}, Guests: {res[4]}")
