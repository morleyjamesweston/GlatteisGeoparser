import pandas as pd

import glatteisgeoparser

testing_data = pd.read_csv("./test_data/glatteis_sample.csv")

app = glatteisgeoparser.create_tester_app(testing_data)
app.run(debug=True)
