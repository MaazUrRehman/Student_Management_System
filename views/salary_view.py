import tkinter as tk
from tkinter import ttk, messagebox

from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class SalaryView:
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.create_ui()

    def create_ui(self):
        self.configure_tree_style()

        # Use parent directly - Dashboard already provides scrollable frame
        page = self.parent

        header = self.create_card(page)
        header.pack(fill=tk.X, pady=(0, 20))
        tk.Label(header, text="Staff Salaries", font=FONTS["title"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(20, 5))
        tk.Label(header, text="Manage monthly salary records and payments", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W, padx=20, pady=(0, 20))

        controls_card = self.create_card(page)
        controls_card.pack(fill=tk.X, pady=(0, 20))
        controls_inner = tk.Frame(controls_card, bg=COLORS["card"])
        controls_inner.pack(fill=tk.X, padx=20, pady=16)

        # Row 1: Month input and buttons
        row1 = tk.Frame(controls_inner, bg=COLORS["card"])
        row1.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(row1, text="Month (YYYY-MM):", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT, padx=(0, 10))
        self.month_entry = self.create_styled_entry(row1, width=12)
        self.month_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.create_button(row1, "Generate", self.generate_records, "success").pack(side=tk.LEFT, padx=5)
        self.create_button(row1, "Filter", self.filter_by_month, "secondary").pack(side=tk.LEFT, padx=5)
        self.create_button(row1, "Show All", self.load_records, "primary").pack(side=tk.LEFT, padx=5)

        # Row 2: Payment method and Mark Paid button
        row2 = tk.Frame(controls_inner, bg=COLORS["card"])
        row2.pack(fill=tk.X)
        
        tk.Label(row2, text="Payment Method:", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT, padx=(0, 10))

        self.method_var = tk.StringVar(value="cash")
        ttk.Combobox(row2, textvariable=self.method_var, values=["cash", "bank", "card"], width=10, state="readonly", font=FONTS["normal"]).pack(side=tk.LEFT, padx=(0, 10))
        
        self.create_button(row2, "Mark Selected Paid", self.pay_selected_salary, "danger").pack(side=tk.LEFT, padx=5)

        table_card = self.create_card(page)
        table_card.pack(fill=tk.BOTH, expand=True)
        tk.Label(table_card, text="Salary Records", font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(16, 10))

        table_frame = tk.Frame(table_card, bg=COLORS["card"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "Staff", "Department", "Designation", "Month", "Amount", "Due Date", "Status", "Method")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12, style="Modern.Treeview")
        widths = {"ID": 60, "Staff": 160, "Department": 120, "Designation": 120, "Month": 100, "Amount": 120, "Due Date": 110, "Status": 100, "Method": 100}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 100), anchor=tk.CENTER)

        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.load_records()

    def create_styled_entry(self, parent, width=None):
        return tk.Entry(parent, font=FONTS["normal"], relief="flat", width=width, bg=COLORS["background"], fg=COLORS["text_primary"], highlightthickness=1, highlightcolor=COLORS["primary"], highlightbackground=COLORS["border"])

    def create_card(self, parent):
        return tk.Frame(parent, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)

    def create_button(self, parent, text, command, variant="primary"):
        color_map = {
            "primary": (COLORS["primary"], COLORS["primary_dark"]),
            "secondary": (COLORS["secondary"], COLORS["primary"]),
            "success": (COLORS["success"], "#059669"),
            "danger": (COLORS["danger"], "#DC2626"),
        }
        bg_color, hover_color = color_map.get(variant, color_map["primary"])
        button = tk.Button(parent, text=text, command=command, font=FONTS["button"], bg=bg_color, fg=COLORS["text_light"], activebackground=hover_color, activeforeground=COLORS["text_light"], relief="flat", bd=0, cursor="hand2", padx=12, pady=6)
        button.bind("<Enter>", lambda _event: button.configure(bg=hover_color))
        button.bind("<Leave>", lambda _event: button.configure(bg=bg_color))
        return button

    def configure_tree_style(self):
        style = ttk.Style()
        style.configure("Modern.Treeview", background=COLORS["card"], fieldbackground=COLORS["card"], foreground=COLORS["text_primary"], rowheight=32, font=FONTS["table_cell"])
        style.configure("Modern.Treeview.Heading", background=COLORS["table_header"], foreground=COLORS["text_primary"], font=FONTS["table_header"])
        style.map("Modern.Treeview", background=[("selected", COLORS["primary_light"])], foreground=[("selected", COLORS["text_light"])])

    def load_records(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = records if records is not None else AccountService.get_all_salary_records()
        records = sorted(records, key=lambda record: record.get("id", 0))

        for idx, record in enumerate(records):
            status = (record.get("status") or "").upper()
            if status == "PAID":
                tag = "paid"
                status_display = "PAID"
            elif status == "LATE":
                tag = "late"
                status_display = "LATE"
            else:
                tag = "pending"
                status_display = "PENDING"

            self.tree.insert("", tk.END, values=(
                record["id"],
                record.get("staff_name", "N/A"),
                record.get("department") or "-",
                record.get("designation") or "-",
                record.get("month") or "-",
                f"${record['salary_amount']:.2f}",
                record.get("due_date") or "-",
                status_display,
                (record.get("payment_method") or "-").upper()
            ), tags=(tag,))

        self.tree.tag_configure("paid", background=COLORS["status_paid"])
        self.tree.tag_configure("pending", background=COLORS["status_pending"])
        self.tree.tag_configure("late", background=COLORS["status_overdue"])

    def generate_records(self):
        month = self.month_entry.get().strip()
        if not month:
            messagebox.showerror("Error", "Please enter a month in YYYY-MM format")
            return

        try:
            created = AccountService.generate_monthly_salary_records(month)
            if created:
                messagebox.showinfo("Success", f"Generated {len(created)} salary record(s)")
            else:
                messagebox.showinfo("Info", "No records generated. They may already exist for this month.")
            self.filter_by_month()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def filter_by_month(self):
        month = self.month_entry.get().strip()
        if not month:
            self.load_records()
            return

        try:
            self.load_records(AccountService.get_salary_by_month(month))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def pay_selected_salary(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a salary record")
            return

        item = self.tree.item(selected[0])
        salary_id = item["values"][0]
        status = str(item["values"][7] or "")
        if "PAID" in status:
            messagebox.showinfo("Info", "This salary has already been paid")
            return

        try:
            AccountService.pay_salary(salary_id, self.method_var.get())
            messagebox.showinfo("Success", "Salary payment recorded successfully!")
            self.filter_by_month()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
