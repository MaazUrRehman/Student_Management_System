

# report_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class ReportView:
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

        tk.Label(header_left, text="📊 Reports & Summary", font=FONTS["title"],
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        tk.Label(header_left, text="Combined financial activity across payments, expenses, and salaries",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W)

        if self.user["role"] in ["admin", "accountant"]:
            self.create_button(header, "📊 Dashboard", self.go_dashboard, "outline").pack(side=tk.RIGHT, padx=20, pady=16)

        # Summary Cards
        summary = AccountService.get_enhanced_financial_summary()
        cards_frame = tk.Frame(page, bg=COLORS["background"])
        cards_frame.pack(fill=tk.X, pady=(0, 20))

        # Configure grid for 4 columns
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        summary_items = [
            ("Total Income", f"${summary['total_income']:,.2f}", COLORS["success"]),
            ("Total Expenses", f"${summary['total_expenses']:,.2f}", COLORS["danger"]),
            ("Pending Fees", f"${summary['pending_fees']:,.2f}", COLORS["warning"]),
            ("Pending Salaries", f"${summary['pending_salaries']:,.2f}", COLORS["warning"]),
            ("Salary Expenses", f"${summary['salary_expenses']:,.2f}", COLORS["primary"]),
            ("Regular Expenses", f"${summary['regular_expenses']:,.2f}", COLORS["secondary"]),
            ("Total Students", str(len(AccountService.get_all_students())), COLORS["primary"]),
            ("Total Staff", str(AccountService.get_staff_count()), COLORS["secondary"])
        ]

        for idx, (title, value, color) in enumerate(summary_items):
            row = idx // 4
            col = idx % 4
            self.create_summary_card(cards_frame, title, value, color, row, col)

        # Transaction Table
        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True)

        table_header = tk.Frame(table_card, bg=COLORS["card"])
        table_header.pack(fill=tk.X, padx=20, pady=(16, 10))
        tk.Label(table_header, text="📋 Transaction Summary", font=FONTS["heading"],
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)

        # Table Frame
        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Treeview with scrollbars
        columns = ("Transaction ID", "Type", "Description", "Amount", "Date", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                 height=15, style="Modern.Treeview")

        # Configure columns
        column_widths = {"Transaction ID": 130, "Type": 100, "Description": 350,
                        "Amount": 120, "Date": 140, "Status": 110}

        for col in columns:
            anchor = tk.W if col == "Description" else tk.CENTER
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 120), anchor=anchor)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.load_transactions()

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

    def create_summary_card(self, parent, title, value, color, row, col):
        """Create a summary statistics card"""
        card = tk.Frame(parent, bg=COLORS["card"],
                       highlightbackground=COLORS["border"],
                       highlightthickness=1)
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        tk.Label(card, text=title, font=FONTS["normal"],
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=14, pady=(14, 6))
        tk.Label(card, text=value, font=("Inter", 16, "bold"),
                bg=COLORS["card"], fg=color).pack(anchor=tk.W, padx=14, pady=(0, 14))

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

    def load_transactions(self):
        """Load transactions into treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        transactions = []

        # Add payment transactions
        for payment in AccountService.get_all_payments():
            transactions.append({
                "id": f"PAY-{payment['id']}",
                "type": "Income",
                "description": f"Payment received from {payment.get('student_name', 'Student')}",
                "amount": payment.get("amount_paid", 0),
                "date": payment.get("payment_date") or "",
                "status": "Completed"
            })

        # Add expense transactions
        for expense in AccountService.get_all_expenses():
            status = "Salary" if expense.get("category") == "salary" else "Operational"
            transactions.append({
                "id": f"EXP-{expense['id']}",
                "type": "Expense",
                "description": expense.get("title", "Expense"),
                "amount": -expense.get("amount", 0),
                "date": expense.get("date") or "",
                "status": status
            })

        # Add salary transactions
        for salary in AccountService.get_all_salary_records():
            status_color = "Paid" if salary.get("status") == "paid" else "Pending"
            transactions.append({
                "id": f"SAL-{salary['id']}",
                "type": "Salary",
                "description": f"{salary.get('staff_name', 'Staff')} - {salary.get('month', '')}",
                "amount": -salary.get("salary_amount", 0),
                "date": salary.get("payment_date") or salary.get("due_date") or "",
                "status": status_color
            })

        # Sort by date (latest to oldest) - parse date for proper sorting
        def parse_date(date_str):
            if not date_str:
                return datetime.min
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except:
                return datetime.min
        
        transactions.sort(key=lambda item: parse_date(item["date"]), reverse=True)

        for idx, transaction in enumerate(transactions):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            amount_color = COLORS["success"] if transaction["amount"] > 0 else COLORS["danger"]
            amount_text = f"${abs(transaction['amount']):,.2f}"
            if transaction["amount"] > 0:
                amount_text = f"+{amount_text}"
            else:
                amount_text = f"-{amount_text}"

            self.tree.insert("", tk.END, values=(
                transaction["id"],
                transaction["type"],
                transaction["description"],
                amount_text,
                transaction["date"],
                transaction["status"]
            ), tags=(tag,))

        self.tree.tag_configure("evenrow", background=COLORS["card"])
        self.tree.tag_configure("oddrow", background=COLORS["background"])

    def go_dashboard(self):
        if self.switch_callback:
            self.switch_callback("dashboard", self.user)
