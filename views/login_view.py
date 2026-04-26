
# login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService
from utils.constants import COLORS, FONTS


class LoginView:
    def __init__(self, root, switch_callback):
        self.root = root
        self.switch_callback = switch_callback
        self.frame = None
        self.create_ui()
    
    def create_ui(self):
        self.frame = tk.Frame(self.root, bg=COLORS["background"])
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Branding
        left_frame = tk.Frame(self.frame, bg=COLORS["primary"], width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Branding content
        branding_frame = tk.Frame(left_frame, bg=COLORS["primary"])
        branding_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(branding_frame, text="📚", font=("Segoe UI", 72), 
                bg=COLORS["primary"], fg=COLORS["text_light"]).pack(pady=(0, 20))
        tk.Label(branding_frame, text="Student Management", font=("Segoe UI", 28, "bold"), 
                bg=COLORS["primary"], fg=COLORS["text_light"]).pack()
        tk.Label(branding_frame, text="System", font=("Segoe UI", 28, "bold"), 
                bg=COLORS["primary"], fg=COLORS["text_light"]).pack()
        tk.Label(branding_frame, text="Efficient management for modern education", 
                font=FONTS["normal"], bg=COLORS["primary"], fg=COLORS["primary_light"]).pack(pady=(20, 0))
        
        # Right side - Login Form
        right_frame = tk.Frame(self.frame, bg=COLORS["background"], width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Center login form
        form_frame = tk.Frame(right_frame, bg=COLORS["background"])
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Login Card
        login_card = tk.Frame(form_frame, bg=COLORS["card"], 
                             highlightbackground=COLORS["border"],
                             highlightthickness=1, padx=40, pady=40)
        login_card.pack()
        
        # Header
        tk.Label(login_card, text="Welcome Back", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(pady=(0, 8))
        tk.Label(login_card, text="Please enter your credentials to continue", 
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(pady=(0, 30))
        
        # Username field
        tk.Label(login_card, text="Username", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, pady=(0, 5))
        self.username_entry = self.create_styled_entry(login_card)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        tk.Label(login_card, text="Password", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = self.create_styled_entry(login_card, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Error label
        self.error_label = tk.Label(login_card, text="", font=FONTS["small"], 
                                   bg=COLORS["card"], fg=COLORS["danger"])
        self.error_label.pack(pady=5)
        
        # Login button
        login_btn = self.create_button(login_card, "Login", self.on_login, "primary")
        login_btn.pack(fill=tk.X, pady=(15, 10))
        
        # Back button
        back_btn = self.create_button(login_card, "Back to Home", self.on_back, "outline")
        back_btn.pack(fill=tk.X)
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self.on_login())
        self.password_entry.bind("<Return>", lambda e: self.on_login())
    
    def create_styled_entry(self, parent, show=None):
        """Create a styled entry widget"""
        entry = tk.Entry(parent, font=FONTS["normal"], relief="flat", show=show,
                        bg=COLORS["background"], fg=COLORS["text_primary"],
                        highlightthickness=1, highlightcolor=COLORS["primary"],
                        highlightbackground=COLORS["border"])
        return entry
    
    def create_button(self, parent, text, command, variant="primary"):
        """Create a styled button"""
        color_map = {
            "primary": (COLORS["primary"], COLORS["primary_dark"]),
            "outline": (COLORS["card"], COLORS["primary"])
        }
        
        bg_color, hover_color = color_map.get(variant, color_map["primary"])
        fg_color = COLORS["text_primary"] if variant == "outline" else COLORS["text_light"]
        
        button = tk.Button(parent, text=text, command=command, font=FONTS["button"],
                          bg=bg_color, fg=fg_color,
                          activebackground=hover_color, activeforeground=COLORS["text_light"],
                          relief="flat", bd=0, cursor="hand2", padx=20, pady=10)
        
        if variant == "outline":
            button.configure(bg=COLORS["card"], fg=COLORS["primary"],
                           highlightbackground=COLORS["primary"], highlightthickness=1)
        
        button.bind("<Enter>", lambda e: self.on_button_hover(button, hover_color, variant))
        button.bind("<Leave>", lambda e: self.on_button_leave(button, bg_color, variant))
        return button
    
    def on_button_hover(self, button, color, variant):
        if variant == "outline":
            button.configure(bg=color, fg=COLORS["text_light"])
        else:
            button.configure(bg=color)
    
    def on_button_leave(self, button, color, variant):
        if variant == "outline":
            button.configure(bg=COLORS["card"], fg=COLORS["primary"])
        else:
            button.configure(bg=color)
    
    def on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.error_label.config(text="Please enter username and password")
            return
        
        result = AuthService.login(username, password)
        
        if result["success"]:
            user = result["user"]
            self.error_label.config(text="")
            self.switch_callback("dashboard", user)
        else:
            self.error_label.config(text=result.get("message", "Invalid credentials"))
    
    def on_back(self):
        self.switch_callback("home")
    
    def destroy(self):
        if self.frame:
            self.frame.destroy()