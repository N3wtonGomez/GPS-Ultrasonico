import json
import pyttsx3
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(voices[0])
engine.setProperty('voice', voices[0].id)

def Talk(message):
    engine.say(message)
    engine.runAndWait()

def getPasos(info):
    nombre = info["instruction"]
    return nombre

def getInstrucciones(features):
    secciones = features[0]
    propertys = secciones["properties"]
    segmentos = propertys["segments"]
    pasos = segmentos[0]
    print(f"su viaje durará ", pasos["duration"], " segundos")
    print(f"su viaje será de ", pasos["distance"], " metros")
    steps = pasos["steps"]
    time.sleep(4)
    print("comenzando viaje a avenida tecnologico")
    for i in range(0, len(steps)):
        print(getPasos(steps[i]))


with open("test/geoinfo.json") as f:
    payload = json.load(f)
print(type(payload))
# hacemos las instrucciones de a donde vamos a ir
instructions = getInstrucciones(payload["features"])
print(instructions)