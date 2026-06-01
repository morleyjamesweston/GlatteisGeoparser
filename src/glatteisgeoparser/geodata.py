import geopandas as gpd

from .configs import GazetteerConfigs


class GeoData:
    def __init__(self) -> None:
        pass

    def add_gazetteer(
        self,
        gdf: gpd.GeoDataFrame,
        configs: GazetteerConfigs,
    ):
        pass
