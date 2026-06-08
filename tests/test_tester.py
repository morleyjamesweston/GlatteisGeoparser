import geopandas as gpd
import pandas as pd
import pytest

from glatteisgeoparser import (
    GazetteerConfigs,
    GeoTesterConfigs,
    GlatteisGeoparser,
    GlatteisGeoTester,
)


def test_geotester():
    testing_data = pd.read_csv("./tests/test_data/glatteis_sample.csv")

    gigp1 = GlatteisGeoparser()
    ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")

    configs = GazetteerConfigs(
        name="natural_earth_countries",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        population_column="POP_EST",
        admin_rank=3,
        is_contextual=True,
    )

    gigp1.add_gazetteer(
        gdf=ne_countries,
        configs=configs,
    )

    cantons = gpd.read_file("./tests/test_data/swiss_govt_data/cantons.geojson")
    cantons = cantons.to_crs("EPSG:4326")

    configs = GazetteerConfigs(
        name="swissCantons",
        index_col="KANTONSNUM",
        names_col="NAME",
        population_column="EINWOHNERZ",
        admin_rank=3,
        is_contextual=True,
    )

    gigp1.add_gazetteer(gdf=cantons, configs=configs)

    districts = gpd.read_file("./tests/test_data/swiss_govt_data/districts.geojson")
    districts = districts.to_crs("EPSG:4326")

    configs = GazetteerConfigs(
        name="swissDistricts",
        index_col="BEZIRKSNUM",
        names_col="NAME",
        population_column="EINWOHNERZ",
        admin_rank=2,
        is_contextual=False,
    )

    gigp1.add_gazetteer(gdf=districts, configs=configs)

    munis = gpd.read_file("./tests/test_data/swiss_govt_data/municipalities.geojson")
    munis = munis.to_crs("EPSG:4326")

    configs = GazetteerConfigs(
        name="swissMunicipalities",
        index_col="BFS_NUMMER",
        names_col="NAME",
        population_column="EINWOHNERZ",
        admin_rank=1,
        is_contextual=False,
    )

    gigp1.add_gazetteer(
        gdf=munis,
        configs=configs,
    )

    populated_places = gpd.read_file("./tests/test_data/ne_110m_populated_places.zip")

    configs = GazetteerConfigs(
        name="naturalEarthPopulatedPlaces",
        index_col="WOF_ID",
        names_col="NAME_DE",
        population_column="POP_MIN",
        admin_rank=4,
        is_contextual=False,
    )

    gigp1.add_gazetteer(
        gdf=populated_places,
        configs=configs,
    )

    gigp2 = GlatteisGeoparser()
    ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")

    configs = GazetteerConfigs(
        name="natural_earth_countries",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        population_column="POP_EST",
        admin_rank=3,
        is_contextual=True,
    )

    gigp2.add_gazetteer(
        gdf=ne_countries,
        configs=configs,
    )

    tester = GlatteisGeoTester(configs=GeoTesterConfigs(), geoparsers=[gigp1, gigp2])
    tester.test_geoparsers(testing_data=testing_data)
