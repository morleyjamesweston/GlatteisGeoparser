"""Authentication routes for the geotester web app."""

from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import Users, db


def register_auth_routes(app, static_folder):
    """Register authentication routes to the Flask app."""

    @app.route("/auth/register", methods=["GET", "POST"])
    def register():
        """User registration endpoint."""
        if request.method == "POST":
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            print(f"Received registration request for username: {username}")

            if Users.query.filter_by(username=username).first():
                print(f"Registration failed: Username '{username}' already taken")
                return (
                    jsonify({"success": False, "error": "Username already taken"}),
                    400,
                )

            if password:
                hashed_password = generate_password_hash(
                    password, method="pbkdf2:sha256"
                )
            else:
                print("registration failed")
                return (
                    jsonify(
                        {"success": False, "error": "Invalid username or password"}
                    ),
                    401,
                )

            new_user = Users(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"success": True, "message": "Registration successful"}), 201
        return send_from_directory(static_folder, "auth/register.html")

    @app.route("/auth/login", methods=["GET", "POST"])
    def login():
        """User login endpoint."""
        if request.method == "POST":
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            user = Users.query.filter_by(username=username).first()

            if user and password and check_password_hash(user.password, password):
                login_user(user)
                return jsonify({"success": True, "message": "Login successful"})
            else:
                print(f"Login failed for username: {username}")
                print(
                    f"User found: {user is not None}, Password provided: {password is not None}"
                )
                return (
                    jsonify(
                        {"success": False, "error": "Invalid username or password"}
                    ),
                    401,
                )

        return send_from_directory(static_folder, "auth/login.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        """Protected dashboard route."""
        return render_template("dashboard.html", username=current_user.username)

    @app.route("/auth/logout")
    @login_required
    def logout():
        """User logout endpoint."""
        logout_user()
        return redirect(url_for("login"))
