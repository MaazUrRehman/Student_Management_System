from database.db import get_connection

class AuthModel:
    @staticmethod
    def add_user(username, password, role):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            conn.commit()
            return cursor.lastrowid
            
        finally:
            conn.close()
    
    @staticmethod
    def verify_user(username, password):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            
            if user:
                return {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"]
                }
            return None
            
        finally:
            conn.close()
    
    @staticmethod
    def get_user_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if user:
                return {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"]
                }
            return None
            
        finally:
            conn.close()
    
    @staticmethod
    def get_all_users():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, username, role FROM users")
            users = cursor.fetchall()
            return [dict(row) for row in users]
            
        finally:
            conn.close()