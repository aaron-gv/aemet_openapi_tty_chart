import http.client
import os
import json
import pandas as pd
# Visualization libs
import altair as alt
from vega_datasets import data
import sys

if len(sys.argv) < 2:
    print("insufucientes parámetros. un parametro obligatorio : idema / nombre estacion meteorologica | Not enough parameters. One required: idema / meteorologic station name")
    quit()

needle = sys.argv[1].upper()

spaces = needle.find(" ")

terms = needle.split()

with open('estaciones.json') as json_file:
    estaciones = json.load(json_file)


''' List of stations that match the search terms from user input '''
matches = []
for estacion in estaciones:
    for term in terms:
        if estacion["ubi"].find(term) != -1 or estacion["idema"].find(term) != -1:
            repeated = next((match for match in matches if match["idema"] == estacion["idema"]), False)
            if repeated == False:
                matches.append({"idema": estacion["idema"], "ubi": estacion["ubi"], "matches": 1})
            else:
                repeated["matches"]+=1

matches = sorted(matches, key=lambda d: d['matches'], reverse=True)

def printOptions(error = False):
    index = 0
    print("")
    if error:
        print("Error, ha introducido un valor incorrecto. admitidos: 0-"+str((len(matches)-1)))
    while index < (len(matches)):
        print(str(index) + ". " + matches[index]["idema"] + " " + matches[index]["ubi"])
        index+=1
    print("")

selected = 0
if len(matches) < 1:
    print("No se encontraron estaciones por: "+needle)
    print("No meteoroligic stations found by: "+needle)
    quit()
elif len(matches) > 1:
    print("hay varios resultados, elija uno 0-"+str((len(matches) - 1))+" : ")
    print("more than one match found, choose one 0-"+str((len(matches) - 1))+" : ")
    selected = -1
    error = False
    while selected < 0 or selected > len(matches):
        printOptions(error)
        error = True
        selected = int(input())
print("")
print("obteniendo información de "+matches[selected]["idema"]+" - "+matches[selected]["ubi"])
print("gathering information for "+matches[selected]["idema"]+" - "+matches[selected]["ubi"])
idema = matches[selected]["idema"]

key = os.environ.get('OPENAPI_KEY')

conn = http.client.HTTPSConnection("opendata.aemet.es")

headers = {
    'cache-control': "no-cache"
}

conn.request("GET", "/opendata/api/observacion/convencional/datos/estacion/"+idema+"/?api_key="+key, headers=headers)

res = conn.getresponse()
data = res.read()
decoded_request = json.loads(data.decode("ISO-8859-15"))

pos = decoded_request["datos"].index("opendata.aemet.es") + 17

url = decoded_request["datos"][pos:(len(decoded_request["datos"])+1)]
conn.request("GET", url, headers=headers)
res = conn.getresponse()
data = res.read()
decoded_data = sorted(json.loads(data.decode("ISO-8859-15")), key = lambda i: i['fint'],reverse=True)

'''
prec = precipitacion
hr = humedad
vv = velocidad viento
ta = temperatura
tamax = temp max
tamin = temp min
dv = direccion del viento (grados?)
vv = velocidad del viento
alt = altitud
'''

location = decoded_data[0]["ubi"]

data_frame = pd.DataFrame(decoded_data)

data_table = data_frame[["fint", "vv", "dv", "dmax", "prec", "alt", "hr", "tamin", "ta", "tamax"]]
data_table.sort_values(by=["fint"], ascending=False)

# Plain text format
print(data_table)

# Chart format
''' this will render a chart on tty. if not a tty session it will try to open your browser (I.E WSL execution) '''
alt.renderers.enable('altair_viewer')
alt.Chart(data_table).mark_point().encode(
    x='fint',
    y='ta',
    color="prec"
).show()

