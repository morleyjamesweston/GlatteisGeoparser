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
        pass

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


__all__ = ["GlatteisConfigs", "GlatteisGeoparser", "GazetteerConfigs"]
