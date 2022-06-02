import json

with open("test\geoinfo.json", "r") as file:
    jsonFile = json.load(file)
    file.close()

features = jsonFile["features"]
features = features[0]
propiedades = features["properties"]
segmentos = propiedades["segments"]
direcciones = segmentos[0]
pasos = direcciones["steps"]
print(len(pasos))

geometria = features["geometry"]
coordenadas = geometria["coordinates"]
print(len(coordenadas))