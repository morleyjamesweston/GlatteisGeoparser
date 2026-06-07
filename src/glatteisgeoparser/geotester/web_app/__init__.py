"""Flask web app for the GlatteisGeoparser testing framework."""

import os
from typing import List

import pandas as pd
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from glatteisgeoparser import GlatteisGeoparser

from .api import register_code_routes
from .auth import register_auth_routes
from .models import Users, db
from .static_routes import register_static_routes


def initialize_web_app(
    testing_data: pd.DataFrame, geoparsers: List[GlatteisGeoparser]
) -> Flask:
    """Create and configure the testing framework Flask app.

    Args:
        testing_data: DataFrame containing test data
        geoparsers: List of GlatteisGeoparser instances

    Returns:
        Configured Flask application
    """
    # Get the path to the tester module's directory
    tester_module_path = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(tester_module_path, "static")

    # Create Flask app
    app = Flask("glatteisgeoparser.testing_framework.tester")

    # Configure Flask app
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "supersecretkey"

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Create database tables
    with app.app_context():
        db.create_all()

    # Load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # Register route blueprints
    register_auth_routes(app, static_folder)
    register_code_routes(app, testing_data, geoparsers)
    register_static_routes(app, static_folder)

    # Enable CORS for all routes
    CORS(app, supports_credentials=True)

    return app


__all__ = ["initialize_web_app"]
