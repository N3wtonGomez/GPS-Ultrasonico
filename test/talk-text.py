import speech_recognition as sr

listener = sr.Recognizer()
try:
    with sr.Microphone() as source:
        pc = listener.adjust_for_ambient_noise(source)
        rec = listener.recognize_google(
            pc,
            lenguage = "es"
        )
        rec = rec.lower()
except Exception as e:
    print(e)