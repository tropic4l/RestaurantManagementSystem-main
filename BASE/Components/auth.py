import tkinter as tk
from tkinter import messagebox
from BASE.Models.user_model import UserModel
from BASE.Components.mainwindow import MainWindow

class LoginUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.model = UserModel()
        self.title("Login")
        self.geometry("300x180")
        self.resizable(False, False)
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Username:").pack(pady=(20, 5))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.authenticate).pack(pady=15)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.model.authenticate_user(username, password)

        if user:
            self.destroy()
            main_window = MainWindow(role=user["role"], username=user["username"])
            main_window.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials!")
