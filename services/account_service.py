from datetime import datetime

from models.student_model import StudentModel
from models.fee_model import FeeModel
from models.payment_model import PaymentModel
from models.expense_model import ExpenseModel
from models.staff_model import StaffModel


class AccountService:
    @staticmethod
    def add_student(name, class_name, parent_name, phone, user_id=None):
        return StudentModel.add_student(name, class_name, parent_name, phone, user_id)

    @staticmethod
    def get_all_students():
        return StudentModel.get_all_students()
    
    @staticmethod
    def get_student(student_id):
        return StudentModel.get_student_by_id(student_id)

    @staticmethod
    def get_student_by_user_id(user_id):
        students = StudentModel.get_all_students()
        for student in students:
            if student.get("user_id") == user_id:
                return student
        return None
    
    @staticmethod
    def update_student(student_id, name, class_name, parent_name, phone):
        return StudentModel.update_student(student_id, name, class_name, parent_name, phone)
    
    @staticmethod
    def delete_student(student_id):
        return StudentModel.delete_student(student_id)
    
    @staticmethod
    def search_students(query):
        return StudentModel.search_students(query)
    
    @staticmethod
    def add_fee_structure(class_name, tuition_fee, exam_fee, transport_fee):
        return FeeModel.add_fee_structure(class_name, tuition_fee, exam_fee, transport_fee)
    
    @staticmethod
    def get_all_fee_structures():
        return FeeModel.get_all_fee_structures()
    
    @staticmethod
    def get_fee_by_class(class_name):
        return FeeModel.get_fee_structure_by_class(class_name)
    
    @staticmethod
    def update_fee_structure(fee_id, tuition_fee, exam_fee, transport_fee):
        return FeeModel.update_fee_structure(fee_id, tuition_fee, exam_fee, transport_fee)
    
    @staticmethod
    def delete_fee_structure(fee_id):
        return FeeModel.delete_fee_structure(fee_id)
    
    @staticmethod
    def create_invoice(student_id, total_amount, discount_amount, final_amount, due_date):
        return PaymentModel.create_invoice(student_id, total_amount, discount_amount, final_amount, due_date)
    
    @staticmethod
    def get_all_invoices():
        return PaymentModel.get_all_invoices()
    
    @staticmethod
    def get_invoice(invoice_id):
        return PaymentModel.get_invoice_by_id(invoice_id)
    
    @staticmethod
    def get_student_invoices(student_id):
        return PaymentModel.get_invoices_by_student(student_id)
    
    @staticmethod
    def add_payment(invoice_id, amount_paid, payment_method):
        return PaymentModel.add_payment(invoice_id, amount_paid, payment_method)
    
    @staticmethod
    def get_invoice_payments(invoice_id):
        return PaymentModel.get_payments_by_invoice(invoice_id)

    @staticmethod
    def get_all_payments():
        return PaymentModel.get_all_payments()
    
    @staticmethod
    def add_expense(title, category, amount, date=None):
        return ExpenseModel.add_expense(title, category, amount, date)
    
    @staticmethod
    def get_all_expenses():
        return ExpenseModel.get_all_expenses()
    
    @staticmethod
    def get_expense(expense_id):
        return ExpenseModel.get_expense_by_id(expense_id)
    
    @staticmethod
    def update_expense(expense_id, title, category, amount):
        return ExpenseModel.update_expense(expense_id, title, category, amount)
    
    @staticmethod
    def delete_expense(expense_id):
        return ExpenseModel.delete_expense(expense_id)
    
    @staticmethod
    def get_total_expenses():
        return ExpenseModel.get_total_expenses()
    
    # ==================== INVOICE AUTO-GENERATION (12 MONTHS) ====================
    
    @staticmethod
    def generate_student_invoices(student_id, class_name):
        """
        Automatically generate 12 monthly invoices for a student.
        Called when a new student is registered.
        """
        # Get fee structure for the class
        fee_structure = FeeModel.get_fee_structure_by_class(class_name)
        
        if not fee_structure:
            # If no fee structure exists, create default values
            total_amount = 0
        else:
            # Calculate total fee: tuition + exam + transport
            total_amount = (
                fee_structure.get("tuition_fee", 0) + 
                fee_structure.get("exam_fee", 0) + 
                fee_structure.get("transport_fee", 0)
            )
        
        discount_amount = 0
        final_amount = total_amount
        
        # Generate 12 invoices starting from current month
        current_date = datetime.now()
        invoices_created = []
        
        for month_offset in range(12):
            # Calculate due date (25th of each month)
            target_month = current_date.month + month_offset
            target_year = current_date.year + (target_month - 1) // 12
            actual_month = ((target_month - 1) % 12) + 1
            
            due_date = datetime(target_year, actual_month, 25).strftime("%Y-%m-%d")
            
            # Create invoice
            invoice_id = PaymentModel.create_invoice(
                student_id, 
                total_amount, 
                discount_amount, 
                final_amount, 
                due_date
            )
            invoices_created.append(invoice_id)
        
        return invoices_created
    
    @staticmethod
    def check_invoices_exist_for_student(student_id):
        """Check if invoices already exist for a student."""
        invoices = PaymentModel.get_invoices_by_student(student_id)
        return len(invoices) > 0
    
    # ==================== LATE FEE CALCULATION ====================
    
    @staticmethod
    def calculate_late_fee(invoice_id):
        """
        Calculate late fee (5%) if current date > due_date.
        Returns dict with original_amount, late_fee, total_payable, is_overdue
        """
        invoice = PaymentModel.get_invoice_by_id(invoice_id)
        
        if not invoice:
            return None
        
        # Get total paid so far
        payments = PaymentModel.get_payments_by_invoice(invoice_id)
        total_paid = sum(p.get("amount_paid", 0) for p in payments)
        
        original_amount = invoice.get("final_amount", 0)
        due_date_str = invoice.get("due_date")
        
        # Check if overdue
        is_overdue = False
        late_fee = 0
        
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            current_date = datetime.now()
            
            if current_date > due_date and invoice.get("status") != "paid":
                is_overdue = True
                # Calculate 5% late fee on remaining amount
                remaining = original_amount - total_paid
                if remaining > 0:
                    late_fee = round(remaining * 0.05, 2)
        
        total_payable = original_amount + late_fee - total_paid
        
        return {
            "original_amount": original_amount,
            "late_fee": late_fee,
            "total_paid": total_paid,
            "total_payable": total_payable,
            "is_overdue": is_overdue,
            "due_date": due_date_str,
            "status": invoice.get("status")
        }
    
    # ==================== FINANCIAL REPORTS ====================
    
    @staticmethod
    def get_financial_summary():
        """
        Get comprehensive financial summary:
        - Total Income (SUM of payments)
        - Total Expenses (SUM of expenses)
        - Pending Fees (SUM of unpaid invoices)
        - Profit (income - expenses)
        """
        # Total Income from payments
        all_payments = PaymentModel.get_all_payments()
        total_income = sum(p.get("amount_paid", 0) for p in all_payments)
        
        # Total Expenses
        total_expenses = ExpenseModel.get_total_expenses()
        
        # Pending Fees (unpaid + partial invoices)
        all_invoices = PaymentModel.get_all_invoices()
        pending_fees = 0
        for inv in all_invoices:
            if inv.get("status") in ["unpaid", "partial"]:
                pending_fees += inv.get("final_amount", 0)
        
        # Profit
        profit = total_income - total_expenses
        
        return {
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "pending_fees": round(pending_fees, 2),
            "profit": round(profit, 2)
        }
    
    @staticmethod
    def get_monthly_income():
        """Get monthly income for the current year."""
        all_payments = PaymentModel.get_all_payments()
        monthly_income = {}
        
        current_year = datetime.now().year
        
        for payment in all_payments:
            payment_date = payment.get("payment_date")
            if payment_date:
                payment_year = int(payment_date[:4])
                if payment_year == current_year:
                    month = int(payment_date[5:7])
                    month_name = datetime(2000, month, 1).strftime("%B")
                    monthly_income[month_name] = monthly_income.get(month_name, 0) + payment.get("amount_paid", 0)
        
        return monthly_income

    @staticmethod
    def get_monthly_trend_data(month_count=12):
        """Return month labels with grouped income and expense totals."""
        month_count = max(1, month_count)
        current = datetime.now()

        month_slots = []
        for offset in range(month_count - 1, -1, -1):
            month = current.month - offset
            year = current.year
            while month <= 0:
                month += 12
                year -= 1
            month_slots.append((year, month))

        month_map = {(year, month): 0 for year, month in month_slots}
        income_totals = dict(month_map)
        expense_totals = dict(month_map)

        for payment in PaymentModel.get_all_payments():
            payment_date = payment.get("payment_date")
            if not payment_date:
                continue
            year = int(payment_date[:4])
            month = int(payment_date[5:7])
            if (year, month) in income_totals:
                income_totals[(year, month)] += payment.get("amount_paid", 0)

        for expense in ExpenseModel.get_all_expenses():
            expense_date = expense.get("date")
            if not expense_date:
                continue
            year = int(expense_date[:4])
            month = int(expense_date[5:7])
            if (year, month) in expense_totals:
                expense_totals[(year, month)] += expense.get("amount", 0)

        labels = [datetime(year, month, 1).strftime("%b %y") for year, month in month_slots]
        income_values = [round(income_totals[(year, month)], 2) for year, month in month_slots]
        expense_values = [round(expense_totals[(year, month)], 2) for year, month in month_slots]

        return {
            "months": labels,
            "income": income_values,
            "expense": expense_values
        }
    
    @staticmethod
    def get_expense_distribution():
        """Get expense distribution by category."""
        all_expenses = ExpenseModel.get_all_expenses()
        category_totals = {}
        
        for expense in all_expenses:
            category = expense.get("category", "Other")
            category_totals[category] = category_totals.get(category, 0) + expense.get("amount", 0)
        
        return category_totals
    
    @staticmethod
    def get_invoice_status_summary():
        """Get summary of paid vs unpaid invoices."""
        all_invoices = PaymentModel.get_all_invoices()
        
        paid_amount = 0
        unpaid_amount = 0
        partial_amount = 0
        
        for inv in all_invoices:
            status = inv.get("status")
            amount = inv.get("final_amount", 0)
            
            if status == "paid":
                paid_amount += amount
            elif status == "partial":
                partial_amount += amount
            else:
                unpaid_amount += amount
        
        return {
            "paid": round(paid_amount, 2),
            "unpaid": round(unpaid_amount, 2),
            "partial": round(partial_amount, 2)
        }
    
    # ==================== STAFF MANAGEMENT ====================
    
    @staticmethod
    def add_staff(name, father_name, qualification, department, designation, salary, user_id=None):
        return StaffModel.add_staff(name, father_name, qualification, department, designation, salary, user_id)

    @staticmethod
    def get_all_staff():
        return StaffModel.get_all_staff()
    
    @staticmethod
    def get_staff(staff_id):
        return StaffModel.get_staff_by_id(staff_id)
    
    @staticmethod
    def get_staff_by_user_id(user_id):
        return StaffModel.get_staff_by_user_id(user_id)
    
    @staticmethod
    def update_staff(staff_id, name, father_name, qualification, department, designation, salary):
        return StaffModel.update_staff(staff_id, name, father_name, qualification, department, designation, salary)
    
    @staticmethod
    def delete_staff(staff_id):
        return StaffModel.delete_staff(staff_id)
    
    @staticmethod
    def search_staff(query):
        return StaffModel.search_staff(query)
    
    # ==================== STAFF SALARY METHODS ====================
    
    @staticmethod
    def create_salary_record(staff_id, salary_amount, month, due_date):
        return StaffModel.create_salary_record(staff_id, salary_amount, month, due_date)
    
    @staticmethod
    def get_all_salary_records():
        return StaffModel.get_all_salary_records()
    
    @staticmethod
    def get_salary_by_id(salary_id):
        return StaffModel.get_salary_by_id(salary_id)
    
    @staticmethod
    def get_staff_salaries(staff_id):
        return StaffModel.get_salary_by_staff(staff_id)
    
    @staticmethod
    def get_salary_by_month(month):
        return StaffModel.get_salary_by_month(month)
    
    @staticmethod
    def pay_salary(salary_id, payment_method):
        return StaffModel.pay_salary(salary_id, payment_method)
    
    @staticmethod
    def get_total_salary_expenses():
        return StaffModel.get_total_salary_expenses()
    
    @staticmethod
    def check_and_update_late_salaries():
        return StaffModel.check_and_update_late_salaries()
    
    @staticmethod
    def generate_monthly_salary_records(month):
        return StaffModel.generate_monthly_salary_records(month)
    
    # ==================== ENHANCED FINANCIAL REPORTS ====================
    
    @staticmethod
    def get_enhanced_financial_summary():
        """
        Get enhanced financial summary including salary expenses.
        """
        # Total Income from payments
        all_payments = PaymentModel.get_all_payments()
        total_income = sum(p.get("amount_paid", 0) for p in all_payments)
        
        # Regular Expenses
        all_expenses = ExpenseModel.get_all_expenses()
        salary_expenses = sum(
            expense.get("amount", 0)
            for expense in all_expenses
            if expense.get("category") == "salary"
        )
        regular_expenses = sum(
            expense.get("amount", 0)
            for expense in all_expenses
            if expense.get("category") != "salary"
        )
        total_expenses = regular_expenses + salary_expenses
        
        # Pending Fees (unpaid + partial invoices)
        all_invoices = PaymentModel.get_all_invoices()
        pending_fees = 0
        for inv in all_invoices:
            if inv.get("status") in ["unpaid", "partial"]:
                pending_fees += inv.get("final_amount", 0)
        
        # Pending Salaries
        all_salaries = StaffModel.get_all_salary_records()
        pending_salaries = 0
        for sal in all_salaries:
            if sal.get("status") in ["unpaid", "late"]:
                pending_salaries += sal.get("salary_amount", 0)
        
        # Profit
        profit = total_income - total_expenses
        
        return {
            "total_income": round(total_income, 2),
            "regular_expenses": round(regular_expenses, 2),
            "salary_expenses": round(salary_expenses, 2),
            "total_expenses": round(total_expenses, 2),
            "pending_fees": round(pending_fees, 2),
            "pending_salaries": round(pending_salaries, 2),
            "profit": round(profit, 2)
        }
    
    @staticmethod
    def get_monthly_expenses():
        """Get monthly expenses (regular + salary) for the current year."""
        all_expenses = ExpenseModel.get_all_expenses()
        monthly_expenses = {}
        
        current_year = datetime.now().year
        
        for expense in all_expenses:
            expense_date = expense.get("date")
            if expense_date:
                expense_year = int(expense_date[:4])
                if expense_year == current_year:
                    month = int(expense_date[5:7])
                    month_name = datetime(2000, month, 1).strftime("%B")
                    monthly_expenses[month_name] = monthly_expenses.get(month_name, 0) + expense.get("amount", 0)
        
        return monthly_expenses

    @staticmethod
    def get_staff_count():
        return len(StaffModel.get_all_staff())

    @staticmethod
    def get_student_dashboard_summary(user_id):
        student = AccountService.get_student_by_user_id(user_id)
        if not student:
            return None

        invoices = PaymentModel.get_invoices_by_student(student["id"])
        total_fees = 0
        total_paid = 0
        late_fees = 0
        recent_payments = []

        for invoice in invoices:
            fee_info = AccountService.calculate_late_fee(invoice["id"])
            if fee_info:
                total_fees += fee_info["original_amount"]
                total_paid += fee_info["total_paid"]
                late_fees += fee_info["late_fee"]

            for payment in PaymentModel.get_payments_by_invoice(invoice["id"]):
                recent_payments.append({
                    "id": payment["id"],
                    "invoice_id": payment["invoice_id"],
                    "amount": payment["amount_paid"],
                    "method": payment["payment_method"],
                    "date": payment["payment_date"]
                })

        recent_payments.sort(key=lambda item: item.get("date", ""), reverse=True)

        return {
            "student": student,
            "total_fees": round(total_fees, 2),
            "paid": round(total_paid, 2),
            "late_fees": round(late_fees, 2),
            "balance": round((total_fees + late_fees) - total_paid, 2),
            "recent_payments": recent_payments[:5]
        }

    @staticmethod
    def get_staff_dashboard_summary(user_id):
        staff = StaffModel.get_staff_by_user_id(user_id)
        if not staff:
            return None

        salaries = StaffModel.get_salary_by_staff(staff["id"])
        current_record = salaries[0] if salaries else None

        return {
            "staff": staff,
            "salary": round(staff.get("salary", 0), 2),
            "status": (current_record.get("status", "no record") if current_record else "no record"),
            "salary_history": salaries[:6]
        }
    
    @staticmethod
    def get_recent_transactions(limit=20):
        """Get recent transactions (payments + expenses combined)."""
        transactions = []
        
        # Get recent payments
        all_payments = PaymentModel.get_all_payments()
        for payment in all_payments:
            transactions.append({
                "type": "income",
                "amount": payment.get("amount_paid", 0),
                "date": payment.get("payment_date"),
                "description": f"Payment - Invoice #{payment.get('invoice_id')}"
            })
        
        # Get recent expenses
        all_expenses = ExpenseModel.get_all_expenses()
        for expense in all_expenses:
            transactions.append({
                "type": "expense",
                "amount": expense.get("amount", 0),
                "date": expense.get("date"),
                "description": f"{expense.get('title', 'Expense')}"
            })
        
        # Sort by date descending
        transactions.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        return transactions[:limit]
