"""Database connection and table creation module for the system."""

import sqlite3

DB_NAME = "user_management_cli.db"


def get_connection():
    """Create and return a SQLite database connection."""
    return sqlite3.connect(DB_NAME)


def create_tables():
    """Create required database tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            reset_token TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            used INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()