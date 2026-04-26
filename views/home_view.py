

# home_view.py - Fixed version
import tkinter as tk
from utils.constants import COLORS, FONTS


class HomeView:
    def __init__(self, root, switch_callback):
        self.root = root
        self.switch_callback = switch_callback
        self.frame = None
        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root, bg=COLORS["background"])
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Hero Section with Gradient Effect
        hero_frame = tk.Frame(self.frame, bg=COLORS["primary"])
        hero_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center content
        center_frame = tk.Frame(hero_frame, bg=COLORS["primary"])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Main Card
        main_card = tk.Frame(center_frame, bg=COLORS["card"], 
                            highlightbackground=COLORS["border"],
                            highlightthickness=1, padx=50, pady=40)
        main_card.pack()
        
        # App Icon/Logo
        icon_label = tk.Label(main_card, text="📚", font=(FONT_FAMILY, 64), 
                             bg=COLORS["card"], fg=COLORS["primary"])
        icon_label.pack(pady=(0, 20))
        
        # Title
        title_label = tk.Label(
            main_card,
            text="Student Management System",
            font=FONTS["title"],
            bg=COLORS["card"],
            fg=COLORS["text_primary"]
        )
        title_label.pack(pady=(0, 12))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_card,
            text="A comprehensive platform for managing students, fees, payments, and reports.",
            font=FONTS["normal"],
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
            wraplength=500,
            justify=tk.CENTER
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Features Grid
        features_frame = tk.Frame(main_card, bg=COLORS["card"])
        features_frame.pack(pady=(0, 30))
        
        features = [
            ("👨‍🎓", "Student Management"),
            ("💰", "Fee Tracking"),
            ("📊", "Financial Reports"),
            ("👥", "Staff Management")
        ]
        
        for i, (icon, text) in enumerate(features):
            feature = tk.Frame(features_frame, bg=COLORS["background"], padx=15, pady=10)
            feature.grid(row=i//2, column=i%2, padx=10, pady=5)
            
            tk.Label(feature, text=icon, font=(FONT_FAMILY, 24), 
                    bg=COLORS["background"]).pack()
            tk.Label(feature, text=text, font=FONTS["small"], 
                    bg=COLORS["background"], fg=COLORS["text_secondary"]).pack()
        
        # Login Button
        login_btn = self.create_button(main_card, "Get Started →", self.on_login_click, "primary")
        login_btn.pack(pady=(0, 10))
        
        # Footer
        footer = tk.Label(main_card, text="Secure access for administrators, accountants, staff, and students",
                         font=FONTS["small"], bg=COLORS["card"], fg=COLORS["text_muted"])
        footer.pack()

    def create_button(self, parent, text, command, variant="primary"):
        """Create a styled button"""
        color_map = {
            "primary": (COLORS["primary"], COLORS["primary_dark"]),
            "secondary": (COLORS["secondary"], COLORS["primary"]),
            "outline": (COLORS["card"], COLORS["primary"])
        }
        
        bg_color, hover_color = color_map.get(variant, color_map["primary"])
        fg_color = COLORS["text_primary"] if variant == "outline" else COLORS["text_light"]
        
        button = tk.Button(parent, text=text, command=command, font=FONTS["button"],
                          bg=bg_color, fg=fg_color,
                          activebackground=hover_color, activeforeground=COLORS["text_light"],
                          relief="flat", bd=0, cursor="hand2", padx=30, pady=12)
        
        if variant == "outline":
            button.configure(bg=COLORS["card"], fg=COLORS["primary"],
                           highlightbackground=COLORS["primary"], highlightthickness=2)
        
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

    def on_login_click(self):
        self.switch_callback("login")

    def destroy(self):
        if self.frame:
            self.frame.destroy()


# Add FONT_FAMILY to the global namespace for other views
try:
    from utils.constants import FONT_FAMILY
except ImportError:
    # Fallback if not defined in constants
    FONT_FAMILY = "Arial"