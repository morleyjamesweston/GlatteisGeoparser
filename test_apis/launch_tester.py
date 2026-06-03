import geopandas as gpd
import pandas as pd

from glatteisgeoparser import GazetteerConfigs, GlatteisGeoparser

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

app = gigp.create_testing_app(testing_data=testing_data)
app.run(debug=True)
