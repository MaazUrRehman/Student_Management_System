# fee_view.py
import tkinter as tk
from tkinter import ttk, messagebox

from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class FeeView:
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
        
        tk.Label(header_left, text="💰 Fee Structures", font=FONTS["title"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        tk.Label(header_left, text="Manage class-wise fee structures and amounts.",
                font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W)
        
        if self.user["role"] in ["admin", "accountant"]:
            self.create_button(header, "📊 Dashboard", self.go_dashboard, "outline").pack(side=tk.RIGHT, padx=20, pady=16)

        # Add Fee Form (Admin only)
        if self.user["role"] == "admin":
            form = self.create_card(page)
            form.pack(fill=tk.X, pady=(0, 20))
            
            # Form header
            form_header = tk.Frame(form, bg=COLORS["card"])
            form_header.pack(fill=tk.X, padx=20, pady=(16, 10))
            tk.Label(form_header, text="➕ Add Fee Structure", font=FONTS["heading"], 
                    bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)
            
            # Form fields in a responsive grid
            fields_frame = tk.Frame(form, bg=COLORS["card"])
            fields_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            # Configure grid columns
            for i in range(2):
                fields_frame.grid_columnconfigure(i, weight=1)
            
            # Row 0: Class and Tuition Fee
            # Class
            class_frame = tk.Frame(fields_frame, bg=COLORS["card"])
            class_frame.grid(row=0, column=0, padx=(0, 10), sticky="ew")
            tk.Label(class_frame, text="Class Name", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, pady=(0, 5))
            self.class_entry = self.create_styled_entry(class_frame)
            self.class_entry.pack(fill=tk.X, pady=(0, 10))
            
            # Tuition Fee
            tuition_frame = tk.Frame(fields_frame, bg=COLORS["card"])
            tuition_frame.grid(row=0, column=1, padx=(10, 0), sticky="ew")
            tk.Label(tuition_frame, text="Tuition Fee ($)", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, pady=(0, 5))
            self.tuition_entry = self.create_styled_entry(tuition_frame)
            self.tuition_entry.pack(fill=tk.X, pady=(0, 10))
            
            # Row 1: Exam Fee and Transport Fee
            # Exam Fee
            exam_frame = tk.Frame(fields_frame, bg=COLORS["card"])
            exam_frame.grid(row=1, column=0, padx=(0, 10), sticky="ew", pady=(10, 0))
            tk.Label(exam_frame, text="Exam Fee ($)", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, pady=(0, 5))
            self.exam_entry = self.create_styled_entry(exam_frame)
            self.exam_entry.pack(fill=tk.X, pady=(0, 10))
            
            # Transport Fee
            transport_frame = tk.Frame(fields_frame, bg=COLORS["card"])
            transport_frame.grid(row=1, column=1, padx=(10, 0), sticky="ew", pady=(10, 0))
            tk.Label(transport_frame, text="Transport Fee ($)", font=FONTS["normal"], 
                    bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, pady=(0, 5))
            self.transport_entry = self.create_styled_entry(transport_frame)
            self.transport_entry.pack(fill=tk.X, pady=(0, 10))
            
            # Add button row
            btn_frame = tk.Frame(fields_frame, bg=COLORS["card"])
            btn_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0), sticky="ew")
            self.create_button(btn_frame, "➕ Add Fee Structure", self.add_fee_structure, "success").pack(fill=tk.X)

        # Fee Table - Increased size
        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        
        table_header = tk.Frame(table_card, bg=COLORS["card"])
        table_header.pack(fill=tk.X, padx=20, pady=(16, 10))
        tk.Label(table_header, text="📋 Fee Structure List", font=FONTS["heading"], 
                bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)
        
        # Table Frame
        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))
        
        # Treeview with increased height (15 rows visible, but full scrollable)
        columns = ("ID", "Class", "Tuition Fee", "Exam Fee", "Transport Fee", "Total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                 height=15, style="Modern.Treeview")
        
        # Configure columns with better widths
        column_widths = {"ID": 80, "Class": 180, "Tuition Fee": 140, 
                        "Exam Fee": 130, "Transport Fee": 140, "Total": 140}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 120), anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Bottom action bar
        action_frame = tk.Frame(table_card, bg=COLORS["card"])
        action_frame.pack(fill=tk.X, padx=20, pady=(0, 16))
        
        # Delete button for admin
        if self.user["role"] == "admin":
            self.create_button(action_frame, "🗑️ Delete Selected", self.delete_fee_structure, "danger").pack(side=tk.RIGHT)
        
        # Refresh button
        self.create_button(action_frame, "🔄 Refresh", self.load_fee_structures, "outline").pack(side=tk.RIGHT, padx=(0, 10))
        
        # Load initial data
        self.load_fee_structures()

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
                          relief="flat", bd=0, cursor="hand2", padx=16, pady=10)
        
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
        """Configure treeview styling with proper heading colors"""
        style = ttk.Style()
        style.configure("Modern.Treeview", 
                       background=COLORS["card"], 
                       fieldbackground=COLORS["card"], 
                       foreground=COLORS["text_primary"], 
                       rowheight=35,  # Slightly taller rows for better readability
                       font=FONTS["table_cell"])
        style.configure("Modern.Treeview.Heading", 
                       background=COLORS["primary"], 
                       foreground="#FFFFFF",  # White text for better contrast with blue background
                       font=FONTS["table_header"])
        style.map("Modern.Treeview", 
                 background=[("selected", COLORS["primary_light"])], 
                 foreground=[("selected", COLORS["text_light"])])

    def load_fee_structures(self):
        """Load fee structures into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all fee structures
        fees = AccountService.get_all_fee_structures()
        
        if not fees:
            # Show "No data" message
            self.tree.insert("", tk.END, values=("", "No fee structures found", "", "", "", ""), 
                           tags=("empty",))
            self.tree.tag_configure("empty", background=COLORS["card"], foreground=COLORS["text_muted"])
            return
        
        # Insert data with alternating row colors
        for index, fee in enumerate(fees):
            total = fee["tuition_fee"] + fee["exam_fee"] + fee["transport_fee"]
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(
                fee["id"],
                fee["class_name"],
                f"${fee['tuition_fee']:,.2f}",
                f"${fee['exam_fee']:,.2f}",
                f"${fee['transport_fee']:,.2f}",
                f"${total:,.2f}"
            ), tags=(tag,))
        
        # Configure row colors
        self.tree.tag_configure("evenrow", background=COLORS["card"])
        self.tree.tag_configure("oddrow", background=COLORS["background"])

    def add_fee_structure(self):
        """Add new fee structure with validation"""
        class_name = self.class_entry.get().strip()
        tuition_fee = self.tuition_entry.get().strip()
        exam_fee = self.exam_entry.get().strip() or "0"
        transport_fee = self.transport_entry.get().strip() or "0"

        # Validation
        if not class_name:
            messagebox.showerror("Error", "Class name is required")
            self.class_entry.focus()
            return
        
        if not tuition_fee:
            messagebox.showerror("Error", "Tuition fee is required")
            self.tuition_entry.focus()
            return
        
        try:
            tuition = float(tuition_fee)
            exam = float(exam_fee)
            transport = float(transport_fee)
            
            if tuition < 0 or exam < 0 or transport < 0:
                messagebox.showerror("Error", "Fees cannot be negative")
                return
            
            # Call service to add fee structure
            AccountService.add_fee_structure(class_name, tuition, exam, transport)
            
            messagebox.showinfo("Success", f"Fee structure for '{class_name}' added successfully!")
            
            # Clear form
            self.clear_entries()
            
            # Reload table
            self.load_fee_structures()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for fees")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def delete_fee_structure(self):
        """Delete selected fee structure with confirmation"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a fee structure to delete")
            return
        
        # Get class name for confirmation message
        item = self.tree.item(selected[0])
        class_name = item["values"][1] if len(item["values"]) > 1 else "this"
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete fee structure for '{class_name}'?\nThis action cannot be undone."):
            return

        fee_id = item["values"][0]
        try:
            AccountService.delete_fee_structure(fee_id)
            messagebox.showinfo("Success", "Fee structure deleted successfully!")
            self.load_fee_structures()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def clear_entries(self):
        """Clear all form entries"""
        self.class_entry.delete(0, tk.END)
        self.tuition_entry.delete(0, tk.END)
        self.exam_entry.delete(0, tk.END)
        self.transport_entry.delete(0, tk.END)
        
        # Set focus back to class entry
        self.class_entry.focus()

    def go_dashboard(self):
        """Navigate back to dashboard"""
        if self.switch_callback:
            self.switch_callback("dashboard", self.user)