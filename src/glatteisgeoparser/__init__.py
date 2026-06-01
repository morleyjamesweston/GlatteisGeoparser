from geopandas import GeoDataFrame

from .configs import GazetteerConfigs, GlatteisConfigs, default_configs
from .geodata import GeoData
from .recognizer import Recognizer


class GlatteisGeoparser:
    def __init__(self, configs: GlatteisConfigs = default_configs) -> None:
        self.geodata = GeoData()
        self.recognizer = Recognizer(
            language=configs.language, library=configs.library, model=configs.model
        )
        pass

    # Passthrough for add_gazetteer
    def add_gazetteer(
        self,
        gdf: GeoDataFrame,
        configs: GazetteerConfigs,
    ) -> None:
        self.geodata.add_gazetteer(gdf, configs)


__all__ = ["GlatteisConfigs", "GlatteisGeoparser", "GazetteerConfigs"]
