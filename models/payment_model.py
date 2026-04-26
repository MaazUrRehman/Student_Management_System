from datetime import datetime
from database.db import get_connection


class PaymentModel:
    @staticmethod
    def create_invoice(student_id, total_amount, discount_amount, final_amount, due_date):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "unpaid"
            
            cursor.execute(
                """INSERT INTO invoices 
                   (student_id, total_amount, discount_amount, final_amount, due_date, status, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (student_id, total_amount, discount_amount, final_amount, due_date, status, created_at)
            )
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_invoices():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT i.*, s.name as student_name, s.class_name 
                   FROM invoices i 
                   JOIN students s ON i.student_id = s.id 
                   ORDER BY i.id ASC"""
            )
            invoices = cursor.fetchall()
            return [dict(row) for row in invoices]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_invoice_by_id(invoice_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT i.*, s.name as student_name, s.class_name 
                   FROM invoices i 
                   JOIN students s ON i.student_id = s.id 
                   WHERE i.id = ?""",
                (invoice_id,)
            )
            invoice = cursor.fetchone()
            return dict(invoice) if invoice else None
            
        finally:
            conn.close()
    
    @staticmethod
    def get_invoices_by_student(student_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT * FROM invoices 
                   WHERE student_id = ? 
                   ORDER BY id ASC""",
                (student_id,)
            )
            invoices = cursor.fetchall()
            return [dict(row) for row in invoices]
            
        finally:
            conn.close()
    
    @staticmethod
    def add_payment(invoice_id, amount_paid, payment_method):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                """INSERT INTO payments 
                   (invoice_id, amount_paid, payment_method, payment_date) 
                   VALUES (?, ?, ?, ?)""",
                (invoice_id, amount_paid, payment_method, payment_date)
            )
            
            cursor.execute(
                "SELECT SUM(amount_paid) as total_paid FROM payments WHERE invoice_id = ?",
                (invoice_id,)
            )
            paid = cursor.fetchone()["total_paid"] or 0
            
            cursor.execute(
                "SELECT final_amount FROM invoices WHERE id = ?",
                (invoice_id,)
            )
            final = cursor.fetchone()["final_amount"]
            
            if paid >= final:
                status = "paid"
            elif paid > 0:
                status = "partial"
            else:
                status = "unpaid"
            
            cursor.execute(
                "UPDATE invoices SET status = ? WHERE id = ?",
                (status, invoice_id)
            )
            
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def get_payments_by_invoice(invoice_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM payments WHERE invoice_id = ? ORDER BY payment_date DESC",
                (invoice_id,)
            )
            payments = cursor.fetchall()
            return [dict(row) for row in payments]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_payments():
        """Get all payments across all invoices."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT p.*, i.student_id, s.name as student_name 
                   FROM payments p 
                   JOIN invoices i ON p.invoice_id = i.id 
                   JOIN students s ON i.student_id = s.id 
                   ORDER BY p.payment_date DESC"""
            )
            payments = cursor.fetchall()
            return [dict(row) for row in payments]
            
        finally:
            conn.close()