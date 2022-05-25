# GPS-Ultrasonico

Programa que ayuda a personas invidentes a traves de un modulo gps recibe la informacion de este, y una interfaz de usuario, en manera de audio, se pueda hacr busqueda de puntos de interes, o locaciones especificas para proseguir en crear una lista de direcciones y poder seguir estas de manera autonoma y caminando, complementando la seguridad el invidente con sensores ultrasonicos para verificar que no haya objetos en colision con el usuario.

# Autor

[Enrique Gómez](https://github.com/N3wtonGomez)

[Jorge García](https://github.com/Jorge02342)

# Contribuidores

# Version 1.1
Esta es una version estable, por ahora solo permite interactuar con el programa buscando las locaciones por tipo de interes, ingresando las categorias descritas en archivo yaml.

# Instalación
El software esta diseñado para usarse en una raspberry (no importa el modelo), el sistema operativo puede ser raspbian lite, o full. 

Primero copia este repositorio en tu equipo, ya sea desde raspbian, o puedes enviarlo por [ssh](https://www.hostinger.mx/tutoriales/que-es-ssh). 
#### 1. Copiar este repositorio
```
git clone https://github.com/N3wtonGomez/GPS-Ultrasonico
```
Puedes generar un [entorno vitual](https://www.freecodecamp.org/espanol/news/entornos-virtuales-de-python-explicados-con-ejemplos/), si deseas que las librerias usadas aquí, no interfieran con tu instalación de python de trabajo.
#### 2. Instalamos las dependecias necesarias
```
pip install -r requirements.txt
```

# Hardware
* [Raspberry Pi](https://www.amazon.com.mx/RASPBERRY-PI-MS-004-00000024-Raspberry-Model/dp/B01LPLPBS8/ref=sr_1_1?keywords=raspberry+pi+3+model+b&qid=1652974163&sprefix=raspberry%2Caps%2C761&sr=8-1&ufe=app_do%3Aamzn1.fos.8a46d436-f8dd-421d-a49c-494b5d1632c6).
* [Sensor Ultrasonico](https://www.amazon.com.mx/IIVVERR-ultras%C3%B3nico-distancia-Ultrasonic-Measuring/dp/B07Y7VSP1K/ref=sr_1_8?keywords=sensor+ultrasonico+hc&qid=1652974210&sprefix=sensor+ultras%2Caps%2C179&sr=8-8), puedes poner hasta 3 sensores.
* [Modulo gps](https://www.amazon.com.mx/Microcontrolador-Compatible-sensibilidad-posicionamiento-navegaci%C3%B3n/dp/B07P8YMVNT/ref=sr_1_1?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=IV3HI6P367D6&keywords=modulo+gps&qid=1652974265&sprefix=modulo+%2Caps%2C133&sr=8-1).

# Como contribuir
1. Crea un fork del repositorio en tu cuenta.
2. Haz una rama de trabajo.

<sub><sup>Retira las comillas, y pon el nombre de tu cambio</sup></sub>
```
git branch <feature-'nombreDeTuFeature'>
```
3. Escribe tu código.
4. Agrega tu nombre a la secciond e contribuidores de este documento.
5. Sube el código a tu repositorio.

<sub><sup>Retira las comillas, y pon el nombre de tu cambio</sup></sub>
```
git push -u origin <feature-'nombreDeTuFeature'>
```
6. Crea tu [pull-request](https://www.freecodecamp.org/espanol/news/como-hacer-tu-primer-pull-request-en-github/).