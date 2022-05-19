# programa que ayuda a personas invidentes a traves de un modulo gps 
# #recibe la informacion de este, y una interfaz
# de usuario, en manera de audio, se pueda hacr busqueda de puntos de interes, o locaciones
# especificas para proseguir en crear una lista de direcciones y poder seguir estas de manera
# autonoma y caminando, complementando la seguridad el invidente con sensores ultrasonicos
# para verificar que no haya objetos en colision con el usuario
#
# @utor: Enrique Gómez
# @utor: Jorge Garcia
# 
# derechos reservados para Tomorrowlab inc.


# libreria que realiza la busqueda de los puntos de interes
# ademas de generar la lista de indicaciones a traves de un geojson
import openrouteservice as ors
# libreria que controla los pines gpio de la raspberry
# donde estan conectados los sensores ultrasonicos, 
# adaptados a entradas usb, para facilidad de conexion
import RPi.GPIO as GPIO
# se usa para poder hacer dos o mas procesos al mismo tiempo
# de manera asincrona
import threading as th
# nos permite traducir los strings en voz 
import pyttsx3
# control del tiempo
import time
# manipulacion del archivo yml donde se encuentran almacenados
# los codigos de clasificacion de los puntos de interes
import yaml

engine = pyttsx3.init() # inciamos el motor de voz
# obtenemos la lista de las voces disponibles
voices = engine.getProperty('voices') 
# seteamos la voz a una voz femenina, aunque esta
# se encuentra en ingles
engine.setProperty('voice', voices[0].id)

# para poder hacr uso de la libreria openrouteservice se necesita
# una llave de seguridad de la api, la cual se puede obtener
# inciando sesion en la pagina web, y creando una llave de manera
# gratuita
# https://openrouteservice.org/
api_key = "5b3ce3597851110001cf62485f5107de0cc54c1db731a1aa335d7635" # api key necesaria para poder trabajar
client =  ors.Client(key=api_key) # hacemos la comunicacion con el sistema a traves de la api

# generamos una variable json con la informacion primaria del usuario,
# el tipo de ubicacion que vamos a usar, en este caso  "point", referente
# a que solo usaremos un par de coordenadas
geojson = {
    "type":"point",
    "coordinates":[-102.262161, 21.879035] # coordenadas que cambiaran conforme el gps
}
# coordenadas variables de nuestra posicion gps
coordinates = [-102.262161, 21.879035]

def Talk(message):
    # como parte de la interfaz de usuario se, usa la funcion pra que el motor de voz
    # pueda decir la informacion de salida de nuestro software, este necesita recibir
    # un string
    engine.say(message) # al motor le mandamos el string 
    engine.runAndWait() # y esperamos a que termine de hablar

def pois(id):
    # esta funcion nos permite encontrar puntos de interes, cerca de nuestra ubicacion
    # necesita que le mandemos el id, de lo que deseamos buscar
    pois = client.places(
        request='pois', # peticion de puntos de interes
        # archivo o variable con la informacion geografica del usuario
        geojson=geojson, 
        buffer=2000, # rango de metros en diametro del area de busqueda
        filter_category_ids=[id] # categoria de la bsuqueda, estas se encuentran
        # en el archivo yml
    )
    # se retorna un archivo yml, con todos los puntos de interes
    # con la informacion completas de estos, nombre, y coordenadas son las
    # que nos interesan
    return pois

def getCoordinates(feature):
    # dado el arhcivo yml, por cada punto de interes, con la seccion de "features"
    # vamos a devolver las coordenadas de las locaciones de interes
    geometry = feature["geometry"]
    return geometry["coordinates"]

def getName(feature):
    # dado el arhcivo yml, por cada punto de interes, con la seccion de "features"
    # vamos a devolver el nombre de las locaciones de interes
    properties = feature["properties"]
    osm = properties["osm_tags"]
    return osm["name"]

def getRuta(coor1, coor2):
    # el usario ya habiendo elegido la locacion a la que quiere llegar
    # hay que obtener los datos para llegar a ella,
    # recibimos dos pares de coordenadas, el punto de origen (el usuario),
    # y el destino (la locacion de interes)
    coordenadas = [coor1, coor2]
    # obtenemos toda las geo instrucciones, con la funcion 'directions'a la que le vamos a dar de parametros,
    # el como nos vamos a mover, y el como queremos obtener la informacion
    ruta = client.directions(coordinates=coordenadas, profile='foot-walking', format='geojson')
    return ruta # devolvemos un archivo yml con las instrucciones especificas

