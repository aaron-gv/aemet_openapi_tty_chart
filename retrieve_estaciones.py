import http.client
import os
import json
import pandas as pd
# Visualization libs
import altair as alt
from vega_datasets import data

key = os.environ.get('OPENAPI_KEY')

conn = http.client.HTTPSConnection("opendata.aemet.es")

headers = {
    'cache-control': "no-cache"
}
estaciones_url = "/opendata/api/observacion/convencional/todas?api_key="

conn.request("GET", estaciones_url+key, headers=headers)

res = conn.getresponse()
data = res.read().decode("ISO-8859-15")
decoded_request = json.loads(data)
pos = decoded_request["datos"].index("opendata.aemet.es") + 17
url = decoded_request["datos"][pos:(len(decoded_request["datos"])+1)]
conn.request("GET", url, headers=headers)
res = conn.getresponse()
data = res.read()
decoded_data = json.loads(data.decode("ISO-8859-15"))

tiny_list = []

for estacion in decoded_data:
    repeated = next((match for match in tiny_list if match["idema"] == estacion["idema"]), False)
    if repeated == False:
        tiny_list.append({"idema": estacion["idema"], "ubi": estacion["ubi"]})

with open('estaciones.json', 'w') as outfile:
    json.dump(tiny_list, outfile)