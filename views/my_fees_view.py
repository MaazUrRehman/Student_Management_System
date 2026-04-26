

# my_fees_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class MyFeesView:
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
        
        tk.Label(header_card, text="📋 My Fee Structure", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 5))
        tk.Label(header_card, text="View all your fee invoices and payment status",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Late fee information card
        info_card = self.create_card(page)
        info_card.pack(fill=tk.X, pady=(0, 20))
        
        info_frame = tk.Frame(info_card, bg=COLORS["primary_lighter"])
        info_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(info_frame, text="ℹ️ Late Fee Policy", font=FONTS["heading"], 
                bg=COLORS["primary_lighter"], fg=COLORS["primary"]).pack(anchor=tk.W)
        tk.Label(info_frame, text="A 5% late fee is applied to invoices that are not paid by the due date.", 
                font=FONTS["small"], bg=COLORS["primary_lighter"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, pady=(5, 0))
        
        # Fee Table
        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True)
        
        table_header = tk.Frame(table_card, bg=COLORS["card"])
        table_header.pack(fill=tk.X, padx=20, pady=(16, 10))
        tk.Label(table_header, text="📊 Invoice List", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)
        
        # Table Frame
        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Treeview with scrollbars
        columns = ("Invoice ID", "Total Amount", "Discount", "Final Amount", "Due Date", "Late Fee", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                 height=12, style="Modern.Treeview")
        
        # Configure columns
        column_widths = {"Invoice ID": 100, "Total Amount": 120, "Discount": 100, 
                        "Final Amount": 120, "Due Date": 120, "Late Fee": 100, "Status": 120}
        
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
        
        self.load_fees()
    
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
    
    def load_fees(self):
        """Load fees into treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        student = self.get_student_by_user_id()
        
        if not student:
            return
        
        invoices = AccountService.get_student_invoices(student["id"])
        
        for inv in invoices:
            fee_info = AccountService.calculate_late_fee(inv["id"])
            late_fee = fee_info["late_fee"] if fee_info else 0
            is_overdue = fee_info["is_overdue"] if fee_info else False
            
            # Format status with badge
            status = inv["status"].upper()
            if is_overdue and status != "PAID":
                status = "⚠️ OVERDUE"
            elif status == "paid":
                status = "✅ PAID"
            elif status == "pending":
                status = "⏳ PENDING"
            
            # Determine row tag based on status
            tag = "overdue" if is_overdue and status != "✅ PAID" else "normal"
            
            item_id = self.tree.insert("", tk.END, values=(
                inv["id"],
                f"${inv['total_amount']:.2f}",
                f"${inv['discount_amount']:.2f}",
                f"${inv['final_amount']:.2f}",
                inv["due_date"] or "N/A",
                f"${late_fee:.2f}",
                status
            ), tags=(tag,))
            
            # Color code overdue items
            if tag == "overdue":
                self.tree.tag_configure("overdue", background=COLORS["status_overdue"])
    
    def get_student_by_user_id(self):
        students = AccountService.get_all_students()
        for student in students:
            if student.get("user_id") == self.user["id"]:
                return student
        return None