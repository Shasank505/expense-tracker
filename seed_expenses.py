#!/usr/bin/env python
"""Seed realistic dummy expenses for a specific user."""

import sqlite3
import random
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '.')
from database.db import get_db

# Arguments
USER_ID = 2
COUNT = 5
MONTHS = 3

# Category definitions with Indian context
CATEGORIES = {
    'Food': {'weight': 25, 'amount_range': (50, 800), 'descriptions': [
        'Breakfast at local cafe', 'Lunch thali', 'Street food', 'Groceries',
        'Dinner with family', 'Coffee and snacks', 'Tiffin service', 'Biryani'
    ]},
    'Transport': {'weight': 15, 'amount_range': (20, 500), 'descriptions': [
        'Auto rickshaw', 'Metro card recharge', 'Bus fare', 'Cab ride',
        'Fuel', 'Ola/Uber', 'Monthly pass', 'Bike service'
    ]},
    'Bills': {'weight': 20, 'amount_range': (200, 3000), 'descriptions': [
        'Electricity bill', 'Mobile recharge', 'Internet bill', 'Water bill',
        'Cooking gas', 'Maintenance charges', 'DTH subscription'
    ]},
    'Health': {'weight': 8, 'amount_range': (100, 2000), 'descriptions': [
        'Doctor consultation', 'Medicines', 'Gym membership', 'Health checkup',
        'Vitamins', 'Physiotherapy', 'Dental visit'
    ]},
    'Entertainment': {'weight': 10, 'amount_range': (100, 1500), 'descriptions': [
        'Movie tickets', 'OTT subscription', 'Concert', 'Gaming',
        'Book purchase', 'Streaming service', 'Club entry'
    ]},
    'Shopping': {'weight': 12, 'amount_range': (200, 5000), 'descriptions': [
        'Clothes', 'Shoes', 'Electronics', 'Home decor',
        'Gifts', 'Accessories', 'Furniture'
    ]},
    'Other': {'weight': 10, 'amount_range': (50, 1000), 'descriptions': [
        'Miscellaneous', 'Donations', 'Stationery', 'Pet supplies',
        'Car wash', 'Laundry', 'Salon'
    ]}
}

def get_category_weights():
    """Return list of (category_name, weight) tuples."""
    return [(name, data['weight']) for name, data in CATEGORIES.items()]

def weighted_choice(choices):
    """Select item based on weights."""
    total = sum(w for _, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for name, weight in choices:
        upto += weight
        if r <= upto:
            return name
    return choices[-1][0]

def generate_expense(category_name, date):
    """Generate a single expense dict."""
    cat = CATEGORIES[category_name]
    amount = round(random.uniform(*cat['amount_range']), 2)
    description = random.choice(cat['descriptions'])
    return {
        'category': category_name,
        'amount': amount,
        'description': description,
        'date': date
    }

def get_random_date_in_past_months(months):
    """Generate random date within past N months."""
    today = datetime.now()
    start_date = today - timedelta(days=months * 30)
    days_diff = random.randint(0, (today - start_date).days)
    random_date = start_date + timedelta(days=days_diff)
    return random_date.strftime('%Y-%m-%d')

def main():
    # Get category IDs from database
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM categories WHERE user_id = ?", (USER_ID,))
    category_map = {row['name']: row['id'] for row in cursor.fetchall()}

    if not category_map:
        print("No categories found for this user. Please run seed_db first.")
        conn.close()
        return

    # Generate expenses
    expenses = []
    for _ in range(COUNT):
        category = weighted_choice(get_category_weights())
        date = get_random_date_in_past_months(MONTHS)
        expense = generate_expense(category, date)
        expense['category_id'] = category_map[category]
        expenses.append(expense)

    # Insert in single transaction
    try:
        cursor.execute("BEGIN")
        for exp in expenses:
            cursor.execute(
                "INSERT INTO expenses (amount, category_id, description, date, user_id) VALUES (?, ?, ?, ?, ?)",
                (exp['amount'], exp['category_id'], exp['description'], exp['date'], USER_ID)
            )
        conn.commit()

        # Fetch inserted records for confirmation
        cursor.execute(
            "SELECT e.id, e.amount, c.name, e.description, e.date FROM expenses e JOIN categories c ON e.category_id = c.id WHERE e.user_id = ? ORDER BY e.date DESC LIMIT ?",
            (USER_ID, COUNT)
        )
        inserted = cursor.fetchall()

        # Get date range
        cursor.execute(
            "SELECT MIN(date), MAX(date) FROM expenses WHERE user_id = ?",
            (USER_ID,)
        )
        date_range = cursor.fetchone()

        print(f"\n{'='*50}")
        print(f"Successfully inserted {COUNT} expenses")
        print(f"Date range: {date_range['MIN(date)']} to {date_range['MAX(date)']}")
        print(f"\nSample of inserted records:")
        print(f"{'ID':<5} {'Amount':<10} {'Category':<15} {'Description':<25} {'Date':<12}")
        print("-" * 70)
        for row in inserted[:5]:
            print(f"{row['id']:<5} Rs.{row['amount']:<8.2f} {row['name']:<15} {row['description']:<25} {row['date']:<12}")
        print(f"{'='*50}\n")

    except Exception as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
