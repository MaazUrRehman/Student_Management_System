import tkinter as tk
from tkinter import ttk, messagebox

from services.account_service import AccountService
from utils.constants import COLORS, FONTS


class PaymentView:
    def __init__(self, parent, user, switch_callback=None):
        self.parent = parent
        self.user = user
        self.switch_callback = switch_callback
        self.create_ui()

    def create_ui(self):
        self.configure_tree_style()

        # Use parent directly - Dashboard already provides scrollable frame
        page = self.parent

        header = self.create_card(page)
        header.pack(fill=tk.X, pady=(0, 20))

        header_left = tk.Frame(header, bg=COLORS["card"])
        header_left.pack(side=tk.LEFT, padx=20, pady=16)
        tk.Label(header_left, text="Payment Management", font=FONTS["title"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W)
        tk.Label(header_left, text="Track invoice status and payment history in one place", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(anchor=tk.W)

        if self.user["role"] in ["admin", "accountant"]:
            self.create_button(header, "Dashboard", self.go_dashboard, "outline").pack(side=tk.RIGHT, padx=20, pady=16)

        if self.user["role"] in ["admin", "accountant"]:
            form = self.create_card(page)
            form.pack(fill=tk.X, pady=(0, 20))

            form_header = tk.Frame(form, bg=COLORS["card"])
            form_header.pack(fill=tk.X, padx=20, pady=(16, 10))
            tk.Label(form_header, text="Record New Payment", font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(side=tk.LEFT)

            fields = tk.Frame(form, bg=COLORS["card"])
            fields.pack(fill=tk.X, padx=20, pady=(0, 20))
            for index in range(4):
                fields.grid_columnconfigure(index, weight=1)

            tk.Label(fields, text="Invoice ID", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=0, padx=(0, 10), sticky="w")
            self.invoice_id_entry = self.create_styled_entry(fields)
            self.invoice_id_entry.grid(row=1, column=0, padx=(0, 10), sticky="ew", pady=(0, 10))

            tk.Label(fields, text="Amount ($)", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=1, padx=10, sticky="w")
            self.amount_entry = self.create_styled_entry(fields)
            self.amount_entry.grid(row=1, column=1, padx=10, sticky="ew", pady=(0, 10))

            tk.Label(fields, text="Payment Method", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).grid(row=0, column=2, padx=10, sticky="w")
            self.method_var = tk.StringVar(value="cash")
            ttk.Combobox(fields, textvariable=self.method_var, values=["cash", "bank", "card"], width=15, state="readonly", font=FONTS["normal"]).grid(
                row=1, column=2, padx=10, sticky="ew", pady=(0, 10)
            )

            self.create_button(fields, "Record Payment", self.add_payment, "success").grid(row=1, column=3, padx=20, sticky="ew", pady=(0, 10))

        details_card = self.create_card(page)
        details_card.pack(fill=tk.X, pady=(0, 20))
        tk.Label(details_card, text="Invoice Details", font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(16, 10))

        self.details_frame = tk.Frame(details_card, bg=COLORS["primary_lighter"])
        self.details_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.details_label = tk.Label(self.details_frame, text="Showing all recorded payments. Select an invoice to view its details.", font=FONTS["normal"], bg=COLORS["primary_lighter"], fg=COLORS["text_secondary"], justify=tk.LEFT)
        self.details_label.pack(padx=15, pady=15, anchor=tk.W)

        tables_frame = tk.Frame(page, bg=COLORS["background"])
        tables_frame.pack(fill=tk.BOTH, expand=True)
        tables_frame.grid_columnconfigure(0, weight=1)
        tables_frame.grid_columnconfigure(1, weight=1)
        tables_frame.grid_rowconfigure(0, weight=1)

        invoice_card = self.create_card(tables_frame)
        invoice_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        tk.Label(invoice_card, text="Invoices", font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(16, 10))
        self.invoice_tree = self.create_table(invoice_card, ("ID", "Student", "Class", "Total", "Discount", "Final", "Status"), 10)
        self.invoice_tree.bind("<<TreeviewSelect>>", self.on_invoice_select)

        payment_card = self.create_card(tables_frame)
        payment_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        tk.Label(payment_card, text="Payment History", font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(anchor=tk.W, padx=20, pady=(16, 10))
        self.payment_tree = self.create_table(payment_card, ("ID", "Invoice ID", "Amount", "Method", "Date"), 10)

        self.load_invoices()
        self.load_all_payments()

    def create_styled_entry(self, parent):
        return tk.Entry(
            parent,
            font=FONTS["normal"],
            relief="flat",
            bg=COLORS["background"],
            fg=COLORS["text_primary"],
            highlightthickness=1,
            highlightcolor=COLORS["primary"],
            highlightbackground=COLORS["border"]
        )

    def create_card(self, parent):
        return tk.Frame(parent, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)

    def create_button(self, parent, text, command, variant="primary"):
        color_map = {
            "primary": (COLORS["primary"], COLORS["primary_dark"]),
            "secondary": (COLORS["secondary"], COLORS["primary"]),
            "success": (COLORS["success"], "#059669"),
            "danger": (COLORS["danger"], "#DC2626"),
            "outline": (COLORS["card"], COLORS["primary"]),
        }
        bg_color, hover_color = color_map.get(variant, color_map["primary"])
        fg_color = COLORS["text_primary"] if variant == "outline" else COLORS["text_light"]

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=FONTS["button"],
            bg=bg_color,
            fg=fg_color,
            activebackground=hover_color,
            activeforeground=COLORS["text_light"],
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=8
        )
        if variant == "outline":
            button.configure(bg=COLORS["card"], fg=COLORS["primary"], highlightbackground=COLORS["primary"], highlightthickness=1)

        button.bind("<Enter>", lambda _event: button.configure(bg=hover_color, fg=COLORS["text_light"] if variant == "outline" else fg_color))
        button.bind("<Leave>", lambda _event: button.configure(bg=COLORS["card"] if variant == "outline" else bg_color, fg=fg_color))
        return button

    def configure_tree_style(self):
        style = ttk.Style()
        style.configure(
            "Modern.Treeview",
            background=COLORS["card"],
            fieldbackground=COLORS["card"],
            foreground=COLORS["text_primary"],
            rowheight=32,
            font=FONTS["table_cell"]
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=COLORS["table_header"],
            foreground=COLORS["text_primary"],
            font=FONTS["table_header"]
        )
        style.map("Modern.Treeview", background=[("selected", COLORS["primary_light"])], foreground=[("selected", COLORS["text_light"])])

    def create_table(self, parent, columns, height):
        frame = tk.Frame(parent, bg=COLORS["card"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        tree = ttk.Treeview(frame, columns=columns, show="headings", height=height, style="Modern.Treeview")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER if col != "Student" else tk.W)

        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        return tree

    def load_invoices(self):
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)

        invoices = sorted(AccountService.get_all_invoices(), key=lambda inv: inv.get("id", 0))
        for idx, inv in enumerate(invoices):
            status = (inv.get("status") or "").upper()
            tag = "paid" if status == "PAID" else "overdue" if status == "OVERDUE" else "normal"
            self.invoice_tree.insert("", tk.END, values=(
                inv["id"],
                inv.get("student_name", "N/A"),
                inv.get("class_name", "N/A"),
                f"${inv['total_amount']:.2f}",
                f"${inv['discount_amount']:.2f}",
                f"${inv['final_amount']:.2f}",
                status or "-"
            ), tags=(tag,))

        self.invoice_tree.tag_configure("paid", background=COLORS["status_paid"])
        self.invoice_tree.tag_configure("overdue", background=COLORS["status_overdue"])
        self.invoice_tree.tag_configure("normal", background=COLORS["card"])

    def on_invoice_select(self, _event):
        selected = self.invoice_tree.selection()
        if not selected:
            return
        invoice_id = self.invoice_tree.item(selected[0])["values"][0]
        self.show_invoice_details(invoice_id)
        self.load_payments(invoice_id)

    def show_invoice_details(self, invoice_id):
        fee_info = AccountService.calculate_late_fee(invoice_id)
        if not fee_info:
            self.details_label.config(text="Invoice not found", fg=COLORS["danger"])
            return

        status_color = COLORS["danger"] if fee_info["is_overdue"] else COLORS["success"]
        details_text = (
            f"Invoice #{invoice_id}\n\n"
            f"Original Amount: ${fee_info['original_amount']:,.2f}\n"
            f"Total Paid: ${fee_info['total_paid']:,.2f}\n"
            f"Late Fee: ${fee_info['late_fee']:,.2f}\n"
            f"Total Payable: ${fee_info['total_payable']:,.2f}\n"
            f"Status: {(fee_info.get('status') or '').upper()}\n"
            f"Due Date: {fee_info.get('due_date') or '-'}"
        )
        self.details_label.config(text=details_text, fg=status_color, justify=tk.LEFT)

    def load_payments(self, invoice_id):
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        payments = sorted(AccountService.get_invoice_payments(invoice_id), key=lambda payment: payment.get("id", 0))
        for idx, payment in enumerate(payments):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.payment_tree.insert("", tk.END, values=(
                payment["id"],
                payment["invoice_id"],
                f"${payment['amount_paid']:.2f}",
                (payment.get("payment_method") or "").upper(),
                payment.get("payment_date") or "-"
            ), tags=(tag,))

        self.payment_tree.tag_configure("evenrow", background=COLORS["card"])
        self.payment_tree.tag_configure("oddrow", background=COLORS["background"])

    def load_all_payments(self):
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        payments = sorted(AccountService.get_all_payments(), key=lambda payment: payment.get("id", 0))
        for idx, payment in enumerate(payments):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.payment_tree.insert("", tk.END, values=(
                payment["id"],
                payment["invoice_id"],
                f"${payment['amount_paid']:.2f}",
                (payment.get("payment_method") or "").upper(),
                payment.get("payment_date") or "-"
            ), tags=(tag,))

        self.payment_tree.tag_configure("evenrow", background=COLORS["card"])
        self.payment_tree.tag_configure("oddrow", background=COLORS["background"])

    def add_payment(self):
        invoice_id = self.invoice_id_entry.get().strip()
        amount = self.amount_entry.get().strip()
        if not invoice_id or not amount:
            messagebox.showerror("Error", "Invoice ID and Amount are required")
            return

        try:
            AccountService.add_payment(int(invoice_id), float(amount), self.method_var.get())
            messagebox.showinfo("Success", "Payment recorded successfully!")
            self.invoice_id_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.load_invoices()
            self.load_all_payments()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def go_dashboard(self):
        if self.switch_callback:
            self.switch_callback("dashboard", self.user)
