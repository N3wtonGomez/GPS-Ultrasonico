import speech_recognition as sr
import openrouteservice as ors
import pyttsx3
import yaml

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



api_key = "5b3ce3597851110001cf62485f5107de0cc54c1db731a1aa335d7635" # api key necesaria para poder trabajar
client =  ors.Client(key=api_key)

geojson = {
    "type":"point",
    "coordinates":[-102.262161, 21.879035] # coordenadas cerca de donde queremos buscar
}
coordinates = [-102.262161, 21.879035]# coordenadas de nuestra posicion

def Talk(message):
    engine.say(message)
    engine.runAndWait()

def Listener():
    listener= sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Hola, ¿a donde quieres ir hoy?")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            text = listener.recognize_bing(audio, lenguage="es")
            return text.lower()
    except:
        Talk("No te eh entendido")

def pois(id):
    pois = client.places(
        request='pois',
        geojson=geojson, # archivo o variable con la informacion
        buffer=2000, # rango de metros en diametro del area de busqueda
        # hospital: 206, restaurant: 570
        filter_category_ids=[id]
    )
    return pois

def getCoordinates(feature):
    geometry = feature["geometry"]
    return geometry["coordinates"]

def getName(feature):
    properties = feature["properties"]
    osm = properties["osm_tags"]
    return osm["name"]

def getRuta(coor1, coor2):
    coordenadas = [coor1, coor2]
    # obtenemos toda las geo instrucciones, con la funcion 'directions'a la que le vamos a dar de parametros,
    # el como nos vamos a mover, y el como queremos obtener la informacion
    ruta = client.directions(coordinates=coordenadas, profile='foot-walking', format='geojson')
    return ruta

def getPasos(info):
    nombre = info["instruction"]
    return nombre

def getInstrucciones(features):
    secciones = features[0]
    propertys = secciones["properties"]
    segmentos = propertys["segments"]
    pasos = segmentos[0]
    minutos = int(pasos["duration"])/60
    km =  int(pasos["distance"])/1000
    print("su viaje durará ", round(minutos) , " minutos")
    Talk(f"su viaje durará {round(minutos)} minutos")
    print("su viaje será de ", km, " kilometros")
    Talk(f"su viaje será de {km} kilometros")
    steps = pasos["steps"]
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