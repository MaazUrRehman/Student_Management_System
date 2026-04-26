import sqlite3
from pathlib import Path


def get_connection():
    db_path = Path(__file__).parent.parent / "sms.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def close_connection(conn):
    if conn:
        conn.close()