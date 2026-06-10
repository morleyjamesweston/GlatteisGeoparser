# Glatteis Geoparser

 A metaframework for building, testing, and using geoparsers


## Step 1: Build a geoparser, or several

This is meant to be split into moduls

```{python}
from glatteisgeoparser import RecognizerConfigs, ResolverConfigs


recognizer_configs = RecognizerConfigs(
    language="de",
    method="spacy",
    model="de_core_news_lg",
)

resolver_configs = ResolverConfigs(method="statistical")

geoparser = GlatteisGeoparser(
    language="de",
    label="basic_geoparser"
    recognizer_configs, 
    resolver_configs
)
```

# Step 2: Add geodata

```{python}
from glatteisgeoparser import GazetteerConfigs
import geopandas as gpd

ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")
ne_country_configs = GazetteerConfigs(
    name="natural_earth_countries",
    index_col="ADM0_A3",
    names_col="NAME_DE",
    population_column="POP_EST",
    admin_rank=0,
    is_contextual=True,
)
geoparser.add_gazetteer(
    gdf=ne_countries, configs=ne_country_configs
)
```

## Step 3: Test geoparsers

```{python}
tester = GlatteisGeoTester(
    geoparsers=[geoparser]
)

testing_data = pd.read_csv("./test_sample.csv")

tester.run_geoparsers(testing_data=testing_data)
```

## Step 4: Manually code test data

```{python}
app = tester.initialize_web_app(testing_data=testing_data)
app.run()
```

## Step 5: Choose the best geoparser


## Step 6: Use in production

```{python}
real_data = pd.read_csv("./test_sample.csv")
geoparser.parse(output="pandas")
```
