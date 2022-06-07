import json

with open("test\geoinfo.json", "r") as file:
    jsonFile = json.load(file)
    file.close()
print(jsonFile)
print()
print()
features = jsonFile["features"]
print(features)
print()
print()
features = features[0]
print(features)
print()
print()
propiedades = features["properties"]
print(propiedades)
print()
print()
segmentos = propiedades["segments"]
print(segmentos)
print()
print()
direcciones = segmentos[0]
print(direcciones)
print()
print()
pasos = direcciones["steps"]
print(len(pasos))

geometria = features["geometry"]
coordenadas = geometria["coordinates"]
print(len(coordenadas))