# from .cross_language_tester import CrossLanguageTester
from typing import List

import pandas as pd

from ..configs import GeoTesterConfigs
from ..geoparser import GlatteisGeoparser
from .web_app import initialize_web_app


class GlatteisGeoTester:
    def __init__(self, configs: GeoTesterConfigs, geoparsers: List[GlatteisGeoparser]):
        self.geoparsers = geoparsers
        self.configs = configs

    def initialize_web_app(self, testing_data: pd.DataFrame):
        return initialize_web_app(
            testing_data=testing_data, geodata=self.geoparsers[0].geodata
        )
