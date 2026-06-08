from dataclasses import dataclass
from pprint import pprint

import pandas as pd


@dataclass
class GeoParserAgreementMetrics:
    location_id_assigned_ratio_per_geoparser: list
    inter_geoparser_agreement_ratio: list
    gazetteer_distribution_per_geoparser: list
    avg_unique_location_ids_per_content_id: float
    entries_with_location_id_per_geoparser: list
    entries_without_location_id_per_geoparser: list
    top_10_common_location_ids_per_geoparser: list


def get_inter_geoparser_agreement(machine_coding_df: pd.DataFrame):
    """Calculate inter-geoparser agreement metrics.

    Args:
        machine_coding_df: DataFrame with columns: id, geoparser_label, location_name,
                          content_id, location_id, gazetteer

    Returns:
        GeoParserAgreementMetrics object with all calculated metrics
    """

    # 1. Ratio of entries with location_id assigned per geoparser
    location_id_assigned_ratio_per_geoparser = []
    for geoparser in machine_coding_df["geoparser_label"].unique():
        geoparser_df = machine_coding_df[
            machine_coding_df["geoparser_label"] == geoparser
        ]
        total = len(geoparser_df)
        with_id = geoparser_df["location_id"].notna().sum()
        ratio = with_id / total if total > 0 else 0
        location_id_assigned_ratio_per_geoparser.append(
            {"geoparser_label": geoparser, "ratio": ratio}
        )

    # Filter to only entries with location_id for further calculations
    df_with_id = machine_coding_df[machine_coding_df["location_id"].notna()].copy()

    # 2. Inter-geoparser agreement ratio for every pair of geoparsers
    geoparsers = machine_coding_df["geoparser_label"].unique()
    inter_geoparser_agreement_ratio = []

    for i, geoparser1 in enumerate(geoparsers):
        for geoparser2 in geoparsers[i + 1 :]:
            # Get entries for both geoparsers
            df1 = df_with_id[df_with_id["geoparser_label"] == geoparser1].copy()
            df2 = df_with_id[df_with_id["geoparser_label"] == geoparser2].copy()

            # Find common content_id and location_name pairs
            df1_set = df1.set_index(["content_id", "location_name"])["location_id"]
            df2_set = df2.set_index(["content_id", "location_name"])["location_id"]

            common_indices = df1_set.index.intersection(df2_set.index)

            if len(common_indices) > 0:
                # Count agreements
                agreements = (df1_set[common_indices] == df2_set[common_indices]).sum()
                agreement_ratio = agreements / len(common_indices)
            else:
                agreement_ratio = 0

            inter_geoparser_agreement_ratio.append(
                {
                    "geoparser1": geoparser1,
                    "geoparser2": geoparser2,
                    "agreement_ratio": agreement_ratio,
                    "common_entries": len(common_indices),
                }
            )

    # 3. Gazetteer distribution per geoparser
    gazetteer_distribution_per_geoparser = []
    for geoparser in geoparsers:
        geoparser_with_id = df_with_id[df_with_id["geoparser_label"] == geoparser]
        gazetteer_dist = geoparser_with_id["gazetteer"].value_counts().to_dict()
        gazetteer_list = [
            {"gazetteer": k, "count": v} for k, v in gazetteer_dist.items()
        ]
        gazetteer_distribution_per_geoparser.append(
            {"geoparser_label": geoparser, "gazetteer_distribution": gazetteer_list}
        )

    # 4. Average number of unique location_ids per content_id
    if len(df_with_id) > 0:
        unique_ids_per_content = df_with_id.groupby("content_id")[
            "location_id"
        ].nunique()
        avg_unique_location_ids_per_content_id = unique_ids_per_content.mean()
    else:
        avg_unique_location_ids_per_content_id = 0

    # 5. Raw number of entries with location_id per geoparser
    entries_with_location_id_per_geoparser = (
        df_with_id["geoparser_label"].value_counts().to_dict()
    )
    entries_with_location_id_per_geoparser = [
        {"geoparser_label": k, "count": v}
        for k, v in entries_with_location_id_per_geoparser.items()
    ]

    # 6. Raw number of entries without location_id per geoparser
    df_without_id = machine_coding_df[machine_coding_df["location_id"].isna()]
    entries_without_location_id_per_geoparser = (
        df_without_id["geoparser_label"].value_counts().to_dict()
    )
    entries_without_location_id_per_geoparser = [
        {"geoparser_label": k, "count": v}
        for k, v in entries_without_location_id_per_geoparser.items()
    ]

    # 7. Top 10 most common location_ids per geoparser
    top_10_common_location_ids_per_geoparser = []
    for geoparser in geoparsers:
        geoparser_with_id = df_with_id[df_with_id["geoparser_label"] == geoparser]
        top_location_ids = (
            geoparser_with_id["location_id"].value_counts().head(10).to_dict()
        )
        top_10_list = [
            {"location_id": k, "count": v} for k, v in top_location_ids.items()
        ]
        top_10_common_location_ids_per_geoparser.append(
            {"geoparser_label": geoparser, "top_10_location_ids": top_10_list}
        )

    metrics = GeoParserAgreementMetrics(
        location_id_assigned_ratio_per_geoparser=location_id_assigned_ratio_per_geoparser,
        inter_geoparser_agreement_ratio=inter_geoparser_agreement_ratio,
        gazetteer_distribution_per_geoparser=gazetteer_distribution_per_geoparser,
        avg_unique_location_ids_per_content_id=avg_unique_location_ids_per_content_id,
        entries_with_location_id_per_geoparser=entries_with_location_id_per_geoparser,
        entries_without_location_id_per_geoparser=entries_without_location_id_per_geoparser,
        top_10_common_location_ids_per_geoparser=top_10_common_location_ids_per_geoparser,
    )

    pprint(metrics)
    return metrics
