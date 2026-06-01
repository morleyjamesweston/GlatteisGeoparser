from itertools import permutations
from typing import Dict, Iterable, List, NamedTuple, Tuple

import flashtext
import geopandas as gpd
import pandas as pd
from shapely.geometry.base import BaseGeometry

from .configs import GazetteerConfigs
from .utilities import standardize_name


class _GazetteerRow(NamedTuple):
    """Type definition for gazetteer rows from itertuples()."""

    Index: int
    original_index: str
    original_names: str
    admin_rank: int
    population_column: int
    standardized_names: str
    geometry: BaseGeometry
    gazetteer_name: str
    is_contextual: bool


class GeoData:
    def __init__(self) -> None:
        self.keywords = flashtext.KeywordProcessor()
        self.original_gazetteers: Dict[
            str, Tuple[GazetteerConfigs, gpd.GeoDataFrame]
        ] = {}
        self.combined_gazetteer = gpd.GeoDataFrame()

    def _add_keywords(self, keywords: Iterable[str]) -> None:
        for keyword in keywords:
            self.keywords.add_keyword(keyword)

    def _candidate_exists(self, candidate: str) -> bool:
        cands = self.keywords.extract_keywords(candidate)
        return len(cands) > 0

    def add_gazetteer(
        self,
        gdf: gpd.GeoDataFrame,
        configs: GazetteerConfigs,
    ):
        """
        Add a gazetteer to the geoparser.

        Arguments:
        gdf: GeoDataFrame containing the gazetteer data
        configs: GazetteerConfigs object containing information about the gazetteer
        """

        # Basic checks to make sure the provided GeoDataFrame has the necessary columns
        if configs.index_col not in gdf.columns:
            raise ValueError("Index column not in GeoDataFrame")
        if configs.names_col not in gdf.columns:
            raise ValueError("Names column not in GeoDataFrame")
        if type(configs.admin_rank) is str and configs.admin_rank not in gdf.columns:
            raise ValueError("Admin rank column not in GeoDataFrame")
        if configs.population_column and configs.population_column not in gdf.columns:
            raise ValueError("Population column not in GeoDataFrame")
        pass

        simplified_gdf = gdf.copy(deep=True)

        # removes null name rows
        simplified_gdf = simplified_gdf[simplified_gdf[configs.names_col].notnull()]
        if type(simplified_gdf) is not gpd.GeoDataFrame:
            raise ValueError("")

        simplified_gdf = simplified_gdf.to_crs("EPSG:4326")

        # sets administrative rank to int for whole gazetteer,
        # or sets administrative rank column name
        if isinstance(configs.admin_rank, str):
            pass
        elif isinstance(configs.admin_rank, int):
            simplified_gdf["gaz_admin_rank"] = configs.admin_rank
            admin_rank = "gaz_admin_rank"
        else:
            raise TypeError("Admin rank must be str or int")

        # sets population column to int for whole gazetteer,
        # or sets population column name
        if configs.population_column is None:
            simplified_gdf["gaz_population"] = 0
            configs.population_column = "gaz_population"
        elif isinstance(configs.population_column, str):
            pass

        # sets standardized name column
        simplified_gdf["standardized_names"] = [
            standardize_name(n) for n in simplified_gdf[configs.names_col]
        ]

        # # only gets needed columns for slim gazetteer
        simplified_gdf = simplified_gdf[
            [
                configs.index_col,
                configs.names_col,
                admin_rank,
                configs.population_column,
                "standardized_names",
                "geometry",
            ]
        ]

        # This is to keep type checker happy
        simplified_gdf = gpd.GeoDataFrame(simplified_gdf)

        # Inplace to keep typing happy
        simplified_gdf.rename(
            columns={
                configs.index_col: "original_index",
                configs.names_col: "original_names",
                admin_rank: "admin_rank",
                configs.population_column: "population_column",
            },
            inplace=True,
        )

        simplified_gdf["gazetteer_name"] = configs.name
        simplified_gdf["is_contextual"] = configs.is_contextual

        self.original_gazetteers[configs.name] = (configs, gdf)

        self.combined_gazetteer = pd.concat(
            [self.combined_gazetteer, simplified_gdf], ignore_index=True
        )

        self._add_keywords(simplified_gdf["original_names"].tolist())
        self._add_keywords(simplified_gdf["standardized_names"].tolist())

    def get_candidates(self, candidates: List[str]) -> gpd.GeoDataFrame | None:
        # candidates = [c for c in text if self._candidate_exists(c)]

        df = self.combined_gazetteer[
            self.combined_gazetteer["standardized_names"].isin(candidates)
        ]

        if df is None or df.empty or type(df) is not gpd.GeoDataFrame:
            return None

        df["has_context"] = False

        for row_a, row_b in permutations(df.itertuples(index=True, name="Row"), 2):
            row_a_cast = _GazetteerRow(*row_a)
            row_b_cast = _GazetteerRow(*row_b)
            if row_a_cast.standardized_names == row_b_cast.standardized_names:
                continue
            if not row_b_cast.is_contextual:
                continue
            if row_a_cast.admin_rank <= row_b_cast.admin_rank:
                continue
            if row_a_cast.geometry.centroid.within(row_b_cast.geometry):
                df.loc[row_a_cast.Index, "has_context"] = True
                df.loc[row_b_cast.Index, "has_context"] = True

        return df
