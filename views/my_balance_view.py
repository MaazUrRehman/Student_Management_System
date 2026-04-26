
# my_balance_view.py
import tkinter as tk
from tkinter import ttk
from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class MyBalanceView:
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
        
        tk.Label(header_card, text="💰 My Balance", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 5))
        tk.Label(header_card, text="View your complete fee balance and payment summary",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        student = self.get_student_by_user_id()
        
        if not student:
            error_card = self.create_card(page)
            error_card.pack(fill=tk.X, pady=20)
            tk.Label(error_card, text="⚠️ No student record found", 
                    font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["danger"]).pack(pady=40)
            return
        
        # Calculate totals
        invoices = AccountService.get_student_invoices(student["id"])
        
        total_payable = 0
        total_paid = 0
        total_late_fees = 0
        
        for inv in invoices:
            fee_info = AccountService.calculate_late_fee(inv["id"])
            if fee_info:
                total_payable += fee_info["original_amount"]
                total_paid += fee_info["total_paid"]
                total_late_fees += fee_info["late_fee"]
        
        total_with_late_fees = total_payable + total_late_fees
        balance = total_with_late_fees - total_paid
        
        # Summary Cards
        summary_frame = tk.Frame(page, bg=COLORS["background"])
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Configure grid for summary cards
        for i in range(3):
            summary_frame.grid_columnconfigure(i, weight=1)
        
        # Create summary cards
        self.create_summary_card(summary_frame, "💰 Total Payable", f"${total_payable:,.2f}", 
                                 COLORS["primary"], 0, 0)
        self.create_summary_card(summary_frame, "⚠️ Late Fees", f"${total_late_fees:,.2f}", 
                                 COLORS["warning"], 0, 1)
        self.create_summary_card(summary_frame, "✅ Total Paid", f"${total_paid:,.2f}", 
                                 COLORS["success"], 0, 2)
        
        # Balance Card (Prominent)
        balance_card = self.create_card(page)
        balance_card.pack(fill=tk.X, pady=(0, 20))
        
        balance_inner = tk.Frame(balance_card, bg=COLORS["card"])
        balance_inner.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(balance_inner, text="Current Balance", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT)
        
        balance_color = COLORS["danger"] if balance > 0 else COLORS["success"]
        balance_text = f"${balance:,.2f}"
        if balance > 0:
            balance_text = f"⚠️ {balance_text} Due"
        elif balance < 0:
            balance_text = f"✅ {balance_text} Credit"
        else:
            balance_text = f"✅ {balance_text} Paid"
        
        tk.Label(balance_inner, text=balance_text, font=("Inter", 20, "bold"), 
                bg=COLORS["card"], fg=balance_color).pack(side=tk.RIGHT)
        
        # Detailed breakdown card
        breakdown_card = self.create_card(page)
        breakdown_card.pack(fill=tk.X)
        
        tk.Label(breakdown_card, text="📋 Detailed Breakdown", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Create breakdown table
        table_frame = tk.Frame(breakdown_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Headers
        headers = ["Description", "Amount"]
        for i, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=FONTS["table_header"], 
                    bg=COLORS["table_header"], fg=COLORS["text_primary"],
                    padx=15, pady=10).grid(row=0, column=i, sticky="ew")
        
        # Add breakdown rows
        breakdown_items = [
            ("Total Payable Amount", f"${total_payable:,.2f}"),
            ("Late Fees Applied", f"${total_late_fees:,.2f}"),
            ("Subtotal (with late fees)", f"${total_with_late_fees:,.2f}"),
            ("Total Payments Made", f"${total_paid:,.2f}"),
        ]
        
        for idx, (desc, amount) in enumerate(breakdown_items, start=1):
            bg_color = COLORS["card"] if idx % 2 == 0 else COLORS["background"]
            tk.Label(table_frame, text=desc, font=FONTS["normal"], 
                    bg=bg_color, fg=COLORS["text_secondary"],
                    padx=15, pady=8).grid(row=idx, column=0, sticky="ew")
            tk.Label(table_frame, text=amount, font=FONTS["normal"], 
                    bg=bg_color, fg=COLORS["text_primary"],
                    padx=15, pady=8).grid(row=idx, column=1, sticky="ew")
        
        # Configure column weights
        table_frame.grid_columnconfigure(0, weight=2)
        table_frame.grid_columnconfigure(1, weight=1)
        
        # Payment reminder if balance > 0
        if balance > 0:
            reminder_card = self.create_card(page)
            reminder_card.pack(fill=tk.X, pady=(20, 0))
            
            reminder_frame = tk.Frame(reminder_card, bg=COLORS["primary_lighter"])
            reminder_frame.pack(fill=tk.X, padx=20, pady=20)
            
            tk.Label(reminder_frame, text="💡 Reminder", font=FONTS["heading"], 
                    bg=COLORS["primary_lighter"], fg=COLORS["primary"]).pack(anchor=tk.W)
            tk.Label(reminder_frame, text="Please clear your pending balance to avoid additional late fees.", 
                    font=FONTS["normal"], bg=COLORS["primary_lighter"], fg=COLORS["text_secondary"]).pack(anchor=tk.W)
    
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
    
    def get_student_by_user_id(self):
        students = AccountService.get_all_students()
        for student in students:
            if student.get("user_id") == self.user["id"]:
                return student
        return None