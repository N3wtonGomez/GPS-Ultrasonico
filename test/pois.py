# el modulo openrouteservice nos obtiene informacion
# de los lugares de interes que queremos buscar, 
# clasificados con codigos numericos almacenados en 
# el archivo yml

import openrouteservice as ors  # importamos la libreria con un sobrenombre

geojson = {
    "type":"point",
    "coordinates":[-102.262161, 21.879035] # coordenadas cerca de donde queremos buscar
}
coordinates = [-102.262161, 21.879035]# coordenadas de nuestra posicion

api_key = "5b3ce3597851110001cf62485f5107de0cc54c1db731a1aa335d7635" # api key necesaria para poder trabajar
client =  ors.Client(key=api_key) # instanciamos el cliente de la api para hacer los calculos

# places of interest
pois = client.places(
    request='pois',
    geojson=geojson, # archivo o variable con la informacion
    buffer=2000, # rango de metros en diametro del area de busqueda
    # hospital: 206, restaurant: 570
    filter_category_ids=[206, 570]
)

print(pois)