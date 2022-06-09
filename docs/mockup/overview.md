# Overview

## Introducción
El módulo `Mockup` está destinando a servir de plantilla base para el desarrollo de un experimento. Es una clase que contiene los atributos necesarios para administrar los procesos de comunicación serial con periféricos, así como la comunicación socketio y la lectura de imágenes.

```py

class Mockup:
    def __init__(self):
        self.camera = ...
        self.serial = ...
        self.socket = ...
```

`Mockup` es capaz de heredar sus atributos a otras clases, para poder personalizar su comportamiento.

```py
from remio import Mockup

class Robot(Mockup):
    super().__init__()
    ...
```
## Algunos conceptos
Dado que el presente framework está destinado a diversos tipos de desarrolladores, no necesariamente especializados en software, introduciremos los conceptos de repositorio de código y control de versiones.

#### Repositorio de código
Un lugar donde las diversas versiones de tu código son almacenadas. Los hay de carácter público o privado. Ejemplos de estos son: Github o Gitlab.

#### Sistema de control de versiones
Un software que almacena las modificaciones que sufran tus archivos a lo largo del tiempo. Ejemplo: Git.

!!! warning "Aviso"

    Github no es lo mismo que Git. Git es un sistema de control de versiones, Github un repositorio de código en la nube, integrado con Git.


## Estructura de Proyecto
En cuánto a la disposición de archivos para proyectos, remio ofrece flexibilidad a los desarrolladores, en cuánto estos deciden como estructurar su código. No obstante, para aquellos desarrolladores noveles, puede resultar confuso como organizarse, por ello sugerimos algunos patrones de diseño, como muetran los siguientes diagramas de árbol.

```bash
  
  project-folder
  ├── arduino
  │   └── code.ino
  ├── .env
  ├── .env.example
  ├── .gitignore
  ├── gui.py
  ├── production.py
  ├── settings.py
  ├── utils.py
  └── README.md
```

## Variables de entorno
En ciertas ocasiones será conveniente para el desarrollador tener variables solo accesibles para el entorno de ejecución del proyecto (varibles de entorno), mismas cuyo carácter general es confidencial, siendo así variables secretas. Esto es especialmente útil para manejar parámetros como contraseñas, claves de acceso a servidores, a bases de datos, y demás.

Las mencionadas variables de entorno se pueden almacenar en archivos de texto, tradicionalmente en archivos nombrados `.env` los cuales se constituyen de pares llave/valor, como se muestra a continuación:

```
# .env file
# LLAVE = VALOR
SERVER_ADDRESS = http://localhost:3000/
SERVER_KEY = 123#aVLXwd1P

```

!!! warning "Advertencia"

    Ningún archivo `.env` debe subirse a ningún repositorio.

#### Lectura de las variables de entorno
Como se mencionó, los archivos `.env` son archivos de texto, por lo tanto, bastaría con emplear los módulos por defecto de python para leer archivos, veáse por caso, las funciones open o read. No obstante, debido a la periocidad del problema, la comunidad de python ya ha desarrollado soluciones amigables para este problema.

`remio` se integra, en especifico con la librería `decouple`, cuya documentación se puede encontrar [aquí](https://github.com/henriquebastos/python-decouple/){:target="_blank"}. decouple se puede emplear de la siguiente manera:

```bash
  project-folder
  ├── .env
  └── settings.py
```

```
# .env file

SERVER_ADDRESS = http://localhost.com

```

```py
"""settings.py"""
from decouple import AutoConfig

config = AutoConfig(search_path='./')
server_address = config['SERVER_ADDRESS']

```

## Configuraciones

Para poder ajustar los parámetros del dispositivo en desarrollo, tales como el puerto serial, la dirección del servidor, la cámara, la resolución de las imágenes, se pueden pasar una serie de configuraciones, en formato de diccionarios.


```py
"""settings.py"""
# ------------------------ SERVER SETTINGS ------------------------------------

serverSettings = {
    "address": "http://localhost:3000",
    "request_timeout": 10,
}

# ------------------------- STREAM SETTINGS -----------------------------------

streamSettings = {
    "endpoint": EXPERIMENT_STREAMS_VIDEO_SERVER,
    "quality": 60,
    "fps": 15,
    "colorspace": "bgr",
    "colorsubsampling": "422",
    "fastdct": True,
    "enabled": True,
}

# ------------------------- CAMERA SETTINGS ------------------------------------

cameraSettings = {
    "webcam": {
        "src": 0,
        "fps": None,
        "size": [600, 400],
        "flipX": True,
        "flipY": False,
        "emitterIsEnabled": False,
        "backgroundIsEnabled": True,
        "processing": lambda image: print(type(image)),
        "processingParams": {},
        "encoderIsEnable": False,
    },
}

# --------------------------- SERIAL SETTINGS ------------------------------

serialSettings = {
    "arduino": {
        "port": "/dev/cu.usbserial-1460",
        "baudrate": 9600,
        "timeout": 1.0,
        "reconnectDelay": 5,
        "portsRefreshTime": 5,
        "emitterIsEnabled": True,
        "emitAsDict": True,
    },
}

```

## Inicialización

`Mockup` es capaz de interactuar con microcontroladores por medio de la comunicación serial, que en general, disponen estos dispositivos. Un ejemplo dónde sus propiedades se vuelven interesantes, es en el desarrollo de un robot. Un robot es un sistema de control que ejecuta acciones siguiendo una cierta lógica; dichas acciones pueden ser mecánicas, eléctricas, u de otra índole.

Suponiendo que desarrollamos un sistema con actuadores y queremos tener cierta potencia de computo, podemos usar un Arduino para manipular la circuitería, y una raspberry para ejecutar cálculos pesados, como procesamiento de imágenes.


```py
from remio import Mockup


class Robot(Mockup):
    def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def move(self):
        ...
    
    def sayhi(self):
        ...

    def autodestroy(self):
        ...

if __name__ == '__main__':
    robot = Robot()
    robot.start(
        camera=True, 
        serial=True, 
        socket=True, 
        streamer=True, 
        wait=True
    )    
    

```

## Interfaces gráficas

En algunas ocasiones el presente software requerirá de interfaces gráficas que permitan interactuar al usuario con el sistema desarrollado. Python tiene un ecosistema amigable, para el desarrollo de interfaces gráficas, lo cuál es particular útil para aquellos usuarios entusiastas.
