from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

from database import db
from database.auth import login_required, get_current_user

db.init_db()
db.seed_db()


@app.context_processor
def inject_current_user():
    """Make current_user available in all templates."""
    return {"current_user": get_current_user()}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters")

    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return render_template("register.html", error="Email already registered")

    password_hash = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    session["user_id"] = user_id
    return redirect(url_for("profile"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]
        return redirect(url_for("profile"))

    return render_template("login.html", error="Invalid email or password")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Protected routes                                                    #
# ------------------------------------------------------------------ #

@app.route("/profile")
@login_required
def profile():
    user = {"name": "Demo User", "email": "demo@spendly.app", "member_since": "April 2026"}
    stats = {"total_spent": "₹13,050", "transaction_count": "7", "top_category": "Bills"}
    transactions = [
        {"date": "18 Apr 2026", "description": "Breakfast and coffee", "category": "Food", "amount": "₹350"},
        {"date": "17 Apr 2026", "description": "Monthly metro pass", "category": "Transport", "amount": "₹1,200"},
        {"date": "15 Apr 2026", "description": "Electricity bill", "category": "Bills", "amount": "₹4,500"},
        {"date": "14 Apr 2026", "description": "Vitamins", "category": "Health", "amount": "₹800"},
        {"date": "12 Apr 2026", "description": "Weekend dinner", "category": "Food", "amount": "₹2,200"},
    ]
    categories = [
        {"name": "Bills", "amount": "₹4,500", "pct": 34},
        {"name": "Food", "amount": "₹2,550", "pct": 20},
        {"name": "Transport", "amount": "₹1,200", "pct": 9},
        {"name": "Shopping", "amount": "₹3,200", "pct": 25},
        {"name": "Entertainment", "amount": "₹1,500", "pct": 11},
    ]
    return render_template("profile.html", user=user, stats=stats, transactions=transactions, categories=categories)


@app.route("/expenses/add")
@login_required
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
@login_required
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
@login_required
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
