import os

import pandas as pd
from flask import Flask, jsonify, send_from_directory


def create_tester_app(testing_data: pd.DataFrame):
    """Create and configure the testing framework Flask app."""

    print("Testing data received in create_tester_app:")
    print(testing_data.head())

    # Get the path to the tester module's directory
    tester_module_path = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(tester_module_path, "static")

    # Create Flask app
    app = Flask(
        "glatteisgeoparser.testing_framework.tester",
    )

    # --------------------
    # API ENDPOINTS
    # --------------------
    # api endpoint to serve a random line from testing_data
    @app.route("/api/random_line", methods=["GET"])
    def random_line():
        random_row = testing_data.sample(n=1)
        return jsonify(random_row.to_dict(orient="records")[0])

    # --------------------
    # SERVE WEBSITE
    # --------------------
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
