"""API endpoints for the geotester web app."""

import json
from dataclasses import dataclass
from typing import List

import pandas as pd
from flask import jsonify, request
from flask_login import current_user
from sqlalchemy import func

from glatteisgeoparser import GlatteisGeoparser
from glatteisgeoparser.geotester.web_app.models import (
    Geoparsers,
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
            results = data.get("resolutions", {})
            if results == "none_found":
                coding_entry = ManualCoding(
                    user_id=current_user.id,
                    content_id=data.get("id", None),
                    location_name="no_locations_found",
                    location_id=None,
                    gazetteer=None,
                )
                session.add(coding_entry)
                session.commit()
                return jsonify(
                    {"message": "Submission received successfully", "success": True}
                )
            else:
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


def register_dashboard_routes(
    app, testing_data: pd.DataFrame, geoparsers: List[GlatteisGeoparser]
):
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
                "user_id": item.user_id,
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

        total_locs_per_geoparser = get_total_locs_per_geoparser(machine_coding_df)
        unresolved_locs_per_geoparser = get_most_common_unresolved_locs_per_geoparser(
            machine_coding_df
        )

        return jsonify(
            {
                "total_locs_per_geoparser": total_locs_per_geoparser,
                "unresolved_locs_per_geoparser": unresolved_locs_per_geoparser,
            }
        ), 200

    @app.route("/api/dashboard/geoparser_accuracies", methods=["GET"])
    def get_all_geoparser_accuracies():
        session = get_db_session(app)
        geoparsers = session.query(Geoparsers).all()
        geoparsers = [g.label for g in geoparsers]
        print(geoparsers)

        manual_coding_df = pd.read_sql(session.query(ManualCoding).statement, db.engine)

        all_geoparser_accuracies = {}
        for geoparser_id in geoparsers:
            machine_coding_df = pd.read_sql(
                session.query(MachineCoding)
                .filter(MachineCoding.geoparser_label == geoparser_id)
                .statement,
                db.engine,
            )
            accuracy = calculate_geoparser_accuracy(machine_coding_df, manual_coding_df)
            all_geoparser_accuracies[geoparser_id] = accuracy

        return jsonify(all_geoparser_accuracies), 200

    @app.route("/api/dashboard/geoparser_accuracy/<geoparser_id>", methods=["GET"])
    def get_geoparser_accuracy(geoparser_id):
        session = get_db_session(app)

        if not geoparser_id:
            return jsonify(
                {"message": "geoparser_id is required", "success": False}
            ), 400

        machine_coding_df = pd.read_sql(
            session.query(MachineCoding)
            .filter(MachineCoding.geoparser_label == geoparser_id)
            .statement,
            db.engine,
        )
        manual_coding_df = pd.read_sql(session.query(ManualCoding).statement, db.engine)

        accuracy = calculate_geoparser_accuracy(machine_coding_df, manual_coding_df)
        return jsonify(accuracy), 200

    @app.route("/api/dashboard/loc_geodata", methods=["GET"])
    def get_geodata_for_locations():
        content_id = request.args.get("content_id")
        if not content_id:
            return jsonify(
                {"message": "location_name is required", "success": False}
            ), 400

        # query db for article locations
        session = get_db_session(app)
        machine_coding_df = pd.read_sql(
            session.query(MachineCoding).statement, db.engine
        )
        manual_coding_df = pd.read_sql(session.query(ManualCoding).statement, db.engine)

        print(machine_coding_df)
        print(manual_coding_df)

        return {}, 200

    @app.route("/api/dashboard/geoparser_configs", methods=["GET"])
    def get_geoparser_configs():
        session = get_db_session(app)

        geoparser_configs = session.query(Geoparsers).all()

        geoparser_configs = [
            {"label": gp.label, "configs_json": json.loads(gp.configs_json)}
            for gp in geoparser_configs
        ]
        return jsonify(geoparser_configs), 200


@dataclass
class AccuracyResult:
    precision: float
    recall: float
    f1_score: float


def calculate_geoparser_accuracy(
    machine_coding_df: pd.DataFrame, manual_coding_df: pd.DataFrame
) -> AccuracyResult:
    """Calculate precision, recall, and F1 for a geoparser against human annotations.

    Matching is set-based per content_id: a machine-coded location_name is a true
    positive when it also appears in the human-coded set for the same content_id.
    Duplicate location_names within the same content_id are counted only once (set
    semantics).  The sentinel value ``"no_locations_found"`` is excluded from all
    counts.

    Args:
        machine_coding_df: Rows produced by the geoparser under evaluation.
            Expected columns: ``location_name``, ``content_id``.
        manual_coding_df: Rows produced by human annotators.
            Expected columns: ``location_name``, ``content_id``.

    Returns:
        An :class:`AccuracyResult` with precision, recall, and F1 in [0, 1].
    """
    NO_LOC = "no_locations_found"

    # Drop the sentinel and deduplicate (same name, different gazetteer rows)
    machine = machine_coding_df[
        machine_coding_df["location_name"] != NO_LOC
    ].drop_duplicates(subset=["content_id", "location_name"])[
        ["content_id", "location_name"]
    ]
    manual = manual_coding_df[
        manual_coding_df["location_name"] != NO_LOC
    ].drop_duplicates(subset=["content_id", "location_name"])[
        ["content_id", "location_name"]
    ]

    # Build per-content_id sets for fast lookup
    machine_sets: dict[str, set[str]] = (
        machine.groupby("content_id")["location_name"].apply(set).to_dict()
    )
    manual_sets: dict[str, set[str]] = (
        manual.groupby("content_id")["location_name"].apply(set).to_dict()
    )

    all_content_ids = set(machine_sets) | set(manual_sets)

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for content_id in all_content_ids:
        machine_locs = machine_sets.get(content_id, set())
        manual_locs = manual_sets.get(content_id, set())

        tp = len(machine_locs & manual_locs)
        fp = len(machine_locs - manual_locs)
        fn = len(manual_locs - machine_locs)

        total_tp += tp
        total_fp += fp
        total_fn += fn

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return AccuracyResult(precision=precision, recall=recall, f1_score=f1)


def get_most_common_unresolved_locs_per_geoparser(df: pd.DataFrame):
    """
    Gets the top 20 most common unresolved locations per geoparser.
    with the name and count per location and geoparser.
    """
    most_common_unresolved_locs_per_geoparser = {}

    # Filter for unresolved locations (where location_id is NaN)
    unresolved_df = df[df["location_id"].isna()]

    # Group by geoparser_label
    for gp_label, geoparser_df in unresolved_df.groupby("geoparser_label"):
        # Get value counts of location_name and take top 20
        top_20_unresolved = geoparser_df["location_name"].value_counts().head(20)

        # Convert to list of dicts with name and count
        most_common_unresolved_locs_per_geoparser[gp_label] = [
            {"name": location_name, "count": int(count)}
            for location_name, count in top_20_unresolved.items()
        ]

    return most_common_unresolved_locs_per_geoparser


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
