

# register_user_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.auth_model import AuthModel
from services.account_service import AccountService
from utils.constants import COLORS, FONTS
from utils.helpers import hash_password


class RegisterUserView:
    def __init__(self, parent, switch_callback, current_user=None):
        self.parent = parent
        self.switch_callback = switch_callback
        self.current_user = current_user
        self.create_ui()
    
    def create_ui(self):
        # Main scrollable container
        self.configure_tree_style()
        
        # Use parent directly - Dashboard already provides scrollable frame
        page = self.parent
        
        # Header Card
        header_card = self.create_card(page)
        header_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_card, text="👤 Register New User", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 5))
        tk.Label(header_card, text="Create new user accounts with appropriate roles",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Main Form Card
        form_card = self.create_card(page)
        form_card.pack(fill=tk.X)
        
        # Account Information Section
        account_section = tk.LabelFrame(form_card, text="Account Information", 
                                        font=FONTS["heading"], bg=COLORS["card"], 
                                        fg=COLORS["primary"], padx=20, pady=15)
        account_section.pack(fill=tk.X, padx=20, pady=(20, 15))
        
        # Username
        tk.Label(account_section, text="Username", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.username_entry = self.create_styled_entry(account_section)
        self.username_entry.grid(row=0, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        # Password
        tk.Label(account_section, text="Password", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=1, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.password_entry = self.create_styled_entry(account_section, show="*")
        self.password_entry.grid(row=1, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        # Role
        tk.Label(account_section, text="Role", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=2, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(account_section, textvariable=self.role_var,
                                 values=["admin", "accountant", "student", "staff"],
                                 width=27, state="readonly", font=FONTS["normal"])
        role_combo.grid(row=2, column=1, padx=(0, 20), pady=8, sticky="ew")
        self.role_var.trace("w", self.on_role_change)
        
        account_section.grid_columnconfigure(1, weight=1)
        
        # Student Details Section
        self.student_section = tk.LabelFrame(form_card, text="Student Details", 
                                             font=FONTS["heading"], bg=COLORS["card"], 
                                             fg=COLORS["primary"], padx=20, pady=15)
        
        # Student fields
        tk.Label(self.student_section, text="Full Name", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.name_entry = self.create_styled_entry(self.student_section)
        self.name_entry.grid(row=0, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.student_section, text="Class", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=1, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.class_entry = self.create_styled_entry(self.student_section)
        self.class_entry.grid(row=1, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.student_section, text="Parent/Guardian Name", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=2, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.parent_entry = self.create_styled_entry(self.student_section)
        self.parent_entry.grid(row=2, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.student_section, text="Phone Number", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=3, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.phone_entry = self.create_styled_entry(self.student_section)
        self.phone_entry.grid(row=3, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        self.student_section.grid_columnconfigure(1, weight=1)
        
        # Staff Details Section
        self.staff_section = tk.LabelFrame(form_card, text="Staff Details", 
                                           font=FONTS["heading"], bg=COLORS["card"], 
                                           fg=COLORS["primary"], padx=20, pady=15)
        
        # Staff fields
        tk.Label(self.staff_section, text="Full Name", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.staff_name_entry = self.create_styled_entry(self.staff_section)
        self.staff_name_entry.grid(row=0, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.staff_section, text="Father's Name", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=1, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.father_name_entry = self.create_styled_entry(self.staff_section)
        self.father_name_entry.grid(row=1, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.staff_section, text="Qualification", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=2, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.qualification_entry = self.create_styled_entry(self.staff_section)
        self.qualification_entry.grid(row=2, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.staff_section, text="Department", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=3, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.department_entry = self.create_styled_entry(self.staff_section)
        self.department_entry.grid(row=3, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.staff_section, text="Designation", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=4, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.designation_entry = self.create_styled_entry(self.staff_section)
        self.designation_entry.grid(row=4, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        tk.Label(self.staff_section, text="Salary ($)", font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=5, column=0, padx=(0, 10), pady=8, sticky=tk.W)
        self.salary_entry = self.create_styled_entry(self.staff_section)
        self.salary_entry.grid(row=5, column=1, padx=(0, 20), pady=8, sticky="ew")
        
        self.staff_section.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(form_card, bg=COLORS["card"])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.create_button(btn_frame, "Register User", self.on_register, "success").pack(side=tk.LEFT, padx=(0, 10))
        self.create_button(btn_frame, "Back to Dashboard", self.on_back, "secondary").pack(side=tk.LEFT)
        
        # Initially hide role-specific sections
        self.on_role_change()
    
    def create_styled_entry(self, parent, show=None):
        """Create a styled entry widget"""
        entry = tk.Entry(parent, font=FONTS["normal"], relief="flat", show=show,
                        bg=COLORS["background"], fg=COLORS["text_primary"],
                        highlightthickness=1, highlightcolor=COLORS["primary"],
                        highlightbackground=COLORS["border"])
        return entry
    
    def create_card(self, parent):
        """Create a styled card frame"""
        card = tk.Frame(parent, bg=COLORS["card"], 
                       highlightbackground=COLORS["border"], 
                       highlightthickness=1)
        return card
    
    def create_button(self, parent, text, command, variant="primary"):
        """Create a styled button"""
        color_map = {
            "primary": (COLORS["primary"], COLORS["primary_dark"]),
            "secondary": (COLORS["secondary"], COLORS["primary"]),
            "success": (COLORS["success"], "#059669"),
            "danger": (COLORS["danger"], "#DC2626"),
        }
        
        bg_color, hover_color = color_map.get(variant, color_map["primary"])
        
        button = tk.Button(parent, text=text, command=command, font=FONTS["button"],
                          bg=bg_color, fg=COLORS["text_light"],
                          activebackground=hover_color, activeforeground=COLORS["text_light"],
                          relief="flat", bd=0, cursor="hand2", padx=20, pady=10)
        
        button.bind("<Enter>", lambda e: button.configure(bg=hover_color))
        button.bind("<Leave>", lambda e: button.configure(bg=bg_color))
        return button
    
    def on_role_change(self, *args):
        """Toggle role-specific fields"""
        role = self.role_var.get()
        
        # Hide all sections first
        self.student_section.pack_forget()
        self.staff_section.pack_forget()
        
        if role == "student":
            self.student_section.pack(fill=tk.X, padx=20, pady=(0, 15))
        elif role == "staff":
            self.staff_section.pack(fill=tk.X, padx=20, pady=(0, 15))
    
    def on_register(self):
        """Register new user"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return
        
        try:
            user_id = AuthModel.add_user(username, hash_password(password), role)
            
            if not user_id:
                messagebox.showerror("Error", "Username already exists")
                return
            
            if role == "student":
                name = self.name_entry.get().strip()
                class_name = self.class_entry.get().strip()
                parent_name = self.parent_entry.get().strip()
                phone = self.phone_entry.get().strip()
                
                if not name or not class_name:
                    messagebox.showerror("Error", "Name and Class are required for student")
                    return
                
                AccountService.add_student(name, class_name, parent_name, phone, user_id)
            
            elif role == "staff":
                name = self.staff_name_entry.get().strip()
                salary = self.salary_entry.get().strip()
                
                if not name or not salary:
                    messagebox.showerror("Error", "Name and Salary are required for staff")
                    return
                
                AccountService.add_staff(
                    name,
                    self.father_name_entry.get().strip(),
                    self.qualification_entry.get().strip(),
                    self.department_entry.get().strip(),
                    self.designation_entry.get().strip(),
                    float(salary),
                    user_id
                )
            
            messagebox.showinfo("Success", f"{role.capitalize()} registered successfully!")
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear_form(self):
        """Clear all form fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_var.set("student")
        
        # Clear student fields
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.parent_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        
        # Clear staff fields
        self.staff_name_entry.delete(0, tk.END)
        self.father_name_entry.delete(0, tk.END)
        self.qualification_entry.delete(0, tk.END)
        self.department_entry.delete(0, tk.END)
        self.designation_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)
        
        self.on_role_change()
    
    def on_back(self):
        """Navigate back to dashboard"""
        if self.current_user:
            self.switch_callback("dashboard", self.current_user)
        else:
            self.switch_callback("home")