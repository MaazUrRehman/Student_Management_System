



# staff_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class StaffView:
    def __init__(self, parent, user, switch_callback=None):
        self.parent = parent
        self.user = user
        self.switch_callback = switch_callback
        self.create_ui()

    def create_ui(self):
        self.configure_tree_style()

        page = tk.Frame(self.parent, bg=COLORS["background"])
        page.pack(fill=tk.BOTH, expand=True)

        # Header Card
        header = self.create_card(page)
        header.pack(fill=tk.X, pady=(0, 20))

        header_left = tk.Frame(header, bg=COLORS["card"])
        header_left.pack(side=tk.LEFT, padx=20, pady=16)

        tk.Label(header_left, text="👥 Staff Management", font=FONTS["title"],
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        tk.Label(header_left, text="Create staff accounts through Register User, then manage them here",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W)

        if self.user["role"] in ["admin", "accountant"]:
            self.create_button(header, "📊 Dashboard", self.go_dashboard, "outline").pack(side=tk.RIGHT, padx=20, pady=16)

        # Search Card
        search_card = self.create_card(page)
        search_card.pack(fill=tk.X, pady=(0, 20))

        search_inner = tk.Frame(search_card, bg=COLORS["card"])
        search_inner.pack(fill=tk.X, padx=20, pady=16)

        tk.Label(search_inner, text="🔍 Search Staff", font=FONTS["heading"],
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT, padx=(0, 15))

        self.search_entry = self.create_styled_entry(search_inner, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.create_button(search_inner, "Search", self.search_staff, "secondary").pack(side=tk.LEFT, padx=5)
        self.create_button(search_inner, "Show All", self.load_staff, "primary").pack(side=tk.LEFT, padx=5)

        # Staff Table
        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True)

        table_header = tk.Frame(table_card, bg=COLORS["card"])
        table_header.pack(fill=tk.X, padx=20, pady=(16, 10))
        tk.Label(table_header, text="📋 Staff List", font=FONTS["heading"],
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)

        # Table Frame
        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Treeview with scrollbars
        columns = ("ID", "Name", "Department", "Designation", "Salary", "Qualification")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                 height=12, style="Modern.Treeview")

        # Configure columns
        column_widths = {"ID": 70, "Name": 180, "Department": 140, "Designation": 140, "Salary": 120, "Qualification": 160}

        for col in columns:
            anchor = tk.CENTER if col in ("ID", "Salary") else tk.W
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 120), anchor=anchor)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Delete button for admin/accountant
        if self.user["role"] in ["admin", "accountant"]:
            action_frame = tk.Frame(table_card, bg=COLORS["card"])
            action_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
            self.create_button(action_frame, "🗑️ Delete Selected", self.delete_staff, "danger").pack(side=tk.RIGHT)

        self.load_staff()

    def create_styled_entry(self, parent, width=None):
        """Create a styled entry widget"""
        entry = tk.Entry(parent, font=FONTS["normal"], relief="flat", width=width,
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
            "danger": (COLORS["danger"], "#DC2626"),
            "outline": (COLORS["card"], COLORS["primary"])
        }

        bg_color, hover_color = color_map.get(variant, color_map["primary"])
        fg_color = COLORS["text_primary"] if variant == "outline" else COLORS["text_light"]

        button = tk.Button(parent, text=text, command=command, font=FONTS["button"],
                          bg=bg_color, fg=fg_color,
                          activebackground=hover_color, activeforeground=COLORS["text_light"],
                          relief="flat", bd=0, cursor="hand2", padx=14, pady=7)

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

    def configure_tree_style(self):
        """Configure treeview styling"""
        style = ttk.Style()
        style.configure("Modern.Treeview",
                       background=COLORS["card"],
                       fieldbackground=COLORS["card"],
                       foreground=COLORS["text_primary"],
                       rowheight=32,
                       font=FONTS["table_cell"])
        style.configure("Modern.Treeview.Heading",
                       background=COLORS["table_header"],
                       foreground=COLORS["text_primary"],
                       font=FONTS["table_header"])
        style.map("Modern.Treeview",
                 background=[("selected", COLORS["primary_light"])],
                 foreground=[("selected", COLORS["text_light"])])

    def load_staff(self):
        """Load all staff into treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        staff_list = sorted(AccountService.get_all_staff(), key=lambda staff: staff.get("id", 0))
        for idx, staff in enumerate(staff_list):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(
                staff["id"],
                staff["name"],
                staff.get("department", "-"),
                staff.get("designation", "-"),
                f"${staff['salary']:.2f}",
                staff.get("qualification", "-")
            ), tags=(tag,))

        self.tree.tag_configure("evenrow", background=COLORS["card"])
        self.tree.tag_configure("oddrow", background=COLORS["background"])

    def search_staff(self):
        """Search staff by name"""
        query = self.search_entry.get().strip()
        if not query:
            self.load_staff()
            return

        results = sorted(AccountService.search_staff(query), key=lambda staff: staff.get("id", 0))

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, staff in enumerate(results):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(
                staff["id"],
                staff["name"],
                staff.get("department", "-"),
                staff.get("designation", "-"),
                f"${staff['salary']:.2f}",
                staff.get("qualification", "-")
            ), tags=(tag,))

    def delete_staff(self):
        """Delete selected staff member"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a staff member to delete")
            return

        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this staff member?"):
            return

        staff_id = self.tree.item(selected[0])["values"][0]
        try:
            AccountService.delete_staff(staff_id)
            messagebox.showinfo("Success", "Staff deleted successfully!")
            self.load_staff()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def go_dashboard(self):
        if self.switch_callback:
            self.switch_callback("dashboard", self.user)
