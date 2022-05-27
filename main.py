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

# esta libreria nos permite escuchar a traves del microfono
# para poder reconocer palabras y convertilas a texto
from audioop import getsample
import json
import speech_recognition as sr
# libreria que realiza la busqueda de los puntos de interes
# ademas de generar la lista de indicaciones a traves de un geojson
import openrouteservice as ors
# libreria que controla los pines gpio de la raspberry
# donde estan conectados los sensores ultrasonicos, 
# adaptados a entradas usb, para facilidad de conexion
import RPi.GPIO as GPIO
# se usa para poder hacer dos o mas procesos al mismo tiempo
# de manera asincrona
from threading import Thread, Condition
# nos permite traducir los strings en voz 
import pyttsx3
# control del tiempo
import time
# manipulacion del archivo yml donde se encuentran almacenados
# los codigos de clasificacion de los puntos de interes
import yaml

con = Condition()

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
coordinates = [0, 1]
coordinates_flag = False


# coordenadas variables de nuestra posicion gps

def getGPS():
    # esta funcion permite actualizar las coordenadas desde el gps
    global coordinates # hacemos que la variable de coordenadas sea global
    global coordinates_flag # hacemos la bandera global
    while True:
        con.acquire()
        if not coordinates_flag:
            # ! extraer coordenadas del gps
            coordinates[0] += 1
            coordinates[1] += 1

            coordinates_flag = True
            con.notify_all()
        else:
            con.wait()
        con.release()

