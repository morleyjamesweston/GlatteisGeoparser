import hashlib
import json
from dataclasses import asdict
from typing import TypedDict

import geopandas as gpd
from geopandas import GeoDataFrame

from .configs import (
    GazetteerConfigs,
    RecognizerConfigs,
    ResolverConfigs,
    default_recognizer_configs,
    default_resolver_configs,
)
from .geodata import GeoData
from .recognizer import Recognizer
from .resolver import Resolver


class _Configs(TypedDict):
    language: str
    recognizer: RecognizerConfigs
    resolver: ResolverConfigs


def dict_hash(dictionary: dict) -> str:
    """Create a reproducible hash from a dictionary."""
    # Convert dict to JSON string with sorted keys
    dict_str = json.dumps(dictionary, sort_keys=True, default=str)
    # Create hash
    return hashlib.sha256(dict_str.encode()).hexdigest()


class GlatteisGeoparser:
    def __init__(
        self,
        language: str = "de",
        label: str | None = None,
        recogizer_configs: RecognizerConfigs = default_recognizer_configs,
        resolver_configs: ResolverConfigs = default_resolver_configs,
    ) -> None:
        self.geodata = GeoData()
        self.recognizer = Recognizer(
            language=recogizer_configs.language,
            library=recogizer_configs.method,
            model=recogizer_configs.model,
        )

        self.resolver = Resolver(
            library=resolver_configs.method,
            language=language,
            model=None,
        )

        self.configs: _Configs = {
            "language": language,
            "recognizer": recogizer_configs,
            "resolver": resolver_configs,
        }

        self._label = label

    @property
    def label(self):
        if self._label is not None:
            return self._label
        else:
            return self.configs_to_json()["hash"]

    def configs_to_json(self):
        """
        Convert the current configuration to a JSON-compatible dictionary.
        Primarily used in the geotester.
        """

        # lists all elements of setup for use in testing app
        gazetteers = {
            name: asdict(configs)
            for name, (configs, _) in self.geodata.original_gazetteers.items()
        }
        configs = {
            "language": self.configs["language"],
            "gazetteers": gazetteers,
            "recognizer": asdict(self.configs["recognizer"]),
            "resolver": asdict(self.configs["resolver"]),
        }

        hash_value = dict_hash(configs)[:20]

        return {"hash": hash_value, "configs": configs}

    # Passthrough for add_gazetteer
    def add_gazetteer(
        self,
        gdf: GeoDataFrame,
        configs: GazetteerConfigs,
    ) -> None:
        """
        Add a gazetteer to the geoparser.

        Arguments:
        gdf: GeoDataFrame containing the gazetteer data
        configs: GazetteerConfigs object containing information about the gazetteer

        Example usage:
        configs = GazetteerConfigs(
            name="my_gazetteer",
            index_col="id",
            names_col="name",
            admin_rank=1,
            population_column="population",
            is_contextual=False,
        )
        geoparser.add_gazetteer(gdf, configs)
        """
        self.geodata.add_gazetteer(gdf, configs)

    def parse(self, text: str) -> gpd.GeoDataFrame | None:

        if not self.geodata.original_gazetteers:
            raise Exception("No gazetteers loaded")

        candidates = self.recognizer(text)
        candidates = self.geodata.get_candidates(candidates)
        if candidates is None:
            return None
        else:
            candidates = self.resolver(text, candidates)
            return candidates


__all__ = ["GlatteisGeoparser"]
