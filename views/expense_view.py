# expense_view.py
import tkinter as tk
from tkinter import ttk, messagebox

from services.account_service import AccountService
from utils.constants import COLORS, FONTS, BUTTON_STYLES


class ExpenseView:
    def __init__(self, parent, user, switch_callback=None):
        self.parent = parent
        self.user = user
        self.switch_callback = switch_callback
        self.create_ui()

    def create_ui(self):
        self.configure_tree_style()
        
        # Use parent directly - Dashboard already provides scrollable frame
        page = self.parent

        # Header Card
        header = self.create_card(page)
        header.pack(fill=tk.X, pady=(0, 20))
        
        header_left = tk.Frame(header, bg=COLORS["card"])
        header_left.pack(side=tk.LEFT, padx=20, pady=16)
        
        tk.Label(header_left, text="💰 Expenses", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        tk.Label(header_left, text="Monitor recorded expenses and total spending.",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W)
        
        if self.user["role"] in ["admin", "accountant"]:
            self.create_button(header, "📊 Dashboard", self.go_dashboard, "outline").pack(side=tk.RIGHT, padx=20, pady=16)

        # Add Expense Form (Admin only)
        if self.user["role"] == "admin":
            form = self.create_card(page)
            form.pack(fill=tk.X, pady=(0, 20))
            
            # Form header with icon
            form_header = tk.Frame(form, bg=COLORS["card"])
            form_header.pack(fill=tk.X, padx=20, pady=(16, 10))
            tk.Label(form_header, text="➕ Add New Expense", font=FONTS["heading"], 
                    bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)
            
            # Form fields in grid
            fields_frame = tk.Frame(form, bg=COLORS["card"])
            fields_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            # Configure grid columns
            for i in range(6):
                fields_frame.grid_columnconfigure(i, weight=1)
            
            # Title
            tk.Label(fields_frame, text="Title", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=0, padx=(0, 10), sticky="w")
            self.title_entry = self.create_styled_entry(fields_frame)
            self.title_entry.grid(row=1, column=0, padx=(0, 10), sticky="ew", pady=(0, 10))
            
            # Category
            tk.Label(fields_frame, text="Category", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=1, padx=10, sticky="w")
            self.category_entry = self.create_styled_entry(fields_frame)
            self.category_entry.grid(row=1, column=1, padx=10, sticky="ew", pady=(0, 10))
            
            # Amount
            tk.Label(fields_frame, text="Amount ($)", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=2, padx=10, sticky="w")
            self.amount_entry = self.create_styled_entry(fields_frame)
            self.amount_entry.grid(row=1, column=2, padx=10, sticky="ew", pady=(0, 10))
            
            # Add button
            self.create_button(fields_frame, "Add Expense", self.add_expense, "success").grid(
                row=1, column=3, padx=20, sticky="ew", pady=(0, 10))

        # Total Expenses Card
        total_card = self.create_card(page)
        total_card.pack(fill=tk.X, pady=(0, 20))
        
        total_frame = tk.Frame(total_card, bg=COLORS["card"])
        total_frame.pack(fill=tk.X, padx=20, pady=16)
        
        tk.Label(total_frame, text="Total Expenses", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT)
        
        total_amount = AccountService.get_total_expenses()
        tk.Label(total_frame, text=f"${total_amount:,.2f}", 
                font=("Inter", 24, "bold"), bg=COLORS["card"], fg=COLORS["danger"]).pack(side=tk.RIGHT)

        # Expense Table
        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True)
        
        table_header = tk.Frame(table_card, bg=COLORS["card"])
        table_header.pack(fill=tk.X, padx=20, pady=(16, 10))
        tk.Label(table_header, text="📋 Expense List", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)
        
        # Table Frame
        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))
        
        # Treeview with scrollbars
        columns = ("ID", "Title", "Category", "Amount", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                 height=12, style="Modern.Treeview")
        
        # Configure columns
        column_widths = {"ID": 60, "Title": 200, "Category": 150, "Amount": 120, "Date": 120}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), 
                           anchor=tk.CENTER if col in ("ID", "Amount") else tk.W)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Delete button for admin
        if self.user["role"] == "admin":
            action_frame = tk.Frame(table_card, bg=COLORS["card"])
            action_frame.pack(fill=tk.X, padx=20, pady=(0, 16))
            self.create_button(action_frame, "🗑️ Delete Selected", self.delete_expense, "danger").pack(side=tk.RIGHT)

        self.load_expenses()

    def create_styled_entry(self, parent):
        """Create a styled entry widget"""
        entry = tk.Entry(parent, font=FONTS["normal"], relief="flat", 
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
            "outline": (COLORS["card"], COLORS["primary"])
        }
        
        bg_color, hover_color = color_map.get(variant, color_map["primary"])
        fg_color = COLORS["text_primary"] if variant == "outline" else COLORS["text_light"]
        
        button = tk.Button(parent, text=text, command=command, font=FONTS["button"],
                          bg=bg_color, fg=fg_color,
                          activebackground=hover_color, activeforeground=COLORS["text_light"],
                          relief="flat", bd=0, cursor="hand2", padx=16, pady=8)
        
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
                       background=COLORS["primary"], 
                       foreground=COLORS["text_primary"], 
                       font=FONTS["table_header"])
        style.map("Modern.Treeview", 
                 background=[("selected", COLORS["primary_light"])], 
                 foreground=[("selected", COLORS["text_light"])])

    def load_expenses(self):
        """Load expenses into treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        expenses = AccountService.get_all_expenses()
        # Sort by ID ascending
        expenses.sort(key=lambda x: x.get("id", 0))
        for index, exp in enumerate(expenses):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(
                exp["id"],
                exp["title"],
                exp["category"],
                f"${exp['amount']:.2f}",
                exp["date"]
            ), tags=(tag,))
        
        self.tree.tag_configure("evenrow", background=COLORS["card"])
        self.tree.tag_configure("oddrow", background=COLORS["background"])

    def add_expense(self):
        """Add new expense"""
        title = self.title_entry.get().strip()
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()
        
        if not title or not category or not amount:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            AccountService.add_expense(title, category, float(amount))
            messagebox.showinfo("Success", "Expense added successfully!")
            self.title_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.load_expenses()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete_expense(self):
        """Delete selected expense"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            return
        
        expense_id = self.tree.item(selected[0])["values"][0]
        try:
            AccountService.delete_expense(expense_id)
            messagebox.showinfo("Success", "Expense deleted successfully!")
            self.load_expenses()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def go_dashboard(self):
        if self.switch_callback:
            self.switch_callback("dashboard", self.user)