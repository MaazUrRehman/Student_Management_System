# import tkinter as tk
# from tkinter import messagebox, ttk

# import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure

# from services.account_service import AccountService
# from utils.constants import COLORS, DIMENSIONS, FONTS


# class ScrollableFrame(tk.Frame):
#     def __init__(self, parent, bg=None):
#         super().__init__(parent, bg=bg or COLORS["background"])
#         self.canvas = tk.Canvas(self, bg=bg or COLORS["background"], highlightthickness=0)
#         self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
#         self.content = tk.Frame(self.canvas, bg=bg or COLORS["background"])

#         self.content.bind("<Configure>", lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
#         self.canvas.create_window((0, 0), window=self.content, anchor="nw")
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)

#         self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#         self.canvas.bind("<Enter>", self.bind_mousewheel)
#         self.canvas.bind("<Leave>", self.unbind_mousewheel)

#     def bind_mousewheel(self, _event=None):
#         self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

#     def unbind_mousewheel(self, _event=None):
#         self.canvas.unbind_all("<MouseWheel>")

#     def on_mousewheel(self, event):
#         self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

#     def get_content_frame(self):
#         return self.content


# class Dashboard:
#     def __init__(self, root, user, switch_callback):
#         self.root = root
#         self.user = user
#         self.switch_callback = switch_callback
#         self.frame = None
#         self.sidebar_canvas = None
#         self.content_frame = None
#         self.create_ui()

#     def create_ui(self):
#         self.frame = tk.Frame(self.root, bg=COLORS["background"])
#         self.frame.pack(fill=tk.BOTH, expand=True)

#         self.create_header()

#         main_container = tk.Frame(self.frame, bg=COLORS["background"])
#         main_container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
#         main_container.grid_columnconfigure(1, weight=1)
#         main_container.grid_rowconfigure(0, weight=1)

#         self.create_sidebar(main_container)

#         self.content_frame = tk.Frame(main_container, bg=COLORS["background"])
#         self.content_frame.grid(row=0, column=1, sticky="nsew")

#         self.show_welcome()

#     def create_header(self):
#         header = tk.Frame(self.frame, bg=COLORS["primary_dark"], height=DIMENSIONS["header_height"])
#         header.pack(fill=tk.X)
#         header.pack_propagate(False)

#         left = tk.Frame(header, bg=COLORS["primary_dark"])
#         left.pack(side=tk.LEFT, fill=tk.Y, padx=20)
#         tk.Label(
#             left,
#             text="Student Management System",
#             font=FONTS["title"],
#             bg=COLORS["primary_dark"],
#             fg=COLORS["text_light"]
#         ).pack(anchor=tk.W, pady=(12, 0))
#         tk.Label(
#             left,
#             text="Manage students, finance, staff, and reports",
#             font=FONTS["small"],
#             bg=COLORS["primary_dark"],
#             fg="#DDE7FF"
#         ).pack(anchor=tk.W)

#         right = tk.Frame(header, bg=COLORS["primary_dark"])
#         right.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
#         tk.Label(
#             right,
#             text=self.user["username"],
#             font=FONTS["heading"],
#             bg=COLORS["primary_dark"],
#             fg=COLORS["text_light"]
#         ).pack(anchor=tk.E, pady=(12, 0))
#         tk.Label(
#             right,
#             text=self.user["role"].capitalize(),
#             font=FONTS["small"],
#             bg=COLORS["primary_dark"],
#             fg="#DDE7FF"
#         ).pack(anchor=tk.E)

#     def create_sidebar(self, parent):
#         sidebar_outer = tk.Frame(parent, bg=COLORS["sidebar"], width=DIMENSIONS["sidebar_width"])
#         sidebar_outer.grid(row=0, column=0, sticky="ns", padx=(0, 16))
#         sidebar_outer.grid_propagate(False)
#         sidebar_outer.grid_rowconfigure(1, weight=1)
#         sidebar_outer.grid_columnconfigure(0, weight=1)

#         top = tk.Frame(sidebar_outer, bg=COLORS["sidebar"])
#         top.grid(row=0, column=0, sticky="ew")
#         tk.Label(top, text="Navigation", font=FONTS["heading"], bg=COLORS["sidebar"], fg=COLORS["text_light"]).pack(
#             anchor=tk.W, padx=16, pady=(16, 4)
#         )
#         tk.Label(
#             top,
#             text="Quick access to your modules",
#             font=FONTS["small"],
#             bg=COLORS["sidebar"],
#             fg=COLORS["text_muted"]
#         ).pack(anchor=tk.W, padx=16, pady=(0, 10))

#         scroll_wrap = tk.Frame(sidebar_outer, bg=COLORS["sidebar"])
#         scroll_wrap.grid(row=1, column=0, sticky="nsew")
#         scroll_wrap.grid_rowconfigure(0, weight=1)
#         scroll_wrap.grid_columnconfigure(0, weight=1)

