"""API endpoints for the geotester web app."""

from pprint import pprint
from typing import List

import pandas as pd
from flask import jsonify, request
from flask_login import current_user
from sqlalchemy import func

from glatteisgeoparser import GlatteisGeoparser
from glatteisgeoparser.geotester.testing_functions import get_inter_geoparser_agreement
from glatteisgeoparser.geotester.web_app.models import (
    MachineCoding,
    ManualCoding,
    Users,
    db,
    get_db_session,
)


def register_code_routes(
    app, testing_data: pd.DataFrame, geoparsers: List[GlatteisGeoparser]
):
    """Register API routes to the Flask app."""

    @app.route("/api/next_content", methods=["GET"])
    def next_content():
        """Get a random content item from the testing data."""
        random_row = testing_data.sample(n=1)
        return jsonify(random_row.to_dict(orient="records")[0])

    @app.route("/api/get_all_content_ids", methods=["GET"])
    def get_all_content_ids():
        """Get all content ids from the testing data."""
        content_ids = testing_data["id"].tolist()
        return jsonify(content_ids)

    @app.route("/api/content", methods=["GET"])
    def get_content_by_id():
        content_id = request.args.get("content_id")
        if content_id:
            content = testing_data[testing_data["id"] == int(content_id)]
            print(content)
            if not content.empty:
                return jsonify(content.to_dict(orient="records")[0])
            else:
                return jsonify({"message": f"No content found for id '{content_id}'"})
        else:
            return jsonify({"message": "No content_id provided"})

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
            session = get_db_session(app)
            for resolution in data.get("resolutions", {}).values():
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
                    session.add(coding_entry)
            session.commit()

            return jsonify(
                {"message": "Submission received successfully", "success": True}
            )
        else:
            print("User not authenticated")
            return jsonify({"message": "User not authenticated", "success": False}), 401


