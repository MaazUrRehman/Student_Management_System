
# my_payments_view.py
import tkinter as tk
from tkinter import ttk
from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class MyPaymentsView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.create_ui()
    
    def create_ui(self):
        self.configure_tree_style()
        
        # Use parent directly - Dashboard already provides scrollable frame
        page = self.parent
        
        # Header Card
        header_card = self.create_card(page)
        header_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_card, text="💳 Payment History", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 5))
        tk.Label(header_card, text="View all your payment transactions",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Summary Cards
        student = self.get_student_by_user_id()
        total_paid = 0
        payment_count = 0
        
        if student:
            invoices = AccountService.get_student_invoices(student["id"])
            for inv in invoices:
                payments = AccountService.get_invoice_payments(inv["id"])
                payment_count += len(payments)
                for payment in payments:
                    total_paid += payment["amount_paid"]
        
        # Summary Frame
        summary_frame = tk.Frame(page, bg=COLORS["background"])
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        for i in range(2):
            summary_frame.grid_columnconfigure(i, weight=1)
        
        self.create_summary_card(summary_frame, "💰 Total Payments", f"${total_paid:,.2f}", 
                                 COLORS["success"], 0, 0)
        self.create_summary_card(summary_frame, "📊 Total Transactions", str(payment_count), 
                                 COLORS["primary"], 0, 1)
        
        # Payments Table
        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True)
        
        table_header = tk.Frame(table_card, bg=COLORS["card"])
        table_header.pack(fill=tk.X, padx=20, pady=(16, 10))
        tk.Label(table_header, text="📋 Transaction History", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)
        
        # Table Frame
        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Treeview with scrollbars
        columns = ("Payment ID", "Invoice ID", "Amount", "Method", "Date", "Time")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                 height=12, style="Modern.Treeview")
        
        # Configure columns
        column_widths = {"Payment ID": 100, "Invoice ID": 100, "Amount": 120, 
                        "Method": 120, "Date": 120, "Time": 100}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.load_payments()
    
    def create_card(self, parent):
        """Create a styled card frame"""
        card = tk.Frame(parent, bg=COLORS["card"], 
                       highlightbackground=COLORS["border"], 
                       highlightthickness=1)
        return card
    
    def create_summary_card(self, parent, title, value, color, row, col):
        """Create a summary statistics card"""
        card = tk.Frame(parent, bg=COLORS["card"], 
                       highlightbackground=COLORS["border"], 
                       highlightthickness=1)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        
        tk.Label(card, text=title, font=FONTS["normal"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=15, pady=(15, 5))
        tk.Label(card, text=value, font=("Inter", 18, "bold"), 
                bg=COLORS["card"], fg=color).pack(anchor=tk.W, padx=15, pady=(0, 15))
    
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
                       foreground=COLORS["text_light"], 
                       font=FONTS["table_header"])
        style.map("Modern.Treeview", 
                 background=[("selected", COLORS["primary_light"])], 
                 foreground=[("selected", COLORS["text_light"])])
    
    def load_payments(self):
        """Load payments into treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        student = self.get_student_by_user_id()
        
        if not student:
            return
        
        invoices = AccountService.get_student_invoices(student["id"])
        
        for inv in invoices:
            payments = AccountService.get_invoice_payments(inv["id"])
            
            for idx, payment in enumerate(payments):
                # Split date and time if needed
                payment_date = payment["payment_date"]
                date_part = payment_date.split()[0] if payment_date else "N/A"
                time_part = payment_date.split()[1] if payment_date and len(payment_date.split()) > 1 else "N/A"
                
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values=(
                    payment["id"],
                    payment["invoice_id"],
                    f"${payment['amount_paid']:.2f}",
                    payment["payment_method"].upper(),
                    date_part,
                    time_part
                ), tags=(tag,))
        
        self.tree.tag_configure("evenrow", background=COLORS["card"])
        self.tree.tag_configure("oddrow", background=COLORS["background"])
    
    def get_student_by_user_id(self):
        students = AccountService.get_all_students()
        for student in students:
            if student.get("user_id") == self.user["id"]:
                return student
        return None