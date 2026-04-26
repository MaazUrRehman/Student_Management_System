from datetime import datetime
from database.db import get_connection


class FeeModel:
    @staticmethod
    def add_fee_structure(class_name, tuition_fee, exam_fee, transport_fee):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """INSERT INTO fee_structures 
                   (class_name, tuition_fee, exam_fee, transport_fee, created_at) 
                   VALUES (?, ?, ?, ?, ?)""",
                (class_name, tuition_fee, exam_fee, transport_fee, created_at)
            )
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_fee_structures():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM fee_structures ORDER BY id ASC")
            structures = cursor.fetchall()
            return [dict(row) for row in structures]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_fee_structure_by_class(class_name):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM fee_structures WHERE class_name = ?",
                (class_name,)
            )
            structure = cursor.fetchone()
            return dict(structure) if structure else None
            
        finally:
            conn.close()
    
    @staticmethod
    def update_fee_structure(fee_id, tuition_fee, exam_fee, transport_fee):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """UPDATE fee_structures 
                   SET tuition_fee = ?, exam_fee = ?, transport_fee = ? 
                   WHERE id = ?""",
                (tuition_fee, exam_fee, transport_fee, fee_id)
            )
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def delete_fee_structure(fee_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM fee_structures WHERE id = ?", (fee_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
