import os
from pprint import pprint

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from glatteisgeoparser.geodata import GeoData


def create_tester_app(testing_data: pd.DataFrame, geodata: GeoData):
    """Create and configure the testing framework Flask app."""

    print("Testing data received in create_tester_app:")
    print(testing_data.head())

    print("Geodata received in create_tester_app:")
    print(geodata.combined_gazetteer.head())

    # Get the path to the tester module's directory
    tester_module_path = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(tester_module_path, "static")

    # Create Flask app
    app = Flask(
        "glatteisgeoparser.testing_framework.tester",
    )

    CORS(app)

    # --------------------
    # API ENDPOINTS
    # --------------------

    # serve the next contents
    @app.route("/api/next_content", methods=["GET"])
    def next_content():
        random_row = testing_data.sample(n=1)
        return jsonify(random_row.to_dict(orient="records")[0])

    @app.route("/api/get_geodata", methods=["GET"])
    def get_geodata():
        return jsonify(geodata.combined_gazetteer.to_json())

    # get potential locations from a location name
    @app.route("/api/get_location_choices", methods=["GET"])
    def get_potential_locations():
        location = request.args.get("location")
        if location:
            candidates = geodata.get_candidates([location])
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
