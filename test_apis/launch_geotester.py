import geopandas as gpd
import pandas as pd

from glatteisgeoparser import GazetteerConfigs, GlatteisGeoparser, GlatteisGeoTester
from glatteisgeoparser.configs import GeoTesterConfigs

testing_data = pd.read_csv("./test_data/glatteis_sample.csv")


gigp = GlatteisGeoparser()

ne_countries = gpd.read_file("./test_data/ne_10m_admin_0_countries.zip")

configs = GazetteerConfigs(
    name="natural_earth_countries",
    index_col="ADM0_A3",
    names_col="NAME_DE",
    population_column="POP_EST",
    admin_rank=0,
    is_contextual=True,
)

gigp.add_gazetteer(gdf=ne_countries, configs=configs)

cantons = gpd.read_file("./test_data/swiss_govt_data/cantons.geojson")
cantons = cantons.to_crs("EPSG:4326")
configs = GazetteerConfigs(
    name="swissCantons",
    index_col="KANTONSNUM",
    names_col="NAME",
    population_column="EINWOHNERZ",
    admin_rank=3,
    is_contextual=True,
)
gigp.add_gazetteer(gdf=cantons, configs=configs)


munis = gpd.read_file("./test_data/swiss_govt_data/municipalities.geojson")
munis = munis.to_crs("EPSG:4326")
configs = GazetteerConfigs(
    name="swissMunicipalities",
    index_col="BFS_NUMMER",
    names_col="NAME",
    population_column="EINWOHNERZ",
    admin_rank=1,
    is_contextual=False,
)
gigp.add_gazetteer(
    gdf=munis,
    configs=configs,
)

populated_places = gpd.read_file("./test_data/ne_110m_populated_places.zip")
configs = GazetteerConfigs(
    name="naturalEarthPopulatedPlaces",
    index_col="WOF_ID",
    names_col="NAME_DE",
    population_column="POP_MIN",
    admin_rank=4,
    is_contextual=False,
)
gigp.add_gazetteer(
    gdf=populated_places,
    configs=configs,
)


configs = GeoTesterConfigs(
    data_path="./",
)

gt = GlatteisGeoTester(configs=configs, geoparsers=[gigp])

app = gt.create_testing_app(testing_data=testing_data)
app.run(debug=True)
