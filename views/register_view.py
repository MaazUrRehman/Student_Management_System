
# register_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService
from utils.constants import COLORS, FONTS


class RegisterView:
    ROLE_LABELS = {
        "admin": "Admin",
        "accountant": "Accountant",
        "student": "Student",
        "staff": "Staff"
    }

    def __init__(self, root, switch_callback, current_user=None):
        self.root = root
        self.switch_callback = switch_callback
        self.current_user = current_user
        self.frame = None
        self.role_var = tk.StringVar()
        self.error_label = None
        self.student_fields_frame = None
        self.staff_fields_frame = None
        self.name_entry = None
        self.class_entry = None
        self.parent_entry = None
        self.phone_entry = None
        self.staff_name_entry = None
        self.father_name_entry = None
        self.qualification_entry = None
        self.department_entry = None
        self.designation_entry = None
        self.salary_entry = None
        self.create_ui()

    def get_allowed_roles(self):
        return AuthService.get_allowed_registration_roles(self.current_user)

    def create_ui(self):
        allowed_roles = self.get_allowed_roles()

        self.frame = tk.Frame(self.root, bg=COLORS["background"])
        self.frame.pack(fill=tk.BOTH, expand=True)

        if not allowed_roles:
            messagebox.showerror("Access Denied", "You are not allowed to access the registration screen.")
            self.show_access_denied()
            return

        # Use parent directly - Dashboard already provides scrollable frame
        page = self.frame

        # Header Card
        header_card = self.create_card(page)
        header_card.pack(fill=tk.X, pady=(0, 20))

        tk.Label(header_card, text="👤 Register New User", font=FONTS["title"],
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 5))
        
        subtitle = "Create users based on your role permissions."
        if self.current_user and self.current_user.get("role") == "accountant":
            subtitle = "You can only register student accounts."
        
        tk.Label(header_card, text=subtitle, font=FONTS["normal"],
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=20, pady=(0, 20))

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

        role_frame = tk.Frame(account_section, bg=COLORS["card"])
        role_frame.grid(row=2, column=1, padx=(0, 20), pady=8, sticky="w")

        self.role_var.set(allowed_roles[0])
        for role in allowed_roles:
            tk.Radiobutton(
                role_frame,
                text=self.ROLE_LABELS[role],
                variable=self.role_var,
                value=role,
                bg=COLORS["card"],
                fg=COLORS["text_primary"],
                selectcolor=COLORS["primary_lighter"],
                activebackground=COLORS["card"],
                activeforeground=COLORS["primary"],
                font=FONTS["normal"],
                command=self.toggle_role_fields
            ).pack(side=tk.LEFT, padx=8)

        account_section.grid_columnconfigure(1, weight=1)

        # Student Details Section
        self.student_section = tk.LabelFrame(form_card, text="Student Details",
                                             font=FONTS["heading"], bg=COLORS["card"],
                                             fg=COLORS["primary"], padx=20, pady=15)

        # Student fields
        fields = [
            ("Full Name", "name_entry"),
            ("Class", "class_entry"),
            ("Parent/Guardian Name", "parent_entry"),
            ("Phone Number", "phone_entry")
        ]

        for idx, (label, attr) in enumerate(fields):
            tk.Label(self.student_section, text=label, font=FONTS["normal"],
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=idx, column=0, padx=(0, 10), pady=8, sticky=tk.W)
            entry = self.create_styled_entry(self.student_section)
            entry.grid(row=idx, column=1, padx=(0, 20), pady=8, sticky="ew")
            setattr(self, attr, entry)

        self.student_section.grid_columnconfigure(1, weight=1)

        # Staff Details Section
        self.staff_section = tk.LabelFrame(form_card, text="Staff Details",
                                           font=FONTS["heading"], bg=COLORS["card"],
                                           fg=COLORS["primary"], padx=20, pady=15)

        # Staff fields
        staff_fields = [
            ("Full Name", "staff_name_entry"),
            ("Father's Name", "father_name_entry"),
            ("Qualification", "qualification_entry"),
            ("Department", "department_entry"),
            ("Designation", "designation_entry"),
            ("Salary ($)", "salary_entry")
        ]

        for idx, (label, attr) in enumerate(staff_fields):
            tk.Label(self.staff_section, text=label, font=FONTS["normal"],
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=idx, column=0, padx=(0, 10), pady=8, sticky=tk.W)
            entry = self.create_styled_entry(self.staff_section)
            entry.grid(row=idx, column=1, padx=(0, 20), pady=8, sticky="ew")
            setattr(self, attr, entry)

        self.staff_section.grid_columnconfigure(1, weight=1)

        # Error label
        self.error_label = tk.Label(form_card, text="", font=FONTS["small"],
                                   bg=COLORS["card"], fg=COLORS["danger"])
        self.error_label.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(form_card, bg=COLORS["card"])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.create_button(btn_frame, "Register User", self.on_register, "success").pack(side=tk.LEFT, padx=(0, 10))
        self.create_button(btn_frame, "Back to Dashboard", self.on_back, "secondary").pack(side=tk.LEFT)

        self.toggle_role_fields()

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

    def show_access_denied(self):
        """Show access denied message"""
        denied_card = self.create_card(self.frame)
        denied_card.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        tk.Label(denied_card, text="⛔ Access Denied", font=FONTS["title"],
                bg=COLORS["card"], fg=COLORS["danger"]).pack(padx=40, pady=(30, 10))
        tk.Label(denied_card, text="Registration is only available from the dashboard for authorized users.",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(padx=40, pady=(0, 20))

        self.create_button(denied_card, "Return to Dashboard", self.on_back, "primary").pack(pady=(0, 30))

    def toggle_role_fields(self):
        """Toggle role-specific fields"""
        selected_role = self.role_var.get()

        # Hide all sections first
        self.student_section.pack_forget()
        self.staff_section.pack_forget()

        if selected_role == "student":
            self.student_section.pack(fill=tk.X, padx=20, pady=(0, 15))
        elif selected_role == "staff":
            self.staff_section.pack(fill=tk.X, padx=20, pady=(0, 15))

    def on_register(self):
        """Register new user"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            self.error_label.config(text="Please enter username and password")
            return

        student_data = None
        staff_data = None

        if role == "student":
            student_data = {
                "name": self.name_entry.get().strip(),
                "class_name": self.class_entry.get().strip(),
                "parent_name": self.parent_entry.get().strip(),
                "phone": self.phone_entry.get().strip()
            }

            if not student_data["name"] or not student_data["class_name"]:
                self.error_label.config(text="Student name and class are required")
                return

        if role == "staff":
            staff_data = {
                "name": self.staff_name_entry.get().strip(),
                "father_name": self.father_name_entry.get().strip(),
                "qualification": self.qualification_entry.get().strip(),
                "department": self.department_entry.get().strip(),
                "designation": self.designation_entry.get().strip(),
                "salary": self.salary_entry.get().strip()
            }

            if not staff_data["name"] or not staff_data["salary"]:
                self.error_label.config(text="Staff name and salary are required")
                return

        try:
            AuthService.create_user(
                self.current_user,
                username,
                password,
                role,
                student_data=student_data,
                staff_data=staff_data
            )
            self.error_label.config(text="")
            messagebox.showinfo("Success", f"{role.capitalize()} registered successfully!")
            self.reset_form()
        except Exception as exc:
            self.error_label.config(text=str(exc))

    def reset_form(self):
        """Reset form fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        allowed_roles = self.get_allowed_roles()
        if allowed_roles:
            self.role_var.set(allowed_roles[0])

        # Clear student entries
        for entry in [self.name_entry, self.class_entry, self.parent_entry, self.phone_entry]:
            if entry:
                entry.delete(0, tk.END)

        # Clear staff entries
        for entry in [self.staff_name_entry, self.father_name_entry, self.qualification_entry,
                     self.department_entry, self.designation_entry, self.salary_entry]:
            if entry:
                entry.delete(0, tk.END)

        self.toggle_role_fields()

    def on_back(self):
        """Navigate back"""
        if self.current_user:
            self.switch_callback("dashboard", self.current_user)
        else:
            self.switch_callback("home")

    def destroy(self):
        if self.frame:
            self.frame.destroy()