#         self.sidebar_canvas = tk.Canvas(scroll_wrap, bg=COLORS["sidebar"], highlightthickness=0, width=DIMENSIONS["sidebar_width"] - 10)
#         sidebar_scroll = ttk.Scrollbar(scroll_wrap, orient="vertical", command=self.sidebar_canvas.yview)
#         self.sidebar_inner = tk.Frame(self.sidebar_canvas, bg=COLORS["sidebar"])
#         self.sidebar_inner.bind(
#             "<Configure>",
#             lambda _event: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all"))
#         )
#         self.sidebar_canvas.create_window((0, 0), window=self.sidebar_inner, anchor="nw")
#         self.sidebar_canvas.configure(yscrollcommand=sidebar_scroll.set)
#         self.sidebar_canvas.grid(row=0, column=0, sticky="nsew")
#         sidebar_scroll.grid(row=0, column=1, sticky="ns")

#         for text, command in self.get_menu_items():
#             self.create_sidebar_button(self.sidebar_inner, text, command)

#         bottom = tk.Frame(sidebar_outer, bg=COLORS["sidebar"])
#         bottom.grid(row=2, column=0, sticky="ew", pady=(8, 12))
#         self.create_sidebar_button(bottom, "Logout", self.on_logout, is_logout=True).pack(fill=tk.X, padx=12)

#     def get_menu_items(self):
#         role = self.user["role"]
#         if role == "admin":
#             return [
#                 ("Dashboard", self.show_welcome),
#                 ("Students", self.show_students),
#                 ("Staff", self.show_staff),
#                 ("Fees", self.show_fees),
#                 ("Payments", self.show_payments),
#                 ("Salaries", self.show_salaries),
#                 ("Expenses", self.show_expenses),
#                 ("Reports", self.show_reports),
#                 ("Register User", self.show_register),
#             ]
#         if role == "accountant":
#             return [
#                 ("Dashboard", self.show_welcome),
#                 ("Students", self.show_students),
#                 ("Staff", self.show_staff),
#                 ("Fees", self.show_fees),
#                 ("Payments", self.show_payments),
#                 ("Salaries", self.show_salaries),
#                 ("Expenses", self.show_expenses),
#                 ("Reports", self.show_reports),
#             ]
#         if role == "staff":
#             return [
#                 ("Dashboard", self.show_welcome),
#                 ("My Profile", self.show_my_profile),
#                 ("My Salary", self.show_my_salary),
#             ]
#         return [
#             ("Dashboard", self.show_welcome),
#             ("My Profile", self.show_my_profile),
#             ("My Fees", self.show_my_fees),
#             ("My Payments", self.show_my_payments),
#             ("My Balance", self.show_my_balance),
#         ]

#     def create_sidebar_button(self, parent, text, command, is_logout=False):
#         base_bg = COLORS["danger"] if is_logout else COLORS["sidebar"]
#         hover_bg = "#DC2626" if is_logout else COLORS["primary"]
#         button = tk.Label(
#             parent,
#             text=text,
#             font=FONTS["normal"],
#             bg=base_bg,
#             fg=COLORS["text_light"],
#             cursor="hand2",
#             padx=14,
#             pady=10,
#             anchor=tk.W
#         )
#         button.bind("<Enter>", lambda _event: button.configure(bg=hover_bg))
#         button.bind("<Leave>", lambda _event: button.configure(bg=base_bg))
#         button.bind("<Button-1>", lambda _event: command())
#         if parent is self.sidebar_inner:
#             button.pack(fill=tk.X, padx=12, pady=4)
#             return button
#         return button

#     def clear_content(self):
#         for widget in self.content_frame.winfo_children():
#             widget.destroy()

#     def create_card(self, parent):
#         return tk.Frame(
#             parent,
#             bg=COLORS["card"],
#             highlightbackground=COLORS["border"],
#             highlightthickness=1
#         )

#     def show_welcome(self):
#         self.clear_content()
#         if self.user["role"] in ["admin", "accountant"]:
#             self.show_admin_accountant_dashboard()
#         else:
#             self.show_simple_role_dashboard()

#     def show_admin_accountant_dashboard(self):
#         scrollable = ScrollableFrame(self.content_frame)
#         scrollable.pack(fill=tk.BOTH, expand=True)
#         page = scrollable.get_content_frame()

#         summary = AccountService.get_financial_summary()
#         trend = AccountService.get_monthly_trend_data(12)
#         expense_breakdown = AccountService.get_expense_distribution()

#         header = self.create_card(page)
#         header.pack(fill=tk.X, pady=(0, 16))
#         tk.Label(header, text=f"Welcome back, {self.user['username']}", font=FONTS["title"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(
#             anchor=tk.W, padx=20, pady=(18, 6)
#         )
#         tk.Label(header, text="Here is your institution overview and monthly financial trend.", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
#             anchor=tk.W, padx=20, pady=(0, 18)
#         )

