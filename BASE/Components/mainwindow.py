import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from sqlite3 import Error

from BASE.Components.printorders import PrintOrders
from BASE.Components.configwindow import ConfigWindow
from BASE.Components.kitchenwindow import KitchenWindow
from BASE.Components.createorders import CreateOrders
from BASE.Components.aboutwindow import AboutWindow
from BASE.Components.database import Database
from BASE.Components.reservations import ReservationUI
from BASE.Components.inventory import InventoryUI
from BASE.Components.staff_schedule import StaffScheduleUI


class MainWindow(tk.Tk):
    def __init__(self, role="guest", username="guest"):
        super().__init__()
        self.role = role
        self.username = username

        self.win_width = 590
        self.win_height = 750
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width / 2 - self.win_width / 2)
        self.center_y = int(screen_height / 2 - self.win_height / 2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)
        self.title(f'RMS - Logged in as: {self.username} ({self.role})')

        self.m_frame = ttk.Frame(self, width=600, height=400)
        self.m_frame.grid(row=0, column=0, sticky=tk.NSEW)

        icon_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'assets', 'icon_m.png')
        self.icon_image = Image.open(icon_path)
        self.python_image = ImageTk.PhotoImage(self.icon_image)
        self.iconphoto(True, self.python_image)

        # Permission flags
        can_order = self.role in ["admin", "staff", "customer"]
        can_kitchen = self.role in ["admin", "chef"]
        can_print = self.role in ["admin", "staff", "chef"]
        can_manage = self.role in ["admin", "manager"]

        # Menus
        self.menubar = tk.Menu(self.m_frame)

        self.filebar = tk.Menu(self.menubar, tearoff=0)
        self.filebar.add_cascade(label="Print Receipts", command=self.print_win, state=tk.NORMAL if can_print else tk.DISABLED)
        self.filebar.add_cascade(label="Kitchen", command=self.kitchen_win, state=tk.NORMAL if can_kitchen else tk.DISABLED)
        self.filebar.add_cascade(label="Create Orders", command=self.customer_win, state=tk.NORMAL if can_order else tk.DISABLED)
        self.filebar.add_cascade(label="Configure Facility/Menu", command=self.config_window, state=tk.NORMAL if self.role == "admin" else tk.DISABLED)
        self.filebar.add_separator()
        self.filebar.add_cascade(label="Logout", command=self.logout)
        self.filebar.add_cascade(label="Exit", command=self.destroy)
        self.menubar.add_cascade(label="File", menu=self.filebar)


        if can_manage:
            self.managebar = tk.Menu(self.menubar, tearoff=0)
            self.managebar.add_command(label="Reservations", command=self.open_reservations)
            self.managebar.add_command(label="Inventory", command=self.open_inventory)
            self.managebar.add_command(label="Staff Scheduling", command=self.open_staff_schedule)
            self.menubar.add_cascade(label="Manage", menu=self.managebar)
            self.managebar.add_command(label="Sales Reports", command=self.open_reports)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=self.about_win)
        self.menubar.add_cascade(label="About", menu=self.helpmenu)

        self.config(menu=self.menubar)

        # Image/banner
        self.img = Image.open(os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'assets', 'main_win_ph.png'))
        self.img = self.img.resize((250, 250), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = tk.Label(
            self.m_frame,
            image=self.img,
            text="Restaurant Management System",
            compound='top',
            font=("Helvetica Bold", 20)
        )
        self.panel.image = self.img
        self.panel.grid(row=0, column=0, sticky=tk.NSEW, padx=90, pady=20)

        self.vers = tk.Label(self.m_frame, text="v0.1.2, N.A", font=("Helvetica", 8))
        self.vers.grid(row=1, column=0, sticky=tk.SW, padx=10)

        # DASHBOARD AREA
        self.dashboard_frame = ttk.LabelFrame(self.m_frame, text="Dashboard")
        self.dashboard_frame.grid(row=2, column=0, padx=20, pady=10, sticky=tk.NSEW)
        self.build_dashboard()

        self.check_databases()

    def build_dashboard(self):
        ttk.Label(
            self.dashboard_frame,
            text=f"Welcome, {self.username}!",
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.dashboard_frame, text=f"Your Role: {self.role.title()}").grid(row=1, column=0, sticky=tk.W)

        # Permissions Overview
        perm_text = "Permissions:\n"
        if self.role in ["admin", "staff", "customer"]:
            perm_text += "- Can create orders\n"
        if self.role in ["admin", "chef"]:
            perm_text += "- Can access kitchen view\n"
        if self.role in ["admin", "staff", "chef"]:
            perm_text += "- Can print receipts\n"
        if self.role in ["admin", "manager"]:
            perm_text += "- Can manage reservations/staff/inventory\n"

        ttk.Label(self.dashboard_frame, text=perm_text, justify="left").grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)

        # Quick Action Buttons
        ttk.Label(self.dashboard_frame, text="Quick Actions:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))

        row = 4
        if self.role in ["admin", "staff", "customer"]:
            ttk.Button(self.dashboard_frame, text="Create Order", command=self.customer_win).grid(row=row, column=0, pady=5, sticky=tk.W)
            row += 1
        if self.role in ["admin", "chef"]:
            ttk.Button(self.dashboard_frame, text="Open Kitchen", command=self.kitchen_win).grid(row=row, column=0, pady=5, sticky=tk.W)
            row += 1
        if self.role in ["admin", "manager"]:
            ttk.Button(self.dashboard_frame, text="Manage Reservations", command=self.open_reservations).grid(row=row, column=0, pady=5, sticky=tk.W)
            ttk.Button(self.dashboard_frame, text="Manage Staff", command=self.open_staff_schedule).grid(row=row, column=1, pady=5, sticky=tk.W)
            row += 1

        ttk.Button(self.dashboard_frame, text="Toggle Theme", command=self.toggle_theme).grid(row=row, column=1, pady=5, sticky=tk.E)

    def toggle_theme(self):
        style = ttk.Style()
        current = style.theme_use()
        # Switch between 'default' and 'clam'
        style.theme_use("clam" if current == "default" else "default")


    def check_databases(self):
        try:
            self.fac_db = Database("restaurant.db")
            load_query = """SELECT * FROM menu_config"""
            res = self.fac_db.read_val(load_query)
            customer_state = tk.NORMAL if res else tk.DISABLED
            self.filebar.entryconfig(2, state=customer_state)

            load_query1 = """SELECT * FROM orders"""
            res1 = self.fac_db.read_val(load_query1)
            kitchen_state = tk.NORMAL if res1 and self.role in ["admin", "chef"] else tk.DISABLED
            self.filebar.entryconfig(1, state=kitchen_state)

            load_query2 = """SELECT * FROM cooked_orders"""
            res2 = self.fac_db.read_val(load_query2)
            print_order_state = tk.NORMAL if res2 and self.role in ["admin", "staff", "chef"] else tk.DISABLED
            self.filebar.entryconfig(0, state=print_order_state)
        except Error as e:
            print(e)

    def config_window(self):
        config_window = ConfigWindow(self, self.check_databases)
        config_window.grab_set()

    def kitchen_win(self):
        kitchen_win = KitchenWindow(self, self.check_databases)
        kitchen_win.grab_set()

    def customer_win(self):
        customer_win = CreateOrders(self, self.check_databases)
        customer_win.grab_set()

    def about_win(self):
        about_win = AboutWindow(self)
        about_win.grab_set()

    def print_win(self):
        print_win = PrintOrders(self)
        print_win.grab_set()

    def open_reservations(self):
        res_win = ReservationUI(self)
        res_win.grab_set()

    def open_inventory(self):
        inv_win = InventoryUI(self)
        inv_win.grab_set()

    def open_staff_schedule(self):
        staff_win = StaffScheduleUI(self)
        staff_win.grab_set()

    def open_reports(self):
        from BASE.Components.reports import ReportWindow
        win = ReportWindow(self)
        win.grab_set()

    def logout(self):
        self.destroy()
        from BASE.Components.auth import LoginUI
        login_app = LoginUI()
        login_app.mainloop()
