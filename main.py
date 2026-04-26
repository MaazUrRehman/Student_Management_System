import tkinter as tk
from tkinter import messagebox
from database.schema import create_tables
from utils.constants import COLORS, DIMENSIONS
from utils.helpers import center_window


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Management System")
        self.root.configure(bg=COLORS["background"])
        
        center_window(self.root, DIMENSIONS["window_width"], DIMENSIONS["window_height"])
        
        self.current_view = None
        self.user = None
        
        self.init_database()
        self.show_home()
        
        self.root.mainloop()
    
    def init_database(self):
        try:
            create_tables()
        except Exception as e:
            print(f"Database initialization: {e}")
    
    def show_home(self):
        self.clear_window()
        
        from views.home_view import HomeView
        self.current_view = HomeView(self.root, self.switch_view)
    
    def show_login(self):
        self.clear_window()
        
        from views.login_view import LoginView
        self.current_view = LoginView(self.root, self.switch_view)
    
    def show_register(self):
        self.clear_window()
        
        from views.register_view import RegisterView
        self.current_view = RegisterView(self.root, self.switch_view)
    
    def show_dashboard(self, user):
        self.clear_window()
        self.user = user
        
        from views.dashboard import Dashboard
        self.current_view = Dashboard(self.root, user, self.switch_view)
    
    def switch_view(self, view_name, user=None):
        if view_name == "home":
            self.show_home()
        elif view_name == "login":
            self.show_login()
        elif view_name == "register":
            self.show_register()
        elif view_name == "dashboard":
            self.show_dashboard(user)
    
    def clear_window(self):
        if self.current_view:
            self.current_view.destroy()
        
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    App()