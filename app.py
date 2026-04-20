from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash

app = Flask(__name__)

from database import db
db.init_db()
db.seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validation
        if not name:
            return render_template("register.html", error="Name is required")
        if not email:
            return render_template("register.html", error="Email is required")
        if not password or len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters")

        # Hash password and create user
        password_hash = generate_password_hash(password)
        user_id = db.create_user(name, email, password_hash)

        if user_id is None:
            return render_template("register.html", error="Email already exists")

        return redirect("/login")

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
