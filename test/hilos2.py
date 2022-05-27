from threading import Thread, Condition
from time import sleep

c = Condition()

flag = False
val = 20

def Suma():
    global val
    global flag
    while True:
        c.acquire()
        if not flag:
            val += 10
            sleep(1)

            flag = True

            c.notify_all()
        else:
            c.wait()
        c.release()

print("corriendo")

b = Thread(target=Suma)
b.start()

while True:
    c.acquire()

    if flag:
        print(f"value: {str(val)}")
        sleep(1)

        flag = False
        c.notify_all()
    else:
        c.wait()
    c.release()
