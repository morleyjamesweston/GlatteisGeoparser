import geopandas as gpd
import pandas as pd
import pytest  # ty:ignore[unresolved-import]

from glatteisgeoparser.geodata import GazetteerConfigs, GeoData


def test_init():
    assert GeoData()


def test_add_bad_gazetteers():
    geodata = GeoData()

    ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")

    # Must be geodataframe
    with pytest.raises(ValueError):
        configs = GazetteerConfigs(
            name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank=3,
            is_contextual=False,
        )
        geodata.add_gazetteer(
            gdf=pd.DataFrame(ne_countries),  # ty:ignore[invalid-argument-type]
            configs=configs,
        )

    # Columns aren't in dataframe
    with pytest.raises(ValueError):
        configs = GazetteerConfigs(
            name="natural_earth_countries",
            index_col="NON_EXTANT_COLUMN",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank=3,
            is_contextual=False,
        )
        geodata.add_gazetteer(
            gdf=ne_countries,
            configs=configs,
        )

    # Names column isn't in dataframe
    with pytest.raises(ValueError):
        configs = GazetteerConfigs(
            name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NON_EXTANT_COLUMN",
            population_column="POP_EST",
            admin_rank=3,
            is_contextual=False,
        )
        geodata.add_gazetteer(
            gdf=ne_countries,
            configs=configs,
        )

    # Population column isn't in dataframe
    with pytest.raises(ValueError):
        configs = GazetteerConfigs(
            name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="NON_EXTANT_COLUMN",
            admin_rank=3,
            is_contextual=False,
        )
        geodata.add_gazetteer(
            gdf=ne_countries,
            configs=configs,
        )

    # Admin rank column isn't in dataframe
    with pytest.raises(ValueError):
        configs = GazetteerConfigs(
            name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank="NON_EXTANT_COLUMN",
            is_contextual=False,
        )
        geodata.add_gazetteer(
            gdf=ne_countries,
            configs=configs,
        )

    # Must be int or string
    with pytest.raises(TypeError):
        configs = GazetteerConfigs(
            name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank=1.5,  # ty:ignore[invalid-argument-type]
            is_contextual=False,
        )
        geodata.add_gazetteer(
            gdf=ne_countries,
            configs=configs,
        )


def test_add_correct_gazetteers():
    geodata = GeoData()
    ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")

    configs = GazetteerConfigs(
        name="natural_earth_countries",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        population_column="POP_EST",
        admin_rank=3,
        is_contextual=True,
    )
    geodata.add_gazetteer(
        gdf=ne_countries,
        configs=configs,
    )

    configs = GazetteerConfigs(
        name="natural_earth_countries_2",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        population_column=None,
        admin_rank=3,
        is_contextual=True,
    )
    # Tests both admin rank and missing pop column
    ne_countries["ADMIN_RANK"] = 4
    geodata.add_gazetteer(
        gdf=ne_countries,
        configs=configs,
    )

    assert geodata

    # assert geodata._candidate_exists("DUMMY_PLACE_NAME") == 0

    # This tests __repr__
    assert print(geodata) is None
