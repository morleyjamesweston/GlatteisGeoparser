import pandas as pd

from glatteisgeoparser import GlatteisGeoparser

testing_data = pd.read_csv("./test_data/glatteis_sample.csv")


glgp = GlatteisGeoparser()

app = glgp.create_testing_app(testing_data=testing_data)
app.run(debug=True)
