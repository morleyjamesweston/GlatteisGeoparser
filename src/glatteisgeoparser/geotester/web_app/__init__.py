import os
from pprint import pprint
from typing import List

import flask_login
import pandas as pd
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from glatteisgeoparser import GlatteisGeoparser

users = {"foo@bar.tld": {"password": "secret"}}


def initialize_web_app(testing_data: pd.DataFrame, geoparsers: List[GlatteisGeoparser]):
    """Create and configure the testing framework Flask app."""
    # Get the path to the tester module's directory
    tester_module_path = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(tester_module_path, "static")

    # Create Flask app
    app = Flask(
        "glatteisgeoparser.testing_framework.tester",
    )

    # Initialize Flask app
    # app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "supersecretkey"

    # Initialize database and login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    db = SQLAlchemy(app)

    # User model
    class Users(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(250), unique=True, nullable=False)
        password = db.Column(db.String(250), nullable=False)

    # Create database
    with app.app_context():
        db.create_all()

    # Load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # Register route
    @app.route("/auth/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if Users.query.filter_by(username=username).first():
                print(f"Registration failed: Username '{username}' already taken")
                return jsonify(
                    {"success": False, "error": "Username already taken"}
                ), 400

            if password:
                hashed_password = generate_password_hash(
                    password, method="pbkdf2:sha256"
                )
            else:
                print("registration failed")
                return jsonify(
                    {"success": False, "error": "Invalid username or password"}
                ), 401

            new_user = Users(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("login"))
        return send_from_directory(static_folder, "auth/register.html")

    # Login route
    @app.route("/auth/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            # Handle JSON data from SvelteKit frontend
            print("Received login request with content type:", request.content_type)
            if request.is_json:
                data = request.get_json()
                username = data.get("username")
                password = data.get("password")
            else:
                # Handle traditional form data
                username = request.form.get("username")
                password = request.form.get("password")

            user = Users.query.filter_by(username=username).first()

            if user and password and check_password_hash(user.password, password):
                login_user(user)
                return jsonify({"success": True, "message": "Login successful"})
            else:
                print(f"Login failed for username: {username}")
                print(
                    f"User found: {user is not None}, Password provided: {password is not None}"
                )
                return jsonify(
                    {"success": False, "error": "Invalid username or password"}
                ), 401

        return send_from_directory(static_folder, "auth/login.html")

    # Protected dashboard route
    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html", username=current_user.username)

    # Logout route
    @app.route("/auth/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    # Enable CORS for all routes
    CORS(app, supports_credentials=True)

    if __name__ == "__main__":
        app.run(debug=True)

    # --------------------
    # API ENDPOINTS
    # --------------------
    # serve the next contents
    @app.route("/api/next_content", methods=["GET"])
    def next_content():
        random_row = testing_data.sample(n=1)
        return jsonify(random_row.to_dict(orient="records")[0])

    # @app.route("/api/get_geodata", methods=["GET"])
    # def get_geodata():
    #     return jsonify(geodata.combined_gazetteer.to_json())

    # get potential locations from a location name
    @app.route("/api/get_location_choices", methods=["GET"])
    def get_potential_locations():
        location = request.args.get("location")
        if location:
            all_candidates = pd.DataFrame()

            for geoparser in geoparsers:
                label = geoparser.label
                candidates = geoparser.geodata.get_candidates([location])
                if candidates:
                    candidates["geoparser"] = label
                    all_candidates = pd.concat(
                        [all_candidates, candidates], ignore_index=True
                    )

            if candidates is not None and not candidates.empty:
                return jsonify(candidates.to_json())
            else:
                return jsonify({"message": f"No candidates found for '{location}'"})

        else:
            return jsonify({"error": "No location parameter provided"})

    @app.route("/api/submit", methods=["POST"])
    def submit():
        data = request.get_json()
        print("Received submission:")
        pprint(data)
        return jsonify({"message": "Submission received successfully"})

    # --------------------
    # SERVE WEBSITE
    # --------------------
    # prioritize static file routes before the catch-all route
    @app.route("/code")
    def index():
        print("Serving index.html for /code route")
        return send_from_directory(static_folder, "code.html")

    @app.route("/<path:filepath>")
    def serve_static(filepath):
        file_path = os.path.join(static_folder, filepath)
        if os.path.isfile(file_path):
            return send_from_directory(static_folder, filepath)
        return send_from_directory(static_folder, "index.html")

    return app


__all__ = ["create_tester_app"]