def register_dashboard_routes(app, testing_data: pd.DataFrame):
    """Register dashboard-related API routes."""

    @app.route("/api/dashboard/coding_progress", methods=["GET"])
    def coding_progress():
        """Get summary statistics for the dashboard."""
        session = get_db_session(app)

        total = testing_data.shape[0]
        progress = (
            session.query(
                ManualCoding.user_id, Users.username, func.count(ManualCoding.id)
            )
            .join(Users, ManualCoding.user_id == Users.id)
            .group_by(ManualCoding.user_id, Users.username)
            .all()
        )
        return jsonify(
            {
                "total_test_data": total,
                "coding_progress": [
                    {
                        "user_id": user_id,
                        "username": username,
                        "coded_count": coded_count,
                    }
                    for user_id, username, coded_count in progress
                ],
            }
        ), 200

    @app.route("/api/dashboard/coded/<content_id>", methods=["GET"])
    def get_data_for_article(content_id: str):
        """Get data for a specific article."""
        # content_id = request.args.get("content_id")
        session = get_db_session(app)

        machine_coding = (
            session.query(MachineCoding)
            .filter(MachineCoding.content_id == content_id)
            .all()
        )
        manual_coding = (
            session.query(ManualCoding)
            .filter(ManualCoding.content_id == content_id)
            .all()
        )

        machine_coding_data = [
            {
                "id": item.id,
                "geoparser_label": item.geoparser_label,
                "content_id": item.content_id,
                "location_name": item.location_name,
                "location_id": item.location_id,
            }
            for item in machine_coding
        ]
        manual_coding_data = [
            {
                "id": item.id,
                "geoparser_label": item.geoparser_label,
                "content_id": item.content_id,
                "location_name": item.location_name,
                "location_id": item.location_id,
            }
            for item in manual_coding
        ]

        return jsonify(
            {"machine_coding": machine_coding_data, "manual_coding": manual_coding_data}
        ), 200

    @app.route("/api/dashboard/all_coded", methods=["GET"])
    def get_all_data():
        """Get all manual coding data."""
        session = get_db_session(app)
        machine_coding = session.query(MachineCoding).all()
        manual_coding = session.query(ManualCoding).all()

        machine_coding_data = [
            {
                "id": item.id,
                "geoparser_label": item.geoparser_label,
                "content_id": item.content_id,
                "location_name": item.location_name,
                "location_id": item.location_id,
                "gazetteer": item.gazetteer,
            }
            for item in machine_coding
        ]

        manual_coding_data = [
            {
                "id": item.id,
                "user_id": item.user_id,
                "content_id": item.content_id,
                "location_name": item.location_name,
                "location_id": item.location_id,
                "gazetteer": item.gazetteer,
            }
            for item in manual_coding
        ]

        return jsonify(
            {"machine_coding": machine_coding_data, "manual_coding": manual_coding_data}
        ), 200

        # manual_coding = session.query(MachineCoding).all()

    @app.route("/api/dashboard/geoparser_evaluation", methods=["GET"])
    def geoparser_evaluation():
        session = get_db_session(app)

        machine_coding_df = pd.read_sql(
            session.query(MachineCoding).statement, db.engine
        )
        manual_coding_df = pd.read_sql(session.query(ManualCoding).statement, db.engine)

        print("Machine coding")
        print(machine_coding_df.head())
        print("\n\n Manual coding")
        print(manual_coding_df.head())

        #    id       geoparser_label location_name content_id location_id                gazetteer
        # 0   1  eae9b2add8a088590639        Kanada   39856255         CAN  natural_earth_countries
        # 1   2  eae9b2add8a088590639    Australien   39856255         AUS  natural_earth_countries
        # 2   3  eae9b2add8a088590639    Neuseeland   39856255         NZL  natural_earth_countries
        # 3   4  eae9b2add8a088590639       Staaten   39856255         NaN                      NaN
        # 4   5  eae9b2add8a088590639         China   39856255         NaN                      NaN

        #  Manual coding
        #    id  user_id location_name content_id location_id            gazetteer
        # 0   1        1        Zürich      96723           1         swissCantons
        # 1   2        1        Zürich      96723         261  swissMunicipalities
        # 2   3        1        Zürich      47012         261  swissMunicipalities
        # 3   4        1        Zürich      47012         261  swissMunicipalities
        # 4   5        1      Freiberg      51224         NaN                  NaN

        # igp = get_inter_geoparser_agreement(machine_coding_df)
        # print(igp)
        total_locs_per_geoparser = get_total_locs_per_geoparser(machine_coding_df)

        return jsonify({"total_locs_per_geoparser": total_locs_per_geoparser}), 200


def get_total_locs_per_geoparser(df: pd.DataFrame):
    """
    Gets the total number of resolved and unresolved locations per geoparser.
    A resolved location is one with a location_id
    (i.e., it was successfully matched to a gazetteer entry).
    """
    total_locs_per_geoparser = {}

    # Group by geoparser_label
    for gp_label, geoparser_df in df.groupby("geoparser_label"):
        resolved = geoparser_df["location_id"].notna().sum()
        unresolved = geoparser_df["location_id"].isna().sum()

        total_locs_per_geoparser[gp_label] = {
            "resolved": int(resolved),
            "unresolved": int(unresolved),
        }

    return total_locs_per_geoparser

    #    id       geoparser_label location_name content_id location_id                gazetteer
    # 0   1  eae9b2add8a088590639        Kanada   39856255         CAN  natural_earth_countries
    # 1   2  eae9b2add8a088590639    Australien   39856255         AUS  natural_earth_countries
    # 2   3  eae9b2add8a088590639    Neuseeland   39856255         NZL  natural_earth_countries
    # 3   4  eae9b2add8a088590639       Staaten   39856255         NaN                      NaN
    # 4   5  eae9b2add8a088590639         China   39856255         NaN                      NaN

    # {gp_label: {resolved: 100, unresolved: 200}, ...}
