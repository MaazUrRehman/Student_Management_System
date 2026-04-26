from datetime import datetime
from database.db import get_connection


class StaffModel:
    @staticmethod
    def add_staff(name, father_name, qualification, department, designation, salary, user_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO staff (name, father_name, qualification, department, designation, salary, user_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (name, father_name, qualification, department, designation, salary, user_id)
            )
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_staff():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM staff ORDER BY name")
            staff = cursor.fetchall()
            return [dict(row) for row in staff]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_staff_by_id(staff_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM staff WHERE id = ?", (staff_id,))
            staff = cursor.fetchone()
            return dict(staff) if staff else None
            
        finally:
            conn.close()
    
    @staticmethod
    def get_staff_by_user_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM staff WHERE user_id = ?", (user_id,))
            staff = cursor.fetchone()
            return dict(staff) if staff else None
            
        finally:
            conn.close()
    
    @staticmethod
    def update_staff(staff_id, name, father_name, qualification, department, designation, salary):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """UPDATE staff 
                   SET name = ?, father_name = ?, qualification = ?, department = ?, designation = ?, salary = ? 
                   WHERE id = ?""",
                (name, father_name, qualification, department, designation, salary, staff_id)
            )
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def delete_staff(staff_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def search_staff(query):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT * FROM staff 
                   WHERE name LIKE ? OR department LIKE ? OR designation LIKE ? 
                   ORDER BY name""",
                (f"%{query}%", f"%{query}%", f"%{query}%")
            )
            staff = cursor.fetchall()
            return [dict(row) for row in staff]
            
        finally:
            conn.close()
    
    # ==================== STAFF SALARY METHODS ====================
    
    @staticmethod
    def create_salary_record(staff_id, salary_amount, month, due_date):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "unpaid"
            
            cursor.execute(
                """INSERT INTO staff_salary 
                   (staff_id, salary_amount, month, due_date, status, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (staff_id, salary_amount, month, due_date, status, created_at)
            )
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_salary_records():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT ss.*, s.name as staff_name, s.department, s.designation 
                   FROM staff_salary ss 
                   JOIN staff s ON ss.staff_id = s.id 
                   ORDER BY ss.id DESC"""
            )
            records = cursor.fetchall()
            return [dict(row) for row in records]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_salary_by_id(salary_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT ss.*, s.name as staff_name, s.department, s.designation 
                   FROM staff_salary ss 
                   JOIN staff s ON ss.staff_id = s.id 
                   WHERE ss.id = ?""",
                (salary_id,)
            )
            record = cursor.fetchone()
            return dict(record) if record else None
            
        finally:
            conn.close()
    
    @staticmethod
    def get_salary_by_staff(staff_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT * FROM staff_salary 
                   WHERE staff_id = ? 
                   ORDER BY id DESC""",
                (staff_id,)
            )
            records = cursor.fetchall()
            return [dict(row) for row in records]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_salary_by_month(month):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT ss.*, s.name as staff_name, s.department, s.designation 
                   FROM staff_salary ss 
                   JOIN staff s ON ss.staff_id = s.id 
                   WHERE ss.month = ? 
                   ORDER BY ss.id DESC""",
                (month,)
            )
            records = cursor.fetchall()
            return [dict(row) for row in records]
            
        finally:
            conn.close()
    
    @staticmethod
    def pay_salary(salary_id, payment_method):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                "UPDATE staff_salary SET status = ?, payment_date = ?, payment_method = ? WHERE id = ?",
                ("paid", payment_date, payment_method, salary_id)
            )
            
            # Get salary record to add as expense
            cursor.execute("SELECT * FROM staff_salary WHERE id = ?", (salary_id,))
            salary_record = cursor.fetchone()
            
            if salary_record:
                # Add salary as expense
                cursor.execute(
                    """INSERT INTO expenses (title, category, amount, date) 
                       VALUES (?, ?, ?, ?)""",
                    (f"Salary - {salary_record['month']}", "salary", salary_record["salary_amount"], payment_date)
                )
                
                # Also add to transactions
                cursor.execute(
                    """INSERT INTO transactions (type, amount, reference_id, date) 
                       VALUES (?, ?, ?, ?)""",
                    ("expense", salary_record["salary_amount"], salary_id, payment_date)
                )
            
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def get_total_salary_expenses():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT SUM(salary_amount) as total FROM staff_salary WHERE status = 'paid'"
            )
            result = cursor.fetchone()
            return result["total"] if result["total"] else 0
            
        finally:
            conn.close()
    
    @staticmethod
    def check_and_update_late_salaries():
        """Check for unpaid salaries past due date and mark as late."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Find unpaid salaries where due_date has passed
            cursor.execute(
                """UPDATE staff_salary 
                   SET status = 'late' 
                   WHERE status = 'unpaid' AND due_date < ?""",
                (current_date,)
            )
            
            conn.commit()
            return cursor.rowcount
            
        finally:
            conn.close()
    
    @staticmethod
    def generate_monthly_salary_records(month):
        """Generate salary records for all staff for a given month."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Get all staff
            cursor.execute("SELECT * FROM staff")
            all_staff = cursor.fetchall()
            
            # Check if records already exist for this month
            cursor.execute(
                "SELECT COUNT(*) as count FROM staff_salary WHERE month = ?",
                (month,)
            )
            existing = cursor.fetchone()["count"]
            
            if existing > 0:
                return []  # Records already exist
            
            # Calculate due date (10th of the month)
            year, mon = map(int, month.split("-"))
            due_date = datetime(year, mon, 10).strftime("%Y-%m-%d")
            
            records_created = []
            for staff in all_staff:
                salary_id = cursor.execute(
                    """INSERT INTO staff_salary 
                       (staff_id, salary_amount, month, due_date, status, created_at) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (staff["id"], staff["salary"], month, due_date, "unpaid", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                records_created.append(staff["id"])
            
            conn.commit()
            return records_created
            
        finally:
            conn.close()