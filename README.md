This simple software show in terminal a graph for desired location (inside Spain) weather information.
The information is gathered from aemet using OpenData API.
for this to work, you will need:
 - Environment variable with the OpenData API key, named OPENAPI_KEY
 - Python3
 - Python packages: pandas, altair, altair, altair_viewer, vega_datasets

To use it, simply run main.py ${search_term}
the search term should be an idema code, or a string representing a location name.

In examples:
- main.py 3194U
- main.py "MADRID UNIVERSITARIA"

If there are more than one result, them will be shown, ordered by relevance, and you can choose the desired location.
If there is a single result, requests to OpenData API will be made in order to get the last 24h weather information for this place, and displayed in your terminal in two different ways: DataFrame , and a Chart.

If you are running this in WSL, the chart will be displayed in your browser instead.

estaciones.json is updated at 2022-06-03

if need further updates on the file, run retrieve_estaciones.py

