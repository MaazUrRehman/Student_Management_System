
# my_salary_view.py
import tkinter as tk
from tkinter import ttk
from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class MySalaryView:
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
        
        tk.Label(header_card, text="💰 My Salary", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 5))
        tk.Label(header_card, text="View your salary records and payment history",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        staff = AccountService.get_staff_by_user_id(self.user["id"])
        
        if not staff:
            error_card = self.create_card(page)
            error_card.pack(fill=tk.X, pady=20)
            tk.Label(error_card, text="⚠️ No staff record found", 
                    font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["danger"]).pack(pady=40)
            return
        
        # Salary Summary Card
        summary_card = self.create_card(page)
        summary_card.pack(fill=tk.X, pady=(0, 20))
        
        summary_inner = tk.Frame(summary_card, bg=COLORS["card"])
        summary_inner.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(summary_inner, text="Base Salary", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT)
        tk.Label(summary_inner, text=f"${staff['salary']:,.2f}", 
                font=("Inter", 20, "bold"), bg=COLORS["card"], fg=COLORS["success"]).pack(side=tk.RIGHT)
        
        # Salary Records Table
        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True)
        
        table_header = tk.Frame(table_card, bg=COLORS["card"])
        table_header.pack(fill=tk.X, padx=20, pady=(16, 10))
        tk.Label(table_header, text="📋 Salary Records", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)
        
        # Table Frame
        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Treeview with scrollbars
        columns = ("ID", "Month", "Amount", "Due Date", "Status", "Payment Date", "Method")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                 height=12, style="Modern.Treeview")
        
        # Configure columns
        column_widths = {"ID": 60, "Month": 100, "Amount": 120, "Due Date": 120, 
                        "Status": 100, "Payment Date": 120, "Method": 100}
        
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
        
        self.load_salary_records(staff["id"])
    
    def create_card(self, parent):
        """Create a styled card frame"""
        card = tk.Frame(parent, bg=COLORS["card"], 
                       highlightbackground=COLORS["border"], 
                       highlightthickness=1)
        return card
    
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
    
    def load_salary_records(self, staff_id):
        """Load salary records into treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = AccountService.get_staff_salaries(staff_id)
        
        for idx, record in enumerate(records):
            # Determine status color tag
            status = record["status"].upper()
            if status == "PAID":
                tag = "paid"
            elif status == "PENDING":
                tag = "pending"
            else:
                tag = "normal"
            
            item_id = self.tree.insert("", tk.END, values=(
                record["id"],
                record["month"],
                f"${record['salary_amount']:.2f}",
                record.get("due_date") or "N/A",
                f"✅ {status}" if status == "PAID" else f"⏳ {status}",
                record.get("payment_date") or "N/A",
                (record.get("payment_method") or "N/A").upper()
            ), tags=(tag,))
            
            # Configure tags with colors
            self.tree.tag_configure("paid", background=COLORS["status_paid"])
            self.tree.tag_configure("pending", background=COLORS["status_pending"])
