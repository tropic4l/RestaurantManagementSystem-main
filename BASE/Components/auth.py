import tkinter as tk
from tkinter import messagebox
from BASE.Models.user_model import UserModel

class LoginUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.model = UserModel()
        self.title("Login")
        self.build_ui()

    def build_ui(self):
        pass

    def authenticate(self):
        pass
