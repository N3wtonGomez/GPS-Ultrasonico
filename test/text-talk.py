import pyttsx3

def Talk(engine, message):
    engine.say(message)
    engine.runAndWait()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

Talk(engine, "Hola mundo")