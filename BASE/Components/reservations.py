import tkinter as tk
from tkinter import ttk
from BASE.Models.reservation_model import ReservationModel

class ReservationUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Reservations")
        self.model = ReservationModel()
        self.build_ui()

    def build_ui(self):
        pass  # GUI Layout Code Here

    def save_reservation(self):
        pass  # Connect UI to Model to Save Reservation
