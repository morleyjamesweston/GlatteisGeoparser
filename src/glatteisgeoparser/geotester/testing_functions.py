from dataclasses import dataclass

import pandas as pd

from .web_app.models import Geoparsers, MachineCoding, db, get_db_session


@dataclass
class GeoParserAgreementMetrics:
    location_id_assigned_ratio: float
    inter_geoparser_agreement_ratio: float
    gazetteer_distribution: list
    avg_unique_location_ids_per_content_id: float
    avg_unique_location_ids_per_location_name: float
    entries_with_location_id_per_geoparser: list
    entries_without_location_id_per_geoparser: list
    top_10_common_location_ids: list


def get_inter_geoparser_agreement(machine_coding_df: pd.DataFrame):
    pass
    # Get the following:
    # 1. The ratio of machine coding entries that have a location_id assigned (i.e., not null) to the total number of machine coding entries.
    # 2. The ratio of agreement between different geoparsers for entries that have a location_id assigned. Agreement can be defined as the percentage of entries where the location_id is the same across different geoparsers for the same content_id and location_name.
    # 3. The distribution of gazetteers used for entries with a location_id assigned.
    # 4. The average number of unique location_ids assigned per content_id for entries with a location_id assigned.
    # 5. The average number of unique location_ids assigned per location_name for entries with a location_id assigned.
    # 6 The raw number of entries with a location_id assigned for each geoparser.
    # 7. The raw number of entries without a location_id assigned for each geoparser.
    # 8. The top 10 most common location_ids assigned across all geoparsers for entries with a location_id assigned.

    # Machine coding
    #    id       geoparser_label location_name content_id location_id                gazetteer
    # 0   1  eae9b2add8a088590639        Kanada   39856255         CAN  natural_earth_countries
    # 1   2  eae9b2add8a088590639    Australien   39856255         AUS  natural_earth_countries
    # 2   3  eae9b2add8a088590639    Neuseeland   39856255         NZL  natural_earth_countries
    # 3   4  eae9b2add8a088590639       Staaten   39856255         NaN                      NaN
    # 4   5  eae9b2add8a088590639         China   39856255         NaN                      NaN
