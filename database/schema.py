from datetime import datetime
from database.db import get_connection, close_connection
from utils.helpers import hash_password


def migrate_users_table_for_staff(conn, cursor):
    cursor.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'users'")
    row = cursor.fetchone()
    table_sql = row["sql"] if row else ""

    if "'staff'" in table_sql:
        return

    cursor.execute("PRAGMA foreign_keys = OFF")
    cursor.execute("""
        CREATE TABLE users_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'accountant', 'student', 'staff'))
        )
    """)
    cursor.execute("""
        INSERT INTO users_new (id, username, password, role)
        SELECT id, username, password, role
        FROM users
    """)
    cursor.execute("DROP TABLE users")
    cursor.execute("ALTER TABLE users_new RENAME TO users")
    cursor.execute("PRAGMA foreign_keys = ON")


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'accountant', 'student', 'staff'))
            )
        """)

        migrate_users_table_for_staff(conn, cursor)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class_name TEXT NOT NULL,
                parent_name TEXT,
                phone TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fee_structures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_name TEXT NOT NULL UNIQUE,
                tuition_fee REAL NOT NULL DEFAULT 0,
                exam_fee REAL NOT NULL DEFAULT 0,
                transport_fee REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                total_amount REAL NOT NULL DEFAULT 0,
                discount_amount REAL NOT NULL DEFAULT 0,
                final_amount REAL NOT NULL DEFAULT 0,
                due_date TEXT,
                status TEXT NOT NULL CHECK(status IN ('paid', 'partial', 'unpaid')),
                created_at TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                amount_paid REAL NOT NULL DEFAULT 0,
                payment_method TEXT CHECK(payment_method IN ('cash', 'bank')),
                payment_date TEXT NOT NULL,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('fixed', 'percentage')),
                value REAL NOT NULL DEFAULT 0,
                reason TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL DEFAULT 0,
                date TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                amount REAL NOT NULL DEFAULT 0,
                reference_id INTEGER,
                date TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                father_name TEXT,
                qualification TEXT,
                department TEXT,
                designation TEXT,
                salary REAL NOT NULL DEFAULT 0,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff_salary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id INTEGER NOT NULL,
                salary_amount REAL NOT NULL DEFAULT 0,
                month TEXT NOT NULL,
                due_date TEXT,
                status TEXT NOT NULL CHECK(status IN ('paid', 'unpaid', 'late')),
                payment_date TEXT,
                payment_method TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE
            )
        """)
        
        default_users = [
            ("admin", hash_password("123"), "admin"),
            ("accountant", hash_password("123"), "accountant"),
            ("student", hash_password("123"), "student")
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
            default_users
        )
        
        conn.commit()
        print("All tables created successfully!")
        print("Default users inserted (admin/accountant/student with password '123')")
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
        raise
        
    finally:
        close_connection(conn)


if __name__ == "__main__":
    create_tables()