#         stats = tk.Frame(page, bg=COLORS["background"])
#         stats.pack(fill=tk.X, pady=(0, 16))
#         for index in range(4):
#             stats.grid_columnconfigure(index, weight=1)

#         cards = [
#             ("Total Students", str(len(AccountService.get_all_students())), COLORS["primary"]),
#             ("Total Income", f"${summary['total_income']:,.2f}", COLORS["success"]),
#             ("Total Expenses", f"${summary['total_expenses']:,.2f}", COLORS["danger"]),
#             ("Pending Fees", f"${summary['pending_fees']:,.2f}", COLORS["secondary"]),
#         ]
#         for col, (title, value, color) in enumerate(cards):
#             self.create_stat_card(stats, title, value, color, 0, col)

#         chart_grid = tk.Frame(page, bg=COLORS["background"])
#         chart_grid.pack(fill=tk.BOTH, expand=True)
#         chart_grid.grid_columnconfigure(0, weight=1)
#         chart_grid.grid_columnconfigure(1, weight=1)

#         self.create_income_expense_chart(chart_grid, trend, 0, 0)
#         self.create_expense_breakdown_chart(chart_grid, expense_breakdown, 0, 1)

#     def show_simple_role_dashboard(self):
#         scrollable = ScrollableFrame(self.content_frame)
#         scrollable.pack(fill=tk.BOTH, expand=True)
#         page = scrollable.get_content_frame()
#         header = self.create_card(page)
#         header.pack(fill=tk.X, pady=(0, 16))
#         name = self.user["username"]
#         subtitle = "Use the menu on the left to access your dashboard features."
#         if self.user["role"] == "student":
#             summary = AccountService.get_student_dashboard_summary(self.user["id"])
#             if summary and summary.get("student"):
#                 name = summary["student"].get("name") or name
#             subtitle = "Use the menu on the left to view your profile, fees, payments, and balance."
#         elif self.user["role"] == "staff":
#             summary = AccountService.get_staff_dashboard_summary(self.user["id"])
#             if summary and summary.get("staff"):
#                 name = summary["staff"].get("name") or name
#             subtitle = "Use the menu on the left to view your profile and salary details."

#         tk.Label(header, text=f"Welcome, {name}", font=FONTS["title"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(
#             anchor=tk.W, padx=20, pady=(18, 6)
#         )
#         tk.Label(header, text=subtitle, font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
#             anchor=tk.W, padx=20, pady=(0, 18)
#         )

#     def show_empty_role_card(self, page, text):
#         card = self.create_card(page)
#         card.pack(fill=tk.X, pady=16)
#         tk.Label(card, text=text, font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["danger"]).pack(padx=20, pady=40)

#     def create_stat_card(self, parent, title, value, color, row, col):
#         card = self.create_card(parent)
#         card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
#         tk.Label(card, text=title, font=FONTS["small"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
#             anchor=tk.W, padx=16, pady=(14, 6)
#         )
#         tk.Label(card, text=value, font=(FONTS["title"][0], 18, "bold"), bg=COLORS["card"], fg=color).pack(
#             anchor=tk.W, padx=16, pady=(0, 16)
#         )

#     def create_chart_card(self, parent, title, row, col):
#         card = self.create_card(parent)
#         card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
#         tk.Label(card, text=title, font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(
#             anchor=tk.W, padx=20, pady=(16, 10)
#         )
#         return card

#     def create_income_expense_chart(self, parent, trend_data, row, col):
#         card = self.create_chart_card(parent, "Income vs Expense Trend", row, col)
#         months = trend_data["months"]
#         income = trend_data["income"]
#         expense = trend_data["expense"]

#         if not any(income) and not any(expense):
#             tk.Label(card, text="No data available", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
#                 pady=70
#             )
#             return

#         fig = Figure(figsize=(5.5, 3.5), facecolor=COLORS["card"])
#         ax = fig.add_subplot(111)
#         ax.plot(months, income, marker="o", linewidth=2.2, color=COLORS["success"], label="Income")
#         ax.plot(months, expense, marker="o", linewidth=2.2, color=COLORS["danger"], label="Expense")
#         ax.set_title("Income vs Expense Trend", fontsize=10)
#         ax.set_facecolor(COLORS["card"])
#         ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.35)
#         ax.legend(fontsize=8)
#         ax.tick_params(axis="x", rotation=35, labelsize=8)
#         ax.tick_params(axis="y", labelsize=8)
#         fig.tight_layout(pad=2)

#         canvas = FigureCanvasTkAgg(fig, master=card)
#         canvas.draw()
#         canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

#     def create_expense_breakdown_chart(self, parent, expense_data, row, col):
#         card = self.create_chart_card(parent, "Expense Breakdown", row, col)

#         buckets = {"Salary": 0, "Rent": 0, "Bills": 0, "Others": 0}
#         for category, amount in expense_data.items():
#             name = str(category).strip().lower()
#             if name == "salary":
#                 buckets["Salary"] += amount
#             elif name == "rent":
#                 buckets["Rent"] += amount
#             elif name == "bills":
#                 buckets["Bills"] += amount
#             else:
#                 buckets["Others"] += amount