def distancia(): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2,GPIO.OUT)
    GPIO.setup(20,GPIO.IN)
    GPIO.output(2,GPIO.LOW)

    try: 
        while True:
            GPIO.output(2,GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(2,GPIO.LOW)
            t1 = time.time()
            while GPIO.input(20) == GPIO.LOW:
                t1 = time.time() 
            while GPIO.input(20) == GPIO.HIGH:
                t2 = time.time()
            t = t2 - t1
            d = 170 * t
            print("Distancia: ", round(d,1), "metros")
            time.sleep(5)

    except: 
        GPIO.cleanup()
        print("Ha salido de modo sensado de distancia")

def getSpeech():
    # esta funcion utiliza el microfono activo de la raspb
    # para poder entender lo que dice la persona
    listener = sr.Recognizer() # inicializamos el engine
    # con el microfono como fuente empezamos a escuchar
    with sr.Microphone() as source:
        # agregamos un filtro al ruido del ambiente
        listener.adjust_for_ambient_noise(source)
        # escuchamos
        audio = listener.listen(source)
        # debemmos ingresar la funcion dentro de un try:catch
        try:
            # usamos el reconocedor de bing, pues el de google
            # ya no puede ser usado de manera gratuita
            rec = listener.recognize_google(
                audio # queremos escuchar el ruido con filtro
            )
            # nos devolverá un string, lo que pondremos en letras minusculas
            # y devolvemos esta informacion 
            return rec.lower() 
        except Exception as e:
            # si no se entiende lo que dice, o no funciona, se retorna el mensaje 
            print(e)
            return "no te entendí bien"

def Talk(message):
    # como parte de la interfaz de usuario se, usa la funcion pra que el motor de voz
    # pueda decir la informacion de salida de nuestro software, este necesita recibir
    # un string
    engine.say(message) # al motor le mandamos el string 
    engine.runAndWait() # y esperamos a que termine de hablar

def pois(id, geojson):
    print(f'pois {geojson}')
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
    print("your trip will last ", round(minutos) , " minutes")
    Talk(f"your trip will last {round(minutos)} minutes")
    # impirmimos en pantalla y hablamos la distancia del trayecto
    print("you will walk ", km, " kilometers")
    Talk(f"you will walk {km} kilometers")
    # buscamos los pasos exactos que necesita nuestro viaje
    steps = pasos["steps"]
    # para cada instruccion sacamos los pasos y los leemos
    for i in range(0, len(steps)):
        print(getPasos(steps[i]))
        Talk(getPasos(steps[i]))       

def search_pois(coordinates, geojson):
    print(f"goejson {geojson}")
    
    with open('categorias.yml', 'r') as f:
        yml = yaml.load(f, yaml.FullLoader)

    for categoria in yml:
        Talk(categoria)
        print(categoria)
    
    # preguntamos que es lo que desea buscar
    Talk("what location you want to search?")
    print("what location you want to search?")
    mensaje = getSpeech()

    # cargamos las categorias
    # buscamos por claves generales, si se encontró lo que queriamos
    for clave in yml:
        if clave in mensaje:
            print(clave)
            Talk(clave)
            valores = yml.get(clave)
            break
    
    # mostramos las subcategorias que esta contiene
    subcategorias = valores["children"]
    for subcategoria in subcategorias:
        Talk(subcategoria)
        print(subcategoria)

    # cual de las anteriores le interesa
    Talk("Specifically what do you want to look for?")
    print("Specifically what do you want to look for?")
    especifica = getSpeech()
    minicategorias = subcategorias[especifica]
    
    # mostramos las que contienen las subcategorias
    for minicategoria in minicategorias:
        Talk(minicategoria)
        print(minicategoria)

    # que es lo que necesita buscar
    Talk("say you're interest")
    print("say you're interest")
    categoria_final = getSpeech()
    valor = minicategorias[categoria_final]
    
    locaciones = pois(valor, geojson=geojson) # buscamos puntos de interes con esa informacion
    pdi = locaciones["features"]
    if len(pdi) == 0: # si no se encuentra nada
        Talk("i did'nt find locations")
        print("i did'nt find locations")
    else:
        Talk("I find this points of interest")
        print("I find this points of interest")
        # mostramos los nombres
        for i in range(0, len(pdi)):
            Talk(getName(pdi[i])) 
            print(getName(pdi[i]))
            print("-------------------")
    
    # le preguntamos a donde se quiere dirigir
    Talk("what its you're destiny?")
    print("what its you're destiny?")
    destino = getSpeech()
    #buscamos el destino
    for i in range(0, len(pdi)):
        if destino == getName(pdi[i]).lower():
            coor2 = getCoordinates(pdi[i]) #obtenemos coordenadas
            break
        else:
            print(" I did'nt get it")
            Talk(" I did'nt get it")
    
    ruta = getRuta(coordinates, coor2) # cargamos las coordenadas y calculamos la ruta
    getInstrucciones(ruta["features"]) # mostramos las instrucciones a seguir

def Menu():
    # le mostramos todas las opciones del sistema
    print("hello, where we are going today?")
    Talk("hello, where we are going today?")
    time.sleep(0.3)

    print("one. Search points of interest")
    Talk("one. Search points of interest")
    time.sleep(0.1)

    print("two. visit my favorite locations")
    Talk("two. visit my favorite locations")
    time.sleep(0.1)

    print("three. add this place to my favorites")
    Talk("three. add this place to my favorites")
    time.sleep(0.1)

    print("four. search by name")
    Talk("four. search by name")
    time.sleep(0.1)

    print("five. Repeat menu")
    Talk("five. Repeat menu")

if __name__ == "__main__":
    # creamos un hilo que usa los sensores
    hilo = Thread(name="ultrasonico1",target=distancia)
    # # inicializamos el hilo
    hilo.start()
    
    getGPS_thread = Thread(name=getGPS, target=getGPS)
    getGPS_thread.start()

    # hacemos que el programa se ejecute todo el tiempo
    while True:
        # solo se activa el programa si el usuario dice 'andromeda'
        if "andromeda" in getSpeech():
        #if True:   
            Menu() # dice el menu

            while True:
                # obtenemos la respuesta
                ans = getSpeech()
                if "points of interest" in ans or "one" in ans: # si quiere puntos de interes
                    con.acquire() # conseguimos el estado del hilo
                    # si la bandera está levantada
                    if coordinates_flag: 
                        print(f'coordenadas {coordinates}') # imprimimos las coordenadas nuevas
                        coordinates_flag = False # bajamos la bandera
                        con.notify_all() # notificamos a los hilos
                        
                        geojson = { # creamos el json
                            "type":"point",
                            "coordinates":coordinates # coordenadas que cambiaran conforme el gps
                        }
                    else:
                        con.wait() # esperamos a los hilos
                    con.release() # soltamos

                    search_pois(coordinates, geojson) # buscamos puntos de interes
                    break

                if "favorite locations" in ans or "two" in ans: # buscar sus locaciones favoritas
                    print("where you want to go?")
                    Talk("where you want to go?")

                    destino = getSpeech()

                    with open("favorites.txt", "r") as file:
                        for line in file:
                            info = str(line).split("-")
                            print(info)
                            if destino in info[0]:
                                nombre = info[0]
                                coordenadas = str(info[1]).split("\n")[0]
                                break

                    con.acquire() # conseguimos el estado del hilo
                    # si la bandera está levantada
                    if coordinates_flag: 
                        print(f'coordenadas {coordinates}') # imprimimos las coordenadas nuevas
                        coordinates_flag = False # bajamos la bandera
                        con.notify_all() # notificamos a los hilos
                        
                        geojson = { # creamos el json
                            "type":"point",
                            "coordinates":coordinates # coordenadas que cambiaran conforme el gps
                        }
                    else:
                        con.wait() # esperamos a los hilos
                    con.release() # soltamos

                    # * (las coordenadas actuales del usurio, las coordenadas de destino)
                    ruta = getRuta(coordinates, coordenadas)
                    # * sacamos las instrucciones
                    getInstrucciones(ruta)

                    break

                if "add to my favorites" in ans or "three" in ans or "tree" in ans: # agregar su ubicacion actual a favoritas
                    print("lets add you're actual location in you're favorites")
                    Talk("lets add you're actual location in you're favorites")

                    print("with wich name you want to save this location?")
                    Talk("with wich name you want to save this location?")

                    nombre = getSpeech()
                    con.acquire() # conseguimos el estado del hilo
                    # si la bandera está levantada
                    if coordinates_flag: 
                        print(f'coordenadas {coordinates}') # imprimimos las coordenadas nuevas
                        coordinates_flag = False # bajamos la bandera
                        con.notify_all() # notificamos a los hilos
        
                    else:
                        con.wait() # esperamos a los hilos
                    con.release() # soltamos

                    with open("favorites.txt", "a") as file:
                        file.write(f"{nombre}-{coordinates}\n")
                        file.close()

                    print(f"I saved this location as {nombre}")
                    Talk(f"I saved this location as {nombre}")

                    break

                if "search by name" in ans or "four" in ans:
                    print("we dont have this option yet")
                    Talk("we dont have this option yet")
                    break
               
                if "repeat" in ans or "five" in ans:
                    Menu()

                else:
                    print("I did'nt get it")
                    Talk("I did'nt get it")
                    continue
        else:
            continue