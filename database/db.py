import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "expense_tracker.db")


def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category_id INTEGER NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Inserts sample data for development."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Create a demo user with hashed password "demo"
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.app", "scrypt:32768:8:1$Df46JA8G5qv75gOF$5e9b7490421524d4982d78af2c1b2102b02703af2ce9dc7516836144ed098f7d266bed38143fa87b286d98fe74a2e8502089332d668527f70ee078d79b1c0d72")
    )
    user_id = cursor.lastrowid

    # Create default categories
    default_categories = [
        ("Food", "🍔", user_id),
        ("Transport", "🚌", user_id),
        ("Bills", "📄", user_id),
        ("Health", "💊", user_id),
        ("Entertainment", "🎬", user_id),
        ("Shopping", "🛍️", user_id),
        ("Other", "📦", user_id),
    ]

    cursor.executemany(
        "INSERT INTO categories (name, icon, user_id) VALUES (?, ?, ?)",
        default_categories
    )

    # Seed expenses
    expenses = [
        (350, 1, "Breakfast and coffee", "2026-04-18", user_id),
        (1200, 2, "Monthly metro pass", "2026-04-17", user_id),
        (4500, 3, "Electricity bill", "2026-04-15", user_id),
        (800, 4, "Vitamins", "2026-04-14", user_id),
        (2200, 1, "Weekend dinner", "2026-04-12", user_id),
        (1500, 5, "Movie tickets", "2026-04-10", user_id),
        (3200, 6, "New shirt", "2026-04-08", user_id),
    ]

    cursor.executemany(
        "INSERT INTO expenses (amount, category_id, description, date, user_id) VALUES (?, ?, ?, ?, ?)",
        expenses
    )

    # Seed income
    income = [
        (65000, "Monthly salary", "2026-04-01", user_id),
        (5000, "Freelance project", "2026-04-12", user_id),
    ]

    cursor.executemany(
        "INSERT INTO income (amount, description, date, user_id) VALUES (?, ?, ?, ?)",
        income
    )

    conn.commit()
    conn.close()
