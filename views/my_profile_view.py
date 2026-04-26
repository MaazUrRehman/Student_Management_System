
# my_profile_view.py
import tkinter as tk
from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class MyProfileView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.create_ui()
    
    def create_ui(self):
        # Use parent directly - Dashboard already provides scrollable frame
        page = self.parent
        
        # Header Card
        header_card = self.create_card(page)
        header_card.pack(fill=tk.X, pady=(0, 20))
        
        # Profile icon and title
        header_inner = tk.Frame(header_card, bg=COLORS["card"])
        header_inner.pack(fill=tk.X, padx=20, pady=20)
        
        # Avatar
        avatar = tk.Canvas(header_inner, width=60, height=60, bg=COLORS["primary"], 
                          highlightthickness=0)
        avatar.pack(side=tk.LEFT, padx=(0, 15))
        avatar.create_oval(5, 5, 55, 55, fill=COLORS["primary_light"], outline="")
        avatar.create_text(30, 30, text=self.user['username'][0].upper(), 
                          font=("Inter", 24, "bold"), fill=COLORS["text_light"])
        
        # Title section
        title_section = tk.Frame(header_inner, bg=COLORS["card"])
        title_section.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(title_section, text="My Profile", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        
        role_color = COLORS["success"] if self.user["role"] == "admin" else COLORS["primary"]
        tk.Label(title_section, text=f"{self.user['role'].upper()} • {self.user['username']}", 
                font=FONTS["normal"], bg=COLORS["card"], fg=role_color).pack(anchor=tk.W)
        
        # Profile Information Card
        info_card = self.create_card(page)
        info_card.pack(fill=tk.X)
        
        tk.Label(info_card, text="📄 Personal Information", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 15))
        
        fields = self.get_profile_fields()
        
        if fields:
            # Create two-column layout for profile fields
            fields_frame = tk.Frame(info_card, bg=COLORS["card"])
            fields_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            # Configure grid
            fields_frame.grid_columnconfigure(0, weight=1)
            fields_frame.grid_columnconfigure(1, weight=2)
            
            for row_index, (label, value) in enumerate(fields):
                # Label
                tk.Label(fields_frame, text=f"{label}:", font=FONTS["normal"], 
                        bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(
                        row=row_index, column=0, padx=(0, 20), pady=10, sticky="ew")
                
                # Value with background
                value_frame = tk.Frame(fields_frame, bg=COLORS["background"], padx=10, pady=5)
                value_frame.grid(row=row_index, column=1, padx=(0, 20), pady=10, sticky="ew")
                
                tk.Label(value_frame, text=value, font=FONTS["normal"], 
                        bg=COLORS["background"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        else:
            error_frame = tk.Frame(info_card, bg=COLORS["status_overdue"], padx=20, pady=15)
            error_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
            tk.Label(error_frame, text="⚠️ No profile information found", 
                    font=FONTS["normal"], bg=COLORS["status_overdue"], fg=COLORS["danger"]).pack()
        
        # Account Information Card
        account_card = self.create_card(page)
        account_card.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(account_card, text="🔐 Account Information", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 15))
        
        account_frame = tk.Frame(account_card, bg=COLORS["card"])
        account_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        account_fields = [
            ("Username", self.user["username"]),
            ("Role", self.user["role"].capitalize()),
            ("User ID", str(self.user["id"]))
        ]
        
        for row_index, (label, value) in enumerate(account_fields):
            tk.Label(account_frame, text=f"{label}:", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(
                    row=row_index, column=0, padx=(0, 20), pady=8, sticky="w")
            
            value_frame = tk.Frame(account_frame, bg=COLORS["background"], padx=10, pady=3)
            value_frame.grid(row=row_index, column=1, padx=(0, 20), pady=8, sticky="ew")
            
            tk.Label(value_frame, text=value, font=FONTS["normal"], 
                    bg=COLORS["background"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        
        account_frame.grid_columnconfigure(1, weight=1)
    
    def create_card(self, parent):
        """Create a styled card frame"""
        card = tk.Frame(parent, bg=COLORS["card"], 
                       highlightbackground=COLORS["border"], 
                       highlightthickness=1)
        return card
    
    def get_profile_fields(self):
        """Get profile fields based on user role"""
        if self.user["role"] == "staff":
            staff = AccountService.get_staff_by_user_id(self.user["id"])
            if not staff:
                return None
            return [
                ("Full Name", staff["name"]),
                ("Father's Name", staff["father_name"] or "Not provided"),
                ("Qualification", staff["qualification"] or "Not provided"),
                ("Department", staff["department"] or "Not provided"),
                ("Designation", staff["designation"] or "Not provided"),
                ("Monthly Salary", f"${staff['salary']:,.2f}")
            ]
        
        elif self.user["role"] == "student":
            student = AccountService.get_student_by_user_id(self.user["id"])
            if not student:
                return None
            return [
                ("Full Name", student["name"]),
                ("Class", student["class_name"]),
                ("Parent/Guardian Name", student["parent_name"] or "Not provided"),
                ("Phone Number", student["phone"] or "Not provided")
            ]
        
        return None