import json
from typing import List

import pandas as pd
from flask import Flask
from tqdm import tqdm

from ..configs import GeoTesterConfigs
from ..geoparser import GlatteisGeoparser
from .web_app import initialize_web_app
from .web_app.models import Geoparsers, MachineCoding, db, get_db_session


class GlatteisGeoTester:
    def __init__(self, configs: GeoTesterConfigs, geoparsers: List[GlatteisGeoparser]):
        self.geoparsers = geoparsers
        self.configs = configs

        # Create app for database access
        self.cli_app = Flask(__name__)
        self.cli_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
        self.cli_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(self.cli_app)
        self.init_db()
        self.save_geoparser_data()

    def init_db(self):
        with self.cli_app.app_context():
            db.create_all()

    def initialize_web_app(self, testing_data: pd.DataFrame):
        return initialize_web_app(testing_data=testing_data, geoparsers=self.geoparsers)

    def save_geoparser_data(self):
        for geoparser in self.geoparsers:
            # insert into db if it doesn't exist
            with self.cli_app.app_context():
                session = get_db_session(self.cli_app)
                existing = (
                    session.query(Geoparsers).filter_by(label=geoparser.label).first()
                )
                print(f"Loaded geoparser {geoparser.label}")
                if not existing:
                    new_entry = Geoparsers(
                        label=geoparser.label,
                        configs_json=json.dumps(
                            geoparser.configs_to_json(), indent=0, ensure_ascii=False
                        ),
                    )
                    session.add(new_entry)
                    session.commit()

    def test_geoparsers(self, testing_data: pd.DataFrame):
        for geoparser in self.geoparsers:
            print(f"Testing geoparser: {geoparser.label}")
            with self.cli_app.app_context():
                session = get_db_session(self.cli_app)
                for line in tqdm(testing_data.to_dict(orient="records")):
                    candidates = geoparser.recognizer(line["content"])
                    parsed_result = geoparser.parse(line["content"])
                    if parsed_result is not None:
                        for result in parsed_result.to_dict(orient="records"):
                            machine_result = MachineCoding(
                                geoparser_label=geoparser.label,
                                content_id=line["id"],
                                location_name=result["original_names"],
                                location_id=result["original_index"],
                                gazetteer=result["gazetteer_name"],
                            )
                            existing = (
                                session.query(MachineCoding)
                                .filter_by(
                                    geoparser_label=machine_result.geoparser_label,
                                    content_id=machine_result.content_id,
                                    location_name=machine_result.location_name,
                                    location_id=machine_result.location_id,
                                    gazetteer=machine_result.gazetteer,
                                )
                                .first()
                            )
                            if not existing:
                                session.add(machine_result)

                        # add candidates that have no results in the parse output
                        for candidate in candidates:
                            if (
                                candidate
                                not in parsed_result["original_names"].tolist()
                            ):
                                machine_result = MachineCoding(
                                    geoparser_label=geoparser.label,
                                    content_id=line["id"],
                                    location_name=candidate,
                                    location_id=None,
                                    gazetteer=None,
                                )
                                existing = (
                                    session.query(MachineCoding)
                                    .filter_by(
                                        geoparser_label=machine_result.geoparser_label,
                                        content_id=machine_result.content_id,
                                        location_name=machine_result.location_name,
                                        location_id=machine_result.location_id,
                                        gazetteer=machine_result.gazetteer,
                                    )
                                    .first()
                                )
                                if not existing:
                                    session.add(machine_result)
                    else:
                        for candidate in candidates:
                            machine_result = MachineCoding(
                                geoparser_label=geoparser.label,
                                content_id=line["id"],
                                location_name=candidate,
                                location_id=None,
                                gazetteer=None,
                            )
                            existing = (
                                session.query(MachineCoding)
                                .filter_by(
                                    geoparser_label=machine_result.geoparser_label,
                                    content_id=machine_result.content_id,
                                    location_name=machine_result.location_name,
                                    location_id=machine_result.location_id,
                                    gazetteer=machine_result.gazetteer,
                                )
                                .first()
                            )
                            if not existing:
                                session.add(machine_result)
                    session.commit()
