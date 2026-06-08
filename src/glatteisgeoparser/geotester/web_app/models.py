"""Database models for the geotester web app."""

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    """User model for authentication."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class ManualCoding(db.Model):
    """Model for manual coding of geoparsing results."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content_id = db.Column(db.String(250), nullable=False)
    location_name = db.Column(db.String(250), nullable=False)
    location_id = db.Column(db.String(250), nullable=False)
    gazetteer = db.Column(db.String(250), nullable=False)


class Geoparsers(db.Model):
    """Model for storing geoparser configurations."""

    label = db.Column(db.String(250), primary_key=True)
    configs_json = db.Column(db.Text, nullable=False)


class MachineCoding(db.Model):
    """Model for storing machine coding results."""

    id = db.Column(db.Integer, primary_key=True)
    geoparser_label = db.Column(
        db.String(250), db.ForeignKey("geoparsers.label"), nullable=False
    )
    content_id = db.Column(db.String(250), nullable=False)
    location_name = db.Column(db.String(250), nullable=False)
    location_id = db.Column(db.String(250), nullable=True)
    gazetteer = db.Column(db.String(250), nullable=True)


def get_db_session(app=None):
    """Get a database session for use outside Flask context.

    Args:
        app: Flask app instance. If None, creates a minimal app for DB access.

    Returns:
        SQLAlchemy session object
    """
    if app is None:
        from flask import Flask

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

    return db.session
