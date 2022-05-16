# el modulo 'openoruteservice' nos genera un archivo json con la informacion
# de una ruta creada con instrucciones especificas, lo que nos permitirá 
# poder decirle al usuario como llegar a su destino

import openrouteservice as ors # importamos la libreria con un sobrenombre
import json # importamos la libreria para guardar la informacion en tipo json

api_key = "5b3ce3597851110001cf62485f5107de0cc54c1db731a1aa335d7635" # api key necesaria para poder trabajar
client =  ors.Client(key=api_key) # instanciamos el cliente de la api para hacer los calculos

# en una lista, conformada por dos listas guardamos las coordenadas lon-lat
# poniendo primero el origen, y al ultimo el destino
coordenadas = [ [-102.262161, 21.879035], [-102.279924, 21.885105] ]

# obtenemos toda las geo instrucciones, con la funcion 'directions'a la que le vamos a dar de parametros,
# el como nos vamos a mover, y el como queremos obtener la informacion
ruta = client.directions(coordinates=coordenadas, profile='foot-walking', format='geojson')
# con la funcion 'open' la usaremos para guardar la variable anterior en un archivo json
# llamado 'geoinfo.json'
with open('test/geoinfo.json', 'w') as f:
    json.dump(ruta, f) # vertimos la informacion en el archivo json