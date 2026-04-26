from database.db import get_connection


class StudentModel:
    @staticmethod
    def add_student(name, class_name, parent_name, phone, user_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """INSERT INTO students (name, class_name, parent_name, phone, user_id) 
                   VALUES (?, ?, ?, ?, ?)""",
                (name, class_name, parent_name, phone, user_id)
            )
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_students():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM students ORDER BY name")
            students = cursor.fetchall()
            return [dict(row) for row in students]
            
        finally:
            conn.close()
    
    @staticmethod
    def get_student_by_id(student_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            student = cursor.fetchone()
            return dict(student) if student else None
            
        finally:
            conn.close()
    
    @staticmethod
    def update_student(student_id, name, class_name, parent_name, phone):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """UPDATE students 
                   SET name = ?, class_name = ?, parent_name = ?, phone = ? 
                   WHERE id = ?""",
                (name, class_name, parent_name, phone, student_id)
            )
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def delete_student(student_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    @staticmethod
    def search_students(query):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """SELECT * FROM students 
                   WHERE name LIKE ? OR class_name LIKE ? 
                   ORDER BY name""",
                (f"%{query}%", f"%{query}%")
            )
            students = cursor.fetchall()
            return [dict(row) for row in students]
            
        finally:
            conn.close()