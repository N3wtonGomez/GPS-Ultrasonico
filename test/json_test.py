# para poder manipular los archivos json es necesaria la libreria json
# la cual nos permitirá almacenar o leer este tipo de archivos
# de ahi en mas la informacion se maneja como un diccionario
import json

def getCoordinates(feature):
    geometry = feature["geometry"]
    return geometry["coordinates"]

def getName(feature):
    properties = feature["properties"]
    osm = properties["osm_tags"]
    return osm["name"]

with open('test/pois.json') as f: # abrimos el archivo
    payload = json.load(f) # y lo cargamos a una variable

pdi = payload["features"] # conseguimos la informacion del diccionario
# con la etiqueta features

for i in range(0, len(pdi)):
    print(getCoordinates(pdi[i]))
    print(getName(pdi[i]))
    print("-------------------")