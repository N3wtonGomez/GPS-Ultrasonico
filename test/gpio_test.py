import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.IN)
GPIO.output(2,GPIO.LOW)

try: 
    while True:
        GPIO.output(2,GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(2,GPIO.LOW)
        t1 = time.time()
        while GPIO.input(3) == GPIO.LOW:
            t1 = time.time() 
        while GPIO.input(3) == GPIO.HIGH:
            t2 = time.time()
        t = t2 - t1
        d = 170 * t
        print("Distancia: ", round(d,1), "metros")
        time.sleep(2)

except: 
    GPIO.cleanup()
    print("Ha salido de modo sensado de distancia")