#         labels = list(buckets.keys())
#         values = list(buckets.values())
#         if not any(values):
#             tk.Label(card, text="No data available", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
#                 pady=70
#             )
#             return

#         fig = Figure(figsize=(5.5, 3.5), facecolor=COLORS["card"])
#         ax = fig.add_subplot(111)
#         bars = ax.barh(labels, values, color=[COLORS["primary"], COLORS["secondary"], COLORS["success"], COLORS["danger"]])
#         ax.set_facecolor(COLORS["card"])
#         ax.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.35)
#         ax.tick_params(axis="x", labelsize=8)
#         ax.tick_params(axis="y", labelsize=9)
#         for bar, value in zip(bars, values):
#             ax.text(value + (max(values) * 0.01 if max(values) else 0.5), bar.get_y() + bar.get_height() / 2, f"${value:,.0f}", va="center", fontsize=8)
#         fig.tight_layout(pad=2)

#         canvas = FigureCanvasTkAgg(fig, master=card)
#         canvas.draw()
#         canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

#     def create_simple_table(self, parent, columns, rows, empty_message="No data available."):
#         container = tk.Frame(parent, bg=COLORS["card"])
#         container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

#         if not rows:
#             tk.Label(container, text=empty_message, font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
#                 pady=30
#             )
#             return None

#         style = ttk.Style()
#         style.configure("Dashboard.Treeview", rowheight=30, font=FONTS["small"])
#         style.configure(
#             "Dashboard.Treeview.Heading",
#             font=FONTS["heading"],
#             background=COLORS["table_header"],
#             foreground=COLORS["text_primary"]
#         )

#         table = ttk.Treeview(container, columns=columns, show="headings", height=min(len(rows), 6), style="Dashboard.Treeview")
#         for col in columns:
#             table.heading(col, text=col)
#             table.column(col, width=120, anchor=tk.CENTER if col not in ("Description", "Date") else tk.W)

#         yscroll = ttk.Scrollbar(container, orient="vertical", command=table.yview)
#         xscroll = ttk.Scrollbar(container, orient="horizontal", command=table.xview)
#         table.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
#         table.grid(row=0, column=0, sticky="nsew")
#         yscroll.grid(row=0, column=1, sticky="ns")
#         xscroll.grid(row=1, column=0, sticky="ew")
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         for idx, row_data in enumerate(rows):
#             tag = "evenrow" if idx % 2 == 0 else "oddrow"
#             table.insert("", tk.END, values=row_data, tags=(tag,))
#         table.tag_configure("evenrow", background=COLORS["table_row_even"])
#         table.tag_configure("oddrow", background=COLORS["table_row_odd"])
#         return table

#     def show_students(self):
#         self.clear_content()
#         from views.student_view import StudentView
#         StudentView(self.content_frame, self.user, self.switch_callback)

#     def show_fees(self):
#         self.clear_content()
#         from views.fee_view import FeeView
#         FeeView(self.content_frame, self.user, self.switch_callback)

#     def show_staff(self):
#         self.clear_content()
#         from views.staff_view import StaffView
#         StaffView(self.content_frame, self.user, self.switch_callback)

#     def show_payments(self):
#         self.clear_content()
#         from views.payment_view import PaymentView
#         PaymentView(self.content_frame, self.user, self.switch_callback)

#     def show_salaries(self):
#         self.clear_content()
#         from views.salary_view import SalaryView
#         SalaryView(self.content_frame, self.user)

#     def show_expenses(self):
#         self.clear_content()
#         from views.expense_view import ExpenseView
#         ExpenseView(self.content_frame, self.user, self.switch_callback)

#     def show_reports(self):
#         self.clear_content()
#         from views.report_view import ReportView
#         ReportView(self.content_frame, self.user, self.switch_callback)

#     def show_register(self):
#         if self.user["role"] != "admin":
#             messagebox.showerror("Access Denied", "Only admins are allowed to register users.")
#             return
#         self.clear_content()
#         from views.register_view import RegisterView
#         RegisterView(self.content_frame, self.switch_callback, self.user)

#     def show_my_profile(self):
#         self.clear_content()
#         from views.my_profile_view import MyProfileView
#         MyProfileView(self.content_frame, self.user)

#     def show_my_fees(self):
#         self.clear_content()
#         from views.my_fees_view import MyFeesView
#         MyFeesView(self.content_frame, self.user)

#     def show_my_payments(self):
#         self.clear_content()
#         from views.my_payments_view import MyPaymentsView
#         MyPaymentsView(self.content_frame, self.user)

#     def show_my_balance(self):
#         self.clear_content()
#         from views.my_balance_view import MyBalanceView
#         MyBalanceView(self.content_frame, self.user)

#     def show_my_salary(self):
#         self.clear_content()
#         from views.my_salary_view import MySalaryView
#         MySalaryView(self.content_frame, self.user)

