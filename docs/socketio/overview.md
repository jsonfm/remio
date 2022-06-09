El módulo de socketIO permite realizar comunicaciones bidireccionales en tiempo real, con latencias bajas, y sencillez de uso. SocketIO es una tecnología ideal para aplicaciones de mensajería, un enfoque afin al desarrollo que plantea `remio`, debido a que los proyectos desarrollados se plantean como intercambiadores de información, en concreto, variables.

## Introducción
Existen diversas implementaciones de la tecnología SocketIO, en diversos lenguajes como python o javascript. SocketIO, presenta además dos enfoques, uno como cliente, otro como servidor, siendo este último un coordinador u entidad central, cuya labor es redigir el tráfico a sus clientes según sea conveniente.

## Eventos
SocketIO está inclinado al asincronismo, y por tanto a la programación orientada a eventos, puesto que no podemos saber en que preciso momento llegará información o la enviaremos.

```py

def connection_callback():
    print("Some connection event ocurrs!")

socket.on("connection", connection_callback)

```

## Emisión
Las comunicaciones socketIO se basan en rutas, que pueden entenderse como espacios lógicos a los que llegan los mensajes.

```py

data = {"message": "Hello world!"}
socket.emit("SOME_ROUTE", data)

```

## Transmisión de variables
Para realizar este cometido, se sugiere emplear el estándar web JSON, que en términos de python son diccionarios. En estos objetos la información es representada por pares llave/valor.
```py
"""Variables en python."""

variables = {
    'var1': 1.34, # float
    'var2': False, # bool
    'var3': 'rotate', # str
    'var4': 9, # int
}
```