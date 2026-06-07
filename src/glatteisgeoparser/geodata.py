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
    has_context: bool


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
    ) -> None:
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
        if (
            isinstance(configs.admin_rank, str)
            and configs.admin_rank not in gdf.columns
        ):
            raise ValueError("Admin rank column not in GeoDataFrame")
        if configs.population_column and configs.population_column not in gdf.columns:
            raise ValueError("Population column not in GeoDataFrame")

        simplified_gdf = gdf.copy(deep=True)

        # removes null name rows
        simplified_gdf = simplified_gdf[simplified_gdf[configs.names_col].notnull()]
        if not isinstance(simplified_gdf, gpd.GeoDataFrame):
            raise ValueError(
                f"All rows in {configs.names_col} column are null for gazetteer {configs.name}"
            )

        simplified_gdf = simplified_gdf.to_crs("EPSG:4326")

        # sets administrative rank to int for whole gazetteer,
        # or sets administrative rank column name
        if isinstance(configs.admin_rank, int):
            simplified_gdf["gaz_admin_rank"] = configs.admin_rank
            admin_rank = "gaz_admin_rank"
        elif isinstance(configs.admin_rank, str):
            pass
        else:
            raise TypeError("Admin rank must be str or int")

        # sets population column to int for whole gazetteer,
        # or sets population column name
        if configs.population_column is None:
            simplified_gdf["gaz_population"] = 0
            configs.population_column = "gaz_population"
        elif isinstance(configs.population_column, str):
            pass
        else:
            raise TypeError("Population column must be str or None")

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

    def _token_similarity(
        self, candidate: str, gazetteer_name: str, min_overlap: float = 0.8
    ) -> bool:
        """Check if candidate contains most tokens from gazetteer name.

        Arguments:
        candidate: The candidate string to search for
        gazetteer_name: The gazetteer entry to match against
        min_overlap: Minimum ratio of gazetteer tokens that must be in candidate (0.0-1.0)

        Returns:
        True if tokens sufficiently overlap, False otherwise
        """
        candidate_tokens = set(candidate.split())
        gazetteer_tokens = set(gazetteer_name.split())

        # If gazetteer is a subset of candidate tokens, it's a match
        if gazetteer_tokens.issubset(candidate_tokens):
            return True

        # Check overlap ratio
        if len(gazetteer_tokens) == 0:
            return len(candidate_tokens) == 0

        overlap = len(candidate_tokens & gazetteer_tokens) / len(gazetteer_tokens)
        return overlap >= min_overlap

    def get_candidates(
        self,
        candidates: List[str],
        use_token_matching: bool = True,
        token_overlap_ratio: float = 0.8,
    ) -> gpd.GeoDataFrame | None:
        """Get candidate locations from the gazetteer.

        Arguments:
        candidates: List of location names to search for
        use_token_matching: If True, use token-based matching for flexibility.
                          If False, use exact matching (default)
        token_overlap_ratio: Minimum ratio of tokens that must match (0.0-1.0).
                            Only used if use_token_matching=True.

        Returns:
        GeoDataFrame with matching candidates, or None if no matches found
        """
        candidates = [standardize_name(c) for c in candidates]

        if not use_token_matching:
            # Exact match (original behavior)
            df = self.combined_gazetteer[
                self.combined_gazetteer["standardized_names"].isin(candidates)
            ]
        else:
            # Token-based matching
            def matches_any_candidate(gaz_name: str) -> bool:
                return any(
                    self._token_similarity(c, gaz_name, token_overlap_ratio)
                    for c in candidates
                )

            mask = self.combined_gazetteer["standardized_names"].apply(
                matches_any_candidate
            )
            df = self.combined_gazetteer[mask]

        # if df is None or df.empty or type(df) is not gpd.GeoDataFrame:
        if df.empty or not isinstance(df, gpd.GeoDataFrame):
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


__all__ = ["GeoData"]