#     def on_logout(self):
#         if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
#             self.switch_callback("home")

#     def destroy(self):
#         if self.frame:
#             self.frame.destroy()

















import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from services.account_service import AccountService
from utils.constants import COLORS, DIMENSIONS, FONTS


class ScrollableFrame(tk.Frame):
    """Scrollable frame with both vertical and horizontal scrolling"""
    def __init__(self, parent, bg=None):
        super().__init__(parent, bg=bg or COLORS["background"])
        
        # Create canvas with both scrollbars
        self.canvas = tk.Canvas(self, bg=bg or COLORS["background"], highlightthickness=0)
        
        # Vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        # Horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Content frame
        self.content = tk.Frame(self.canvas, bg=bg or COLORS["background"])
        
        # Bind events
        self.content.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Create window in canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        
        # Pack scrollbars and canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Bind mousewheel for vertical scroll
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        
        # Bind shift+mousewheel for horizontal scroll
        self.canvas.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
    
    def _on_frame_configure(self, event=None):
        """Update scroll region when frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Update canvas window width when canvas resizes"""
        if event.width > 0:
            self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def _bind_mousewheel(self, event=None):
        """Bind mousewheel for vertical scrolling"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event=None):
        """Unbind mousewheel"""
        self.canvas.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event):
        """Handle vertical mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _on_shift_mousewheel(self, event):
        """Handle horizontal mousewheel scrolling (Shift + Wheel)"""
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def get_content_frame(self):
        """Return the content frame where widgets should be placed"""
        return self.content