def getPasos(info):
    # el archivo yml que recibe el usario estamos en la seccion de pasos, y 
    # vamos a devolver al usario por cada paso, la instruccion necesaria
    return info["instruction"]

def getInstrucciones(features):
    # con el archivo yml vamos a leer la informacion de nuestro viaje
    secciones = features[0] # la primer seccion es la que nos da las instrucciones
    # hay que ir desglosando para poder llegar al texto con las instrucciones 
    # especificas
    propertys = secciones["properties"] # sacamos las propiedades
    segmentos = propertys["segments"] # los segmentos
    # el primer segmento contiene la informacion de la duracion del viaje
    # la distancia caminada, y un diccionario con las instrucciones 
    pasos = segmentos[0] 
    # convertimos los segundos de trayecto que nos da, a minutos
    minutos = int(pasos["duration"])/60
    # convertimos los metros que nos da a km
    km =  int(pasos["distance"])/1000
    # impirmimos en pantalla y hablamos la duracion del trayecto
    print("su viaje durará ", round(minutos) , " minutos")
    Talk(f"su viaje durará {round(minutos)} minutos")
    # impirmimos en pantalla y hablamos la distancia del trayecto
    print("su viaje será de ", km, " kilometros")
    Talk(f"su viaje será de {km} kilometros")
    # buscamos los pasos exactos que necesita nuestro viaje
    steps = pasos["steps"]
    # para cada instruccion sacamos los pasos y los leemos
    for i in range(0, len(steps)):
        print(getPasos(steps[i]))
        Talk(getPasos(steps[i]))

if __name__ == "__main__":
    #mensaje = Listener()

    # preguntamos que es lo que desea buscar
    Talk("¿que ubicacion deseas buscar?")
    mensaje = input("¿que ubicacion deseas buscar?\t")

    # cargamos las categorias
    with open('test\categorias.yml', 'r') as f:
        yml = yaml.load(f, yaml.FullLoader)

    # buscamos por claves generales, si se encontró lo que queriamos
    for clave in yml:
        if clave in mensaje:
            valores = yml.get(clave)
            break
    
    # mostramos las subcategorias que esta contiene
    subcategorias = valores["children"]
    for subcategoria in subcategorias:
        Talk(subcategoria)
        print(subcategoria)

    # cual de las anteriores le interesa
    Talk("¿especificamente que desesas buscar?")
    especifica = input("¿especificamente que desesas buscar?\t")
    minicategorias = subcategorias[especifica]
    
    # mostramos las que contienen las subcategorias
    for minicategoria in minicategorias:
        Talk(minicategoria)
        print(minicategoria)

    # que es lo que necesita buscar
    Talk("Ingresa tu interes")
    categoria_final = input("Ingresa tu interes\t")
    valor = minicategorias[categoria_final]
    
    locaciones = pois(valor) # buscamos puntos de interes con esa informacion
    pdi = locaciones["features"]
    if len(pdi) == 0: # si no se encuentra nada
        Talk("No encontramos lugares")
        print("No encontramos lugares")
    else:
        Talk("encontré estos lugares de interes")
        print("encontré estos lugares de interes")
        # mostramos los nombres
        for i in range(0, len(pdi)):
            Talk(getName(pdi[i])) 
            print(getName(pdi[i]))
            print("-------------------")
    
    # le preguntamos a donde se quiere dirigir
    Talk("¿cual es tu destino?")
    destino = input("¿cual es tu destino?\t").lower()
    #buscamos el destino
    for i in range(0, len(pdi)):
        if destino == getName(pdi[i]).lower():
            coor2 = getCoordinates(pdi[i]) #obtenemos coordenadas
            break
        else:
            print(" no te entendi")
            Talk(" no te entendi")
    
    ruta = getRuta(coordinates, coor2) # cargamos las coordenadas y calculamos la ruta

    instrucciones = getInstrucciones(ruta["features"]) # mostramos las instrucciones a seguir