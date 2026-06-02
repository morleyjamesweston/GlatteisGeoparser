import os

from flask import Flask, send_from_directory  # ty:ignore[unresolved-import]


def create_tester_app():
    """Create and configure the testing framework Flask app."""

    # Get the path to the tester module's directory
    tester_module_path = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(tester_module_path, "static")

    # Create Flask app
    app = Flask(
        "glatteisgeoparser.testing_framework.tester",
    )

    # prioritize static file routes before the catch-all route
    @app.route("/")
    def index():
        return send_from_directory(static_folder, "index.html")

    @app.route("/<path:filepath>")
    def serve_static(filepath):
        file_path = os.path.join(static_folder, filepath)
        if os.path.isfile(file_path):
            return send_from_directory(static_folder, filepath)
        return send_from_directory(static_folder, "index.html")

    return app


__all__ = ["create_tester_app"]