class Dashboard:
    def __init__(self, root, user, switch_callback):
        self.root = root
        self.user = user
        self.switch_callback = switch_callback
        self.frame = None
        self.sidebar_canvas = None
        self.content_frame = None
        self.content_scrollable = None
        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root, bg=COLORS["background"])
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_header()

        main_container = tk.Frame(self.frame, bg=COLORS["background"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        self.create_sidebar(main_container)

        # Content area with scrollable frame
        self.content_container = tk.Frame(main_container, bg=COLORS["background"])
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for content
        self.content_scrollable = ScrollableFrame(self.content_container, bg=COLORS["background"])
        self.content_scrollable.grid(row=0, column=0, sticky="nsew")
        self.content_frame = self.content_scrollable.get_content_frame()

        self.show_welcome()

    def create_header(self):
        header = tk.Frame(self.frame, bg=COLORS["primary_dark"], height=DIMENSIONS["header_height"])
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        left = tk.Frame(header, bg=COLORS["primary_dark"])
        left.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        tk.Label(
            left,
            text="Student Management System",
            font=FONTS["title"],
            bg=COLORS["primary_dark"],
            fg=COLORS["text_light"]
        ).pack(anchor=tk.W, pady=(12, 0))
        tk.Label(
            left,
            text="Manage students, finance, staff, and reports",
            font=FONTS["small"],
            bg=COLORS["primary_dark"],
            fg="#DDE7FF"
        ).pack(anchor=tk.W)

        right = tk.Frame(header, bg=COLORS["primary_dark"])
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        tk.Label(
            right,
            text=self.user["username"],
            font=FONTS["heading"],
            bg=COLORS["primary_dark"],
            fg=COLORS["text_light"]
        ).pack(anchor=tk.E, pady=(12, 0))
        tk.Label(
            right,
            text=self.user["role"].capitalize(),
            font=FONTS["small"],
            bg=COLORS["primary_dark"],
            fg="#DDE7FF"
        ).pack(anchor=tk.E)

    def create_sidebar(self, parent):
        sidebar_outer = tk.Frame(parent, bg=COLORS["sidebar"], width=DIMENSIONS["sidebar_width"])
        sidebar_outer.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        sidebar_outer.grid_propagate(False)
        sidebar_outer.grid_rowconfigure(1, weight=1)
        sidebar_outer.grid_columnconfigure(0, weight=1)

        top = tk.Frame(sidebar_outer, bg=COLORS["sidebar"])
        top.grid(row=0, column=0, sticky="ew")
        tk.Label(top, text="Navigation", font=FONTS["heading"], bg=COLORS["sidebar"], fg=COLORS["text_light"]).pack(
            anchor=tk.W, padx=16, pady=(16, 4)
        )
        tk.Label(
            top,
            text="Quick access to your modules",
            font=FONTS["small"],
            bg=COLORS["sidebar"],
            fg=COLORS["text_muted"]
        ).pack(anchor=tk.W, padx=16, pady=(0, 10))

        scroll_wrap = tk.Frame(sidebar_outer, bg=COLORS["sidebar"])
        scroll_wrap.grid(row=1, column=0, sticky="nsew")
        scroll_wrap.grid_rowconfigure(0, weight=1)
        scroll_wrap.grid_columnconfigure(0, weight=1)

        self.sidebar_canvas = tk.Canvas(scroll_wrap, bg=COLORS["sidebar"], highlightthickness=0, width=DIMENSIONS["sidebar_width"] - 10)
        sidebar_scroll = ttk.Scrollbar(scroll_wrap, orient="vertical", command=self.sidebar_canvas.yview)
        self.sidebar_inner = tk.Frame(self.sidebar_canvas, bg=COLORS["sidebar"])
        self.sidebar_inner.bind(
            "<Configure>",
            lambda _event: self.sidebar_canvas.configure(scrollregion=self.sidebar_canvas.bbox("all"))
        )
        self.sidebar_canvas.create_window((0, 0), window=self.sidebar_inner, anchor="nw")
        self.sidebar_canvas.configure(yscrollcommand=sidebar_scroll.set)
        self.sidebar_canvas.grid(row=0, column=0, sticky="nsew")
        sidebar_scroll.grid(row=0, column=1, sticky="ns")

        for text, command in self.get_menu_items():
            self.create_sidebar_button(self.sidebar_inner, text, command)

        bottom = tk.Frame(sidebar_outer, bg=COLORS["sidebar"])
        bottom.grid(row=2, column=0, sticky="ew", pady=(8, 12))
        self.create_sidebar_button(bottom, "Logout", self.on_logout, is_logout=True).pack(fill=tk.X, padx=12)

    def get_menu_items(self):
        role = self.user["role"]
        if role == "admin":
            return [
                ("Dashboard", self.show_welcome),
                ("Students", self.show_students),
                ("Staff", self.show_staff),
                ("Fees", self.show_fees),
                ("Payments", self.show_payments),
                ("Salaries", self.show_salaries),
                ("Expenses", self.show_expenses),
                ("Reports", self.show_reports),
                ("Register User", self.show_register),
            ]
        if role == "accountant":
            return [
                ("Dashboard", self.show_welcome),
                ("Students", self.show_students),
                ("Staff", self.show_staff),
                ("Fees", self.show_fees),
                ("Payments", self.show_payments),
                ("Salaries", self.show_salaries),
                ("Expenses", self.show_expenses),
                ("Reports", self.show_reports),
            ]
        if role == "staff":
            return [
                ("Dashboard", self.show_welcome),
                ("My Profile", self.show_my_profile),
                ("My Salary", self.show_my_salary),
            ]
        return [
            ("Dashboard", self.show_welcome),
            ("My Profile", self.show_my_profile),
            ("My Fees", self.show_my_fees),
            ("My Payments", self.show_my_payments),
            ("My Balance", self.show_my_balance),
        ]

    def create_sidebar_button(self, parent, text, command, is_logout=False):
        base_bg = COLORS["danger"] if is_logout else COLORS["sidebar"]
        hover_bg = "#DC2626" if is_logout else COLORS["primary"]
        button = tk.Label(
            parent,
            text=text,
            font=FONTS["normal"],
            bg=base_bg,
            fg=COLORS["text_light"],
            cursor="hand2",
            padx=14,
            pady=10,
            anchor=tk.W
        )
        button.bind("<Enter>", lambda _event: button.configure(bg=hover_bg))
        button.bind("<Leave>", lambda _event: button.configure(bg=base_bg))
        button.bind("<Button-1>", lambda _event: command())
        if parent is self.sidebar_inner:
            button.pack(fill=tk.X, padx=12, pady=4)
            return button
        return button

    def clear_content(self):
        """Clear all widgets from content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_card(self, parent):
        return tk.Frame(
            parent,
            bg=COLORS["card"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )

    def show_welcome(self):
        self.clear_content()
        if self.user["role"] in ["admin", "accountant"]:
            self.show_admin_accountant_dashboard()
        else:
            self.show_simple_role_dashboard()

    def show_admin_accountant_dashboard(self):
        """Admin/Accountant dashboard with charts and stats"""
        # Note: content_frame already scrollable because it's inside ScrollableFrame
        page = self.content_frame

        summary = AccountService.get_financial_summary()
        trend = AccountService.get_monthly_trend_data(12)
        expense_breakdown = AccountService.get_expense_distribution()

        header = self.create_card(page)
        header.pack(fill=tk.X, pady=(0, 16))
        tk.Label(header, text=f"Welcome back, {self.user['username']}", font=FONTS["title"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(
            anchor=tk.W, padx=20, pady=(18, 6)
        )
        tk.Label(header, text="Here is your institution overview and monthly financial trend.", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
            anchor=tk.W, padx=20, pady=(0, 18)
        )

        stats = tk.Frame(page, bg=COLORS["background"])
        stats.pack(fill=tk.X, pady=(0, 16))
        # Responsive grid - columns will adjust based on width
        for index in range(4):
            stats.grid_columnconfigure(index, weight=1)

        cards = [
            ("Total Students", str(len(AccountService.get_all_students())), COLORS["primary"]),
            ("Total Income", f"${summary['total_income']:,.2f}", COLORS["success"]),
            ("Total Expenses", f"${summary['total_expenses']:,.2f}", COLORS["danger"]),
            ("Pending Fees", f"${summary['pending_fees']:,.2f}", COLORS["secondary"]),
        ]
        for col, (title, value, color) in enumerate(cards):
            self.create_stat_card(stats, title, value, color, 0, col)

        chart_grid = tk.Frame(page, bg=COLORS["background"])
        chart_grid.pack(fill=tk.BOTH, expand=True)
        chart_grid.grid_columnconfigure(0, weight=1)
        chart_grid.grid_columnconfigure(1, weight=1)
        chart_grid.grid_rowconfigure(0, weight=1)

        self.create_income_expense_chart(chart_grid, trend, 0, 0)
        self.create_expense_breakdown_chart(chart_grid, expense_breakdown, 0, 1)

    def show_simple_role_dashboard(self):
        """Simple dashboard for staff and students"""
        page = self.content_frame
        
        header = self.create_card(page)
        header.pack(fill=tk.X, pady=(0, 16))
        name = self.user["username"]
        subtitle = "Use the menu on the left to access your dashboard features."
        
        if self.user["role"] == "student":
            summary = AccountService.get_student_dashboard_summary(self.user["id"])
            if summary and summary.get("student"):
                name = summary["student"].get("name") or name
            subtitle = "Use the menu on the left to view your profile, fees, payments, and balance."
        elif self.user["role"] == "staff":
            summary = AccountService.get_staff_dashboard_summary(self.user["id"])
            if summary and summary.get("staff"):
                name = summary["staff"].get("name") or name
            subtitle = "Use the menu on the left to view your profile and salary details."

        tk.Label(header, text=f"Welcome, {name}", font=FONTS["title"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(
            anchor=tk.W, padx=20, pady=(18, 6)
        )
        tk.Label(header, text=subtitle, font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
            anchor=tk.W, padx=20, pady=(0, 18)
        )
        
        # Add some helpful information card
        info_card = self.create_card(page)
        info_card.pack(fill=tk.X, pady=(0, 16))
        
        info_frame = tk.Frame(info_card, bg=COLORS["primary_lighter"])
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(info_frame, text="ℹ️ Quick Tips", font=FONTS["heading"], 
                bg=COLORS["primary_lighter"], fg=COLORS["primary"]).pack(anchor=tk.W)
        tk.Label(info_frame, text="• Use the navigation menu on the left to access all features\n• For assistance, contact your system administrator\n• Keep your login credentials secure", 
                font=FONTS["normal"], bg=COLORS["primary_lighter"], fg=COLORS["text_secondary"], justify=tk.LEFT).pack(anchor=tk.W, pady=(5, 0))

    def create_stat_card(self, parent, title, value, color, row, col):
        card = self.create_card(parent)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        tk.Label(card, text=title, font=FONTS["small"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
            anchor=tk.W, padx=16, pady=(14, 6)
        )
        tk.Label(card, text=value, font=(FONTS["title"][0], 18, "bold"), bg=COLORS["card"], fg=color).pack(
            anchor=tk.W, padx=16, pady=(0, 16)
        )

    def create_chart_card(self, parent, title, row, col):
        card = self.create_card(parent)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        tk.Label(card, text=title, font=FONTS["heading"], bg=COLORS["card"], fg=COLORS["text_primary"]).pack(
            anchor=tk.W, padx=20, pady=(16, 10)
        )
        return card

    def create_income_expense_chart(self, parent, trend_data, row, col):
        card = self.create_chart_card(parent, "Income vs Expense Trend", row, col)
        months = trend_data["months"]
        income = trend_data["income"]
        expense = trend_data["expense"]

        if not any(income) and not any(expense):
            tk.Label(card, text="No data available", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
                pady=70
            )
            return

        fig = Figure(figsize=(5.5, 3.5), facecolor=COLORS["card"], dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(months, income, marker="o", linewidth=2.2, color=COLORS["success"], label="Income")
        ax.plot(months, expense, marker="o", linewidth=2.2, color=COLORS["danger"], label="Expense")
        ax.set_title("Income vs Expense Trend", fontsize=10)
        ax.set_facecolor(COLORS["card"])
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.35)
        ax.legend(fontsize=8)
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=35, ha='right')
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=8)
        
        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

    def create_expense_breakdown_chart(self, parent, expense_data, row, col):
        card = self.create_chart_card(parent, "Expense Breakdown", row, col)

        buckets = {"Salary": 0, "Rent": 0, "Bills": 0, "Others": 0}
        for category, amount in expense_data.items():
            name = str(category).strip().lower()
            if name == "salary":
                buckets["Salary"] += amount
            elif name == "rent":
                buckets["Rent"] += amount
            elif name == "bills":
                buckets["Bills"] += amount
            else:
                buckets["Others"] += amount

        labels = list(buckets.keys())
        values = list(buckets.values())
        
        if not any(values):
            tk.Label(card, text="No data available", font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
                pady=70
            )
            return

        fig = Figure(figsize=(5.5, 3.5), facecolor=COLORS["card"], dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.barh(labels, values, color=[COLORS["primary"], COLORS["secondary"], COLORS["success"], COLORS["danger"]])
        ax.set_facecolor(COLORS["card"])
        ax.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.35)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=9)
        
        max_value = max(values) if max(values) else 1
        for bar, value in zip(bars, values):
            ax.text(value + (max_value * 0.01), bar.get_y() + bar.get_height() / 2, 
                   f"${value:,.0f}", va="center", fontsize=8)
        
        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

    def create_simple_table(self, parent, columns, rows, empty_message="No data available."):
        container = tk.Frame(parent, bg=COLORS["card"])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        if not rows:
            tk.Label(container, text=empty_message, font=FONTS["normal"], bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(
                pady=30
            )
            return None

        style = ttk.Style()
        style.configure("Dashboard.Treeview", rowheight=30, font=FONTS["small"])
        style.configure(
            "Dashboard.Treeview.Heading",
            font=FONTS["heading"],
            background=COLORS["table_header"],
            foreground=COLORS["text_primary"]
        )

        # Create frame with horizontal scroll for table
        table_container = tk.Frame(container)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbars for table
        table_canvas = tk.Canvas(table_container, bg=COLORS["card"], highlightthickness=0)
        h_scroll = ttk.Scrollbar(table_container, orient="horizontal", command=table_canvas.xview)
        v_scroll = ttk.Scrollbar(table_container, orient="vertical", command=table_canvas.yview)
        
        table_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        table_inner = tk.Frame(table_canvas, bg=COLORS["card"])
        table_canvas.create_window((0, 0), window=table_inner, anchor="nw")
        
        table_canvas.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)
        
        # Create treeview inside inner frame
        table = ttk.Treeview(table_inner, columns=columns, show="headings", height=min(len(rows), 8), style="Dashboard.Treeview")
        for col in columns:
            table.heading(col, text=col)
            # Auto-adjust column width based on content
            table.column(col, width=min(200, max(80, len(col) * 15)), anchor=tk.CENTER if col not in ("Description", "Date", "Name") else tk.W)
        
        table.pack(fill=tk.BOTH, expand=True)
        
        def update_scrollregion(event):
            table_canvas.configure(scrollregion=table_canvas.bbox("all"))
        
        table_inner.bind("<Configure>", update_scrollregion)

        for idx, row_data in enumerate(rows):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            table.insert("", tk.END, values=row_data, tags=(tag,))
        table.tag_configure("evenrow", background=COLORS["table_row_even"])
        table.tag_configure("oddrow", background=COLORS["table_row_odd"])
        
        return table

    def show_students(self):
        self.clear_content()
        from views.student_view import StudentView
        StudentView(self.content_frame, self.user, self.switch_callback)

    def show_fees(self):
        self.clear_content()
        from views.fee_view import FeeView
        FeeView(self.content_frame, self.user, self.switch_callback)

    def show_staff(self):
        self.clear_content()
        from views.staff_view import StaffView
        StaffView(self.content_frame, self.user, self.switch_callback)

    def show_payments(self):
        self.clear_content()
        from views.payment_view import PaymentView
        PaymentView(self.content_frame, self.user, self.switch_callback)

    def show_salaries(self):
        self.clear_content()
        from views.salary_view import SalaryView
        SalaryView(self.content_frame, self.user)

    def show_expenses(self):
        self.clear_content()
        from views.expense_view import ExpenseView
        ExpenseView(self.content_frame, self.user, self.switch_callback)

    def show_reports(self):
        self.clear_content()
        from views.report_view import ReportView
        ReportView(self.content_frame, self.user, self.switch_callback)

    def show_register(self):
        if self.user["role"] != "admin":
            messagebox.showerror("Access Denied", "Only admins are allowed to register users.")
            return
        self.clear_content()
        from views.register_view import RegisterView
        RegisterView(self.content_frame, self.switch_callback, self.user)

    def show_my_profile(self):
        self.clear_content()
        from views.my_profile_view import MyProfileView
        MyProfileView(self.content_frame, self.user)

    def show_my_fees(self):
        self.clear_content()
        from views.my_fees_view import MyFeesView
        MyFeesView(self.content_frame, self.user)

    def show_my_payments(self):
        self.clear_content()
        from views.my_payments_view import MyPaymentsView
        MyPaymentsView(self.content_frame, self.user)

    def show_my_balance(self):
        self.clear_content()
        from views.my_balance_view import MyBalanceView
        MyBalanceView(self.content_frame, self.user)

    def show_my_salary(self):
        self.clear_content()
        from views.my_salary_view import MySalaryView
        MySalaryView(self.content_frame, self.user)

    def on_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.switch_callback("home")

    def destroy(self):
        if self.frame:
            self.frame.destroy()


# Add this import at the top for matplotlib
import matplotlib.pyplot as plt