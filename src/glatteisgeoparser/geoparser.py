import geopandas as gpd
from geopandas import GeoDataFrame

from .configs import (
    GazetteerConfigs,
    RecognizerConfigs,
    default_recognizer_configs,
    default_resolver_configs,
)
from .geodata import GeoData
from .recognizer import Recognizer
from .resolver import Resolver
from .utilities import standardize_name


class GlatteisGeoparser:
    def __init__(
        self, recogizer_configs: RecognizerConfigs = default_recognizer_configs
    ) -> None:
        self.geodata = GeoData()
        self.recognizer = Recognizer(
            language=recogizer_configs.language,
            library=recogizer_configs.method,
            model=recogizer_configs.model,
        )

        self.resolver = Resolver(
            library=default_resolver_configs.method,
            language="de",
            model=None,
        )

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
        candidates = [standardize_name(c) for c in candidates]
        candidates = self.geodata.get_candidates(candidates)
        if candidates is None:
            return None
        else:
            candidates = self.resolver(text, candidates)
            return candidates


__all__ = ["GlatteisGeoparser"]
