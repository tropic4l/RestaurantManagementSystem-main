"""
Restaurant Management System v1,
    App is made to facilitate restaurant management processes.

Developed by two students in April-May 2025
    Last upgrades: 
"""

#from mainwindow import MainWindow
from BASE.Components.auth import LoginUI
from ctypes import windll
 # import login screen
windll.shcore.SetProcessDpiAwareness(1)


if __name__ == "__main__":
    #app = MainWindow()
    #app.mainloop()
    login_app = LoginUI()
    login_app.mainloop()