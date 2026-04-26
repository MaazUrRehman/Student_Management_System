from datetime import datetime
from database.db import get_connection


class ExpenseModel:
    @staticmethod
    def add_expense(title, category, amount, date=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            cursor.execute(
                """INSERT INTO expenses (title, category, amount, date) 
                   VALUES (?, ?, ?, ?)""",
                (title, category, amount, date)
            )
            
            cursor.execute(
                """INSERT INTO transactions (type, amount, reference_id, date) 
                   VALUES (?, ?, ?, ?)""",
                ("expense", amount, cursor.lastrowid, date)
            )
            
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_expenses():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
            expenses = cursor.fetchall()
            return [dict(row) for row in expenses]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_expense_by_id(expense_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            expense = cursor.fetchone()
            return dict(expense) if expense else None
            
        finally:
            conn.close()
    
    @staticmethod
    def update_expense(expense_id, title, category, amount):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """UPDATE expenses 
                   SET title = ?, category = ?, amount = ? 
                   WHERE id = ?""",
                (title, category, amount, expense_id)
            )
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def delete_expense(expense_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def get_expenses_by_category(category):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC",
                (category,)
            )
            expenses = cursor.fetchall()
            return [dict(row) for row in expenses]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_total_expenses():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT SUM(amount) as total FROM expenses")
            result = cursor.fetchone()["total"]
            return result if result else 0
            
        finally:
            conn.close()