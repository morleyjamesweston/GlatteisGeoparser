"""API endpoints for the geotester web app."""

from pprint import pprint
from typing import List

import pandas as pd
from flask import jsonify, request
from flask_login import current_user

from glatteisgeoparser import GlatteisGeoparser
from glatteisgeoparser.geotester.web_app.models import ManualCoding, get_db_session


def register_code_routes(
    app, testing_data: pd.DataFrame, geoparsers: List[GlatteisGeoparser]
):
    """Register API routes to the Flask app."""

    @app.route("/api/next_content", methods=["GET"])
    def next_content():
        """Get a random content item from the testing data."""
        random_row = testing_data.sample(n=1)
        return jsonify(random_row.to_dict(orient="records")[0])

    @app.route("/api/get_location_choices", methods=["GET"])
    def get_potential_locations():
        """Get potential location candidates for a given location name."""
        location = request.args.get("location")
        if location:
            all_candidates = pd.DataFrame()

            for geoparser in geoparsers:
                label = geoparser.label
                candidates = geoparser.geodata.get_candidates([location])
                if candidates is not None:
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
        """Handle submission of test results."""
        data = request.get_json()

        if current_user.is_authenticated:
            pprint(f"Received submission data: {data}")
            session = get_db_session(app)
            for resolution in data.get("resolutions", {}).values():
                # pprint(f"Processing resolution for location: {resolution}")
                print("RESOLUTION IS:")
                pprint(resolution)
                if resolution is None:
                    pass
                else:
                    coding_entry = ManualCoding(
                        user_id=current_user.id,
                        content_id=data.get("id", None),
                        location_name=resolution.get("original_names", ""),
                        location_id=resolution.get("original_index", ""),
                        gazetteer=resolution.get("gazetteer_name", ""),
                    )
                    pprint(f"Created coding entry: {coding_entry}")
                    session.add(coding_entry)
            session.commit()

            return jsonify(
                {"message": "Submission received successfully", "success": True}
            )
        else:
            print("User not authenticated")
            return jsonify({"message": "User not authenticated", "success": False}), 